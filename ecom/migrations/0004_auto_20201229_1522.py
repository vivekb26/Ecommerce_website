# Generated by Django 3.1.4 on 2020-12-29 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0003_auto_20201229_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_desc',
            field=models.TextField(),
        ),
    ]