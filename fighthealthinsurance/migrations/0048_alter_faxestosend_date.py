# Generated by Django 5.1.2 on 2024-11-04 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fighthealthinsurance", "0047_denial_plan_context"),
    ]

    operations = [
        migrations.AlterField(
            model_name="faxestosend",
            name="date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]