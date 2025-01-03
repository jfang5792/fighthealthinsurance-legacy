"""Test the rest API functionality"""

import hashlib
import os
import time
import sys
import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from fighthealthinsurance.models import Denial


class Delete(APITestCase):
    """Test just the delete API."""

    fixtures = ["./fighthealthinsurance/fixtures/initial.yaml"]

    def test_url_root(self):
        url = reverse("dataremoval-list")
        email = "timbit@fighthealthinsurance.com"
        hashed_email = hashlib.sha512(email.encode("utf-8")).hexdigest()
        # Create the object
        Denial.objects.create(denial_text="test", hashed_email=hashed_email).save()
        denials_for_user_count = Denial.objects.filter(
            hashed_email=hashed_email
        ).count()
        assert denials_for_user_count > 0
        # Delete it
        response = self.client.delete(
            url, json.dumps({"email": email}), content_type="application/json"
        )
        self.assertTrue(status.is_success(response.status_code))
        # Make sure we did that
        denials_for_user_count = Denial.objects.filter(
            hashed_email=hashed_email
        ).count()
        assert denials_for_user_count == 0


class DenialLongEmployerName(APITestCase):
    """Test denial with long employer name."""

    fixtures = ["./fighthealthinsurance/fixtures/initial.yaml"]

    def test_long_employer_name(self):
        denial_text = "Group Name: "
        for a in range(0, 300):
            denial_text += str(a)
        denial_text += "INC "
        url = reverse("denials-list")
        email = "timbit@fighthealthinsurance.com"
        hashed_email = hashlib.sha512(email.encode("utf-8")).hexdigest()
        denials_for_user_count = Denial.objects.filter(
            hashed_email=hashed_email
        ).count()
        assert denials_for_user_count == 0
        # Create a denial
        response = self.client.post(
            url,
            json.dumps(
                {
                    "email": email,
                    "denial_text": denial_text,
                    "pii": "true",
                    "tos": "true",
                    "privacy": "true",
                    "store_raw_email": "true",  # Store the raw e-mail for the follow-up form
                }
            ),
            content_type="application/json",
        )
        self.assertTrue(status.is_success(response.status_code))
        denials_for_user_count = Denial.objects.filter(
            hashed_email=hashed_email,
        ).count()
        assert denials_for_user_count == 1


class DenialEndToEnd(APITestCase):
    """Test end to end, we need to load the initial fixtures so we have denial types."""

    fixtures = ["./fighthealthinsurance/fixtures/initial.yaml"]

    def test_denial_end_to_end(self):
        url = reverse("denials-list")
        email = "timbit@fighthealthinsurance.com"
        hashed_email = Denial.get_hashed_email(email)
        denials_for_user_count = Denial.objects.filter(
            hashed_email=hashed_email
        ).count()
        assert denials_for_user_count == 0
        # Create a denial
        response = self.client.post(
            url,
            json.dumps(
                {
                    "email": email,
                    "denial_text": "test",
                    "pii": "true",
                    "tos": "true",
                    "privacy": "true",
                    "store_raw_email": "true",  # Store the raw e-mail for the follow-up form
                }
            ),
            content_type="application/json",
        )
        self.assertTrue(status.is_success(response.status_code))
        parsed = response.json()
        denial_id = parsed["denial_id"]
        semi_sekret = parsed["semi_sekret"]
        # Make sure we added a denial for this user
        denials_for_user_count = Denial.objects.filter(
            hashed_email=hashed_email,
        ).count()
        assert denials_for_user_count > 0
        # Make sure we can get the denial
        denial = Denial.objects.filter(
            hashed_email=hashed_email, denial_id=denial_id
        ).get()
        print(f"We should find {denial}")
        # Now we need to poke entity extraction
        entity_extraction_url = reverse("api_streamingentity_json_backend")
        response = self.client.post(
            entity_extraction_url,
            json.dumps(
                {
                    "email": email,
                    "semi_sekret": semi_sekret,
                    "denial_id": denial_id,
                }
            ),
            content_type="application/json",
        )
        print(str(response.streaming_content))
        # Ok now lets get the additional info
        find_next_steps_url = reverse("nextsteps-list")
        find_next_steps_response = self.client.post(
            find_next_steps_url,
            json.dumps(
                {
                    "email": email,
                    "semi_sekret": semi_sekret,
                    "denial_id": denial_id,
                    "denial_type": [1, 2],
                    "diagnosis": "high risk homosexual behaviour",
                }
            ),
            content_type="application/json",
        )
        find_next_steps_parsed = find_next_steps_response.json()
        # Make sure we got back a reasonable set of questions.
        assert len(find_next_steps_parsed["combined_form"]) == 5
        assert list(find_next_steps_parsed["combined_form"][0].keys()) == [
            "name",
            "field_type",
            "label",
            "visible",
            "required",
            "help_text",
            "initial",
            "type",
        ]
        # Now we need to poke at the appeal creator
        appeals_gen_url = reverse("api_appeals_json_backend")
        appeals_gen_response = self.client.post(
            appeals_gen_url,
            json.dumps(
                {
                    "email": email,
                    "semi_sekret": semi_sekret,
                    "medical_reason": "preventive",
                    "age": "30",
                    "in_network": True,
                    "denial_id": denial_id,
                }
            ),
            content_type="application/json",
        )
        # It's a streaming response with one per new line
        text = b"".join(appeals_gen_response).split(b"\n")
        appeals = json.loads(text[0])
        assert appeals.startswith("Dear")
        # Now lets go ahead and provide follow up
        denial = Denial.objects.get(denial_id=denial_id)
        followup_url = reverse("followups-list")
        followup_response = self.client.post(
            followup_url,
            json.dumps(
                {
                    "denial_id": denial_id,
                    "uuid": str(denial.uuid),
                    "hashed_email": denial.hashed_email,
                    "user_comments": "test",
                    "appeal_result": "Yes",
                    "follow_up_again": True,
                    "follow_up_semi_sekret": denial.follow_up_semi_sekret,
                }
            ),
            content_type="application/json",
        )
        print(followup_response)
        self.assertTrue(status.is_success(followup_response.status_code))
