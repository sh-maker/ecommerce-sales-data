# Generated by Django 5.1.2 on 2024-11-29 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='contact_email',
            field=models.EmailField(max_length=254),
        ),
    ]
