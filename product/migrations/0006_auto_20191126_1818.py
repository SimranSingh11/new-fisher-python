# Generated by Django 2.2.7 on 2019-11-26 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_is_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='importing',
            field=models.ForeignKey(db_column='importing_id', on_delete=django.db.models.deletion.CASCADE, related_name='product_importing', to='product.Importing'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(db_column='subcategory_id', on_delete=django.db.models.deletion.CASCADE, related_name='product_subcategory', to='product.SubCategory'),
        ),
    ]
