# Generated by Django 4.2.1 on 2023-05-18 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_bookissue_librarian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='branch',
            field=models.CharField(blank=True, choices=[('GL', 'Gulshan'), ('BR', 'Baridhara'), ('BN', 'Banani')], default='GL', max_length=2, null=True),
        ),
    ]
