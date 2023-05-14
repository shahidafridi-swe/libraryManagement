# Generated by Django 4.2.1 on 2023-05-14 13:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('accession_number', models.PositiveIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99999)])),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('publication', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('publish_year', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)])),
                ('edition', models.CharField(blank=True, max_length=255, null=True)),
                ('ISBN', models.CharField(blank=True, max_length=13, null=True)),
                ('call_number', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('page', models.PositiveIntegerField()),
                ('branch', models.CharField(choices=[('GL', 'Gulshan'), ('BR', 'Baridhara'), ('BN', 'Banani')], default='GL', max_length=2)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('tags', models.CharField(blank=True, max_length=255, null=True)),
                ('cover_photo', models.ImageField(blank=True, default='default-book.png', null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookIssue',
            fields=[
                ('person_name', models.CharField(max_length=255)),
                ('person_id', models.CharField(max_length=9, unique=True)),
                ('person_type', models.CharField(choices=[('STUDENT', 'Student'), ('FACULTY', 'Faculty')], default='STUDENT', max_length=7)),
                ('person_email', models.EmailField(max_length=255, unique=True)),
                ('person_phone', models.CharField(blank=True, max_length=11, null=True)),
                ('issued_date', models.DateField(auto_now_add=True)),
                ('return_date', models.DateField()),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('book', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='library.book')),
            ],
        ),
    ]
