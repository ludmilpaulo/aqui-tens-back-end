# Generated by Django 5.0.3 on 2024-04-04 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, default=None, max_length=3000, upload_to='product_images/'),
        ),
    ]
