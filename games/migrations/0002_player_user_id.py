# Generated by Django 4.2.11 on 2024-09-22 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="user_id",
            field=models.CharField(max_length=150, null=True),
        ),
    ]
