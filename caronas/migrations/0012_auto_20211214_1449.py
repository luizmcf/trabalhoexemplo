# Generated by Django 3.2.8 on 2021-12-14 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caronas', '0011_alter_carona_valor_carona'),
    ]

    operations = [
        migrations.AddField(
            model_name='avaliacao',
            name='id_condutor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='caronas.condutor'),
        ),
        migrations.AddField(
            model_name='avaliacao',
            name='id_passageiro',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='caronas.profile'),
        ),
        migrations.AddField(
            model_name='avaliacao',
            name='passageiro_avaliou',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='denuncia',
            name='id_condutor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='caronas.condutor'),
        ),
        migrations.AddField(
            model_name='denuncia',
            name='id_passageiro',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='caronas.profile'),
        ),
        migrations.AddField(
            model_name='denuncia',
            name='passageiro_denunciou',
            field=models.BooleanField(default=False),
        ),
    ]
