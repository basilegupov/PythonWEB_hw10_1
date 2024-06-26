# Generated by Django 5.0.5 on 2024-05-10 09:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='quotes.author'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='tags',
            field=models.ManyToManyField(to='quotes.tag'),
        ),
    ]
