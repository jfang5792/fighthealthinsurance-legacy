# Generated by Django 5.1.2 on 2024-10-09 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "fighthealthinsurance",
            "0032_rename_followup_semi_sekret_denial_follow_up_semi_sekret",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="PubMedArticleSummarized",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pmid", models.TextField(blank=True)),
                ("doi", models.TextField(blank=True)),
                ("query", models.TextField(blank=True)),
                ("title", models.TextField(blank=True, null=True)),
                ("abstract", models.TextField(blank=True, null=True)),
                ("basic_summary", models.TextField()),
                ("says_effective", models.BooleanField()),
                ("publication_date", models.DateTimeField()),
                ("retrival_date", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="PubQueryMedData",
            fields=[
                ("internal_id", models.AutoField(primary_key=True, serialize=False)),
                ("query", models.TextField(max_length=300)),
                ("articles", models.TextField(null=True)),
                ("query_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]