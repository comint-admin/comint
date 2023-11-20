# Generated by Django 4.2.5 on 2023-11-20 07:48

import comintapp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comintapp', '0004_alter_comintuser_options_alter_comintuser_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('avatar_url', models.CharField(blank=True, max_length=256, null=True)),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('ssn', models.CharField(help_text='Social Security Number in the format XXX-XX-XXXX', max_length=11, validators=[comintapp.models.validate_ssn], verbose_name='SSN')),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
    ]