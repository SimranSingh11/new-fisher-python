# Generated by Django 2.2.7 on 2019-11-15 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='importing_id',
            new_name='importing',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='subcategory_id',
            new_name='subcategory',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='category_id',
            new_name='category',
        ),
    ]
