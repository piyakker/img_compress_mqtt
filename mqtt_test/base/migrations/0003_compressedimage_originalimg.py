# Generated by Django 4.1.6 on 2023-02-14 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_compressedimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="compressedimage",
            name="originalImg",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="base.uploadimage",
            ),
        ),
    ]