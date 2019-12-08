# Generated by Django 2.2.7 on 2019-11-27 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20191126_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(to='product.Size'),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(db_column='type_id', default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product_type', to='product.Type'),
            preserve_default=False,
        ),
    ]
