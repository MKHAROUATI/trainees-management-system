# Generated by Django 4.2.7 on 2023-11-25 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0002_permission_duration_alter_stagiaire_pays'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='duration',
            field=models.CharField(max_length=150),
        ),
    ]
