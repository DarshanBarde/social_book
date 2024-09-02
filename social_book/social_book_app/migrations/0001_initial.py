# Generated by Django 5.1 on 2024-08-20 15:24

import social_book_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('visibility', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], max_length=10)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('year_published', models.IntegerField()),
                ('file', models.FileField(upload_to='uploaded_files/', validators=[social_book_app.models.validate_file_extension])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
