# Generated by Django 2.0 on 2019-12-25 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20191225_1454'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GoodsImages',
            new_name='GoodsImage',
        ),
        migrations.AlterField(
            model_name='goodscategorybrand',
            name='image',
            field=models.ImageField(upload_to='brands/'),
        ),
    ]
