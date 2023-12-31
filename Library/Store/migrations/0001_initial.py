# Generated by Django 4.2.7 on 2023-11-25 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stagiaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('prenom', models.CharField(max_length=150)),
                ('grade', models.CharField(max_length=150)),
                ('unite', models.CharField(max_length=150, null=True)),
                ('pays', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=150)),
                ('date_out', models.DateField()),
                ('date_in', models.DateField()),
                ('accompagnateur', models.TextField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('stagiaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.stagiaire')),
            ],
        ),
        migrations.CreateModel(
            name='Renseignement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='fiches')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('stagiaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.stagiaire')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motif', models.TextField(max_length=250)),
                ('destination', models.CharField(max_length=150)),
                ('date_out', models.DateField()),
                ('date_in', models.DateField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('stagiaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.stagiaire')),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medcin_decision', models.TextField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('stagiaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.stagiaire')),
            ],
        ),
    ]
