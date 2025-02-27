# Generated by Django 5.0.2 on 2024-06-27 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sawah', '0002_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='sawah.city')),
            ],
        ),
    ]
