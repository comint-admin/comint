# Generated by Django 4.2.5 on 2024-03-17 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comintapp', '0003_alter_locnegotiationrequest_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='locconfirmation',
            name='confirmed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]