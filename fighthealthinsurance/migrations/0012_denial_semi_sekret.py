# Generated by Django 5.0.8 on 2024-09-12 06:40

import fighthealthinsurance.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "fighthealthinsurance",
            "0011_plansource_plansourcerelation_denial_plan_source",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="denial",
            name="semi_sekret",
            field=models.CharField(
                default=fighthealthinsurance.models.sekret_gen, max_length=100
            ),
        ),
    ]