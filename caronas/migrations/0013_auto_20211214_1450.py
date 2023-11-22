# Generated by Django 3.2.8 on 2021-12-14 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caronas', '0012_auto_20211214_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avaliacao',
            name='id_condutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caronas.condutor'),
        ),
        migrations.AlterField(
            model_name='avaliacao',
            name='id_passageiro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caronas.profile'),
        ),
        migrations.AlterField(
            model_name='denuncia',
            name='id_condutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caronas.condutor'),
        ),
        migrations.AlterField(
            model_name='denuncia',
            name='id_passageiro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caronas.profile'),
        ),
    ]