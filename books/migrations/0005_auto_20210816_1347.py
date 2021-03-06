# Generated by Django 3.2.6 on 2021-08-16 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20210815_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='publsiher',
            field=models.CharField(blank=True, help_text='Optional: You can specify the book publisher ', max_length=100, null=True, verbose_name='Publisher'),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Birthdate'),
        ),
        migrations.AlterField(
            model_name='book',
            name='edition',
            field=models.CharField(blank=True, help_text='Optional: You can specify the book edition', max_length=100, null=True, verbose_name='Edition'),
        ),
    ]
