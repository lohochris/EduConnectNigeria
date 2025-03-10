# Generated by Django 5.1.6 on 2025-03-07 15:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tutoring', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutoringsession',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning_sessions', to='users.user'),
        ),
        migrations.AddField(
            model_name='tutoringsession',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutoring_sessions', to='users.user'),
        ),
    ]
