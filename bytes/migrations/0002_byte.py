# Generated by Django 5.0 on 2023-12-14 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bytes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Byte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=200)),
                ('desc', models.TextField(max_length=250)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
