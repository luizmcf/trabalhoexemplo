# Generated by Django 3.2.8 on 2021-12-09 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caronas', '0006_auto_20211209_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caronas.status'),
        ),
    ]