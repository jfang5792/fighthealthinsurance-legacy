# Generated by Django 4.1.7 on 2023-06-18 19:39

from django.db import migrations, models
import regex_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fighthealthinsurance', '0008_denialtypes_form'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('regex', regex_field.fields.RegexField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Procedures',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('regex', regex_field.fields.RegexField(max_length=400)),
            ],
        ),
        migrations.AddField(
            model_name='denial',
            name='procedure',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='denial',
            name='treatment',
            field=models.CharField(max_length=300, null=True),
        ),
    ]