# Generated by Django 3.2.6 on 2021-08-15 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Genre'},
        ),
    ]
