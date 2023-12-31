# Generated by Django 3.2.8 on 2021-12-08 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('caronas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='email',
        ),
        migrations.RemoveField(
            model_name='users',
            name='senha',
        ),
        migrations.RemoveField(
            model_name='users',
            name='username',
        ),
        migrations.AddField(
            model_name='users',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='avaliacao',
            name='comentario_avaliacao',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='carona',
            name='observacoes',
            field=models.CharField(default='Nenhuma observação', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cartao_passageiro',
            name='apelido_cart',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='conta_cond',
            name='apelido_conta',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='denuncia',
            name='comentario_denuncia',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='log_carona',
            name='comentario_log',
            field=models.CharField(default='-', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='resultado_denuncia',
            name='comentario_resden',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='complemento',
            field=models.CharField(default='-', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='veiculo',
            name='apelido_veic',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='verifica_cond',
            name='comentario_vercond',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='verifica_veic',
            name='comentario_verveic',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
