# Generated by Django 3.1.5 on 2021-01-10 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20210110_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sampleImage',
            field=models.ImageField(blank=True, default='640x360Sample.png', null=True, upload_to=''),
        ),
    ]
