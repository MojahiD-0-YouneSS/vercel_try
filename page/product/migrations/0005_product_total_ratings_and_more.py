# Generated by Django 5.1.1 on 2024-09-12 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='total_ratings',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='total_ratings_instences',
            field=models.IntegerField(default=0),
        ),
    ]
