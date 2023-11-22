from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class Status(models.Model): 
    # Tabela com os status de usuários e verificações
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.descricao}'


class Profile(models.Model): 
    # Tabela com os dados dos usuários
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nascimento = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=11)
    cep = models.CharField(max_length=8)
    estado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    num_residencia = models.CharField(max_length=8)
    complemento = models.CharField(max_length=50, null=True, default="-")
    is_condutor = models.BooleanField(default=False)
    is_passageiro = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Condutor(models.Model):
    id_user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    num_carteira_motorista = models.CharField(max_length=15)
    validade_carteira = models.DateField()
    
    def __str__(self):
        return f'{self.id_user}'


class Cartao_Passageiro(models.Model):
    id_passageiro = models.ForeignKey(Profile, on_delete=models.CASCADE)
    numero_cart = models.CharField(max_length=16)
    validade_cart = models.CharField(max_length=7)
    cvn_cart = models.CharField(max_length=3)
    nome_cart = models.CharField(max_length=255)
    apelido_cart = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return f'{self.apelido_cart if self.apelido_cart else self.apelido_cart}'

class Conta_Cond(models.Model):
    id_condutor = models.ForeignKey(Condutor, on_delete=models.CASCADE)
    banco_conta = models.CharField(max_length=50)
    agencia_conta = models.CharField(max_length=4)
    num_conta = models.CharField(max_length=9)
    apelido_conta = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f'{self.apelido_conta if self.apelido_conta else self.apelido_conta}'

class Veiculo(models.Model):
    id_condutor = models.ForeignKey(Condutor, on_delete=models.CASCADE)
    fabricante_veic = models.CharField(max_length=50)
    modelo_veic = models.CharField(max_length=50)
    placa_veic = models.CharField(max_length=7)
    cor_veic = models.CharField(max_length=50)
    capacidade_veic = models.IntegerField()
    apelido_veic = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f'{self.apelido_veic if self.apelido_veic else self.modelo_veic}'

class Carona(models.Model):
    id_condutor = models.ForeignKey(Condutor, on_delete=models.CASCADE)
    id_veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    horario_carona = models.DateTimeField()
    valor_carona = models.DecimalField(max_digits=6, decimal_places=2)
    vagas_disponiveis = models.IntegerField()
    observacoes = models.CharField(max_length=255, null=True, default="Nenhuma observação")
    cep_origem = models.CharField(max_length=8)
    endereco_origem = models.CharField(max_length=255)
    num_origem = models.CharField(max_length=8)
    bairro_origem = models.CharField(max_length=255)
    cidade_origem = models.CharField(max_length=50)
    estado_origem = models.CharField(max_length=50)
    cep_destino = models.CharField(max_length=8)
    endereco_destino = models.CharField(max_length=255)
    num_destino = models.CharField(max_length=8)
    bairro_destino = models.CharField(max_length=255)
    cidade_destino = models.CharField(max_length=50)
    estado_destino = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.id_condutor} - {self.horario_carona}'

class Carona_Passageiros(models.Model):
    CARTAO = 'cartao'
    DINHEIRO = 'dinheiro'
    TIPO_PAGAMENTO_CHOICES = [
        (CARTAO, 'Cartão'),
        (DINHEIRO, 'Dinheiro'),
    ]

    id_passageiro = models.ForeignKey(Profile, on_delete=models.CASCADE)
    id_cartao_passageiro = models.ForeignKey(Cartao_Passageiro, on_delete=models.CASCADE, null=True)
    id_carona = models.ForeignKey(Carona, on_delete=models.CASCADE)
    num_pessoas = models.IntegerField()
    tipo_pagamento = models.CharField(max_length=20,choices=TIPO_PAGAMENTO_CHOICES)
    
    def __str__(self):
        return f'{self.id_carona} - {self.id_passageiro}'

class Avaliacao(models.Model):
    id_carona_passageiros = models.ForeignKey(Carona_Passageiros, on_delete=models.CASCADE)
    id_condutor  = models.ForeignKey(Condutor, on_delete=models.CASCADE)
    id_passageiro  = models.ForeignKey(Profile, on_delete=models.CASCADE)
    passageiro_avaliou = models.BooleanField(default=False)
    nota_avaliacao = models.IntegerField()
    comentario_avaliacao = models.CharField(max_length=255, null=True, blank=True)
    horario_avaliacao = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.id_carona_passageiros} - {self.nota_avaliacao}'

class Log_Carona(models.Model):
    id_carona_passageiros = models.ForeignKey(Carona_Passageiros, on_delete=models.CASCADE)
    horario_log = models.DateTimeField(default=timezone.now)
    status_carona = models.ForeignKey(Status, on_delete=models.CASCADE)
    comentario_log = models.CharField(max_length=255, null=True, default="-")
    
    def __str__(self):
        return f'{self.id_carona_passageiros} - {self.status_carona}'

class Denuncia(models.Model):
    id_carona_passageiros = models.ForeignKey(Carona_Passageiros, on_delete=models.CASCADE)
    id_condutor  = models.ForeignKey(Condutor, on_delete=models.CASCADE)
    id_passageiro  = models.ForeignKey(Profile, on_delete=models.CASCADE)
    passageiro_denunciou = models.BooleanField(default=False)
    motivo_denuncia = models.CharField(max_length=20)
    comentario_denuncia = models.CharField(max_length=255, null=True, blank=True)
    status_denuncia = models.ForeignKey(Status, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id_carona_passageiros} - {self.motivo_denuncia}'

class Resultado_Denuncia(models.Model):
    id_denuncia = models.OneToOneField(Denuncia, on_delete=models.CASCADE, primary_key=True)
    id_admin = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parecer_resden = models.CharField(max_length=20)
    comentario_resden = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f'{self.id_denuncia} - {self.parecer_resden}'