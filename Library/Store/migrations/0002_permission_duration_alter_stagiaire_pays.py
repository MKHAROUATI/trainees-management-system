# Generated by Django 4.2.7 on 2023-11-25 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='duration',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='pays',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]