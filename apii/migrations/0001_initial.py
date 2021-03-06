# Generated by Django 4.0.4 on 2022-05-26 20:26

import apii.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TemporaryUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_url', models.CharField(max_length=250)),
                ('tmp_url', models.CharField(default=apii.models.generate_url, max_length=100)),
                ('expires', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Tier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('can_link_200px_height', models.BooleanField(default=False)),
                ('can_link_400px_height', models.BooleanField(default=False)),
                ('can_link_custom_height', models.BooleanField(default=False)),
                ('custom_height_px', models.PositiveIntegerField(blank=True, null=True)),
                ('can_link_original_image', models.BooleanField(default=False)),
                ('can_create_tmp_url', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OriginalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, upload_to=apii.models.file_location_original)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apii.author')),
            ],
        ),
        migrations.CreateModel(
            name='CompressedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to=apii.models.file_location_compressed)),
                ('px', models.PositiveIntegerField()),
                ('original', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apii.originalimage')),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='tier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apii.tier'),
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
