# Generated by Django 4.2.16 on 2024-12-28 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0011_alter_recipe_cooking_time_alter_recipe_desc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='additional_quantity',
            field=models.IntegerField(blank=True, default=1, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='raw_weight',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, verbose_name='Сырой вес, г'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, verbose_name='Вес после обработки, г'),
        ),
    ]
