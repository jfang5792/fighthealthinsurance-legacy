# Generated by Django 5.1.4 on 2025-02-12 06:31

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fighthealthinsurance", "0073_appeal_combined_document_enc"),
    ]

    operations = [
        migrations.AddField(
            model_name="appeal",
            name="uuid_field",
            field=models.CharField(
                default=uuid.uuid4, editable=False, max_length=100, unique=True
            ),
        ),
    ]
