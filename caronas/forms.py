from django import forms
from django.forms import ModelForm, ValidationError
from django.db.models import fields
from django.db.models.base import Model
from django.utils.timezone import datetime

from caronas.models import Profile, Condutor, Carona, Veiculo, Carona_Passageiros, Cartao_Passageiro

class CaronaForm(ModelForm):
    class Meta:
        model = Carona
        fields = [
            'id_veiculo',
            'horario_carona',
            'valor_carona',
            'vagas_disponiveis',
        ]

        widgets = { 
            'horario_carona': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime','value': datetime.now().strftime('%d/%m/%Y %H:%M')}),
        }

        labels = {
            'id_veiculo': 'Escolha o veículo utilizado',
            'horario_carona': 'Data e horário da partida (dd/mm/aaaa HH:MM)',
            'valor_carona': 'Valor da carona (R$)',
            'vagas_disponiveis': 'Número de vagas',
        }

    def __init__(self, user, *args, **kwargs):
        super(CaronaForm, self).__init__(*args, **kwargs)
        id_user = Profile.objects.get(user=user)
        id_condutor = Condutor.objects.get(id_user=id_user)
        self.fields['id_veiculo'].queryset = Veiculo.objects.filter(id_condutor=id_condutor)
    
    def clean_vagas_disponiveis(self, *args, **kwargs):
        vagas = self.cleaned_data.get("vagas_disponiveis")
        capacidade_veic = self.cleaned_data.get("id_veiculo").capacidade_veic
        if vagas > capacidade_veic:
            raise forms.ValidationError("Número de vagas é maior do que a capacidade do veículo (máximo de " + str(capacidade_veic) + " vaga(s))")
        return vagas


class CaronaPassageiroForm(ModelForm):
    class Meta:
        model = Carona_Passageiros
        fields = [
            'num_pessoas',
            'tipo_pagamento',
        ]

        labels = {
            'num_pessoas': 'Quantidade de vagas que deseja reservar',
            'tipo_pagamento': 'Escolha a forma de pagamento',
        }

    def __init__(self, carona, *args, **kwargs):
        super(CaronaPassageiroForm, self).__init__(*args, **kwargs)
        self.fields['num_pessoas'].widget.attrs['max'] = carona.vagas_disponiveis

class CaronaPassageiroCartaoForm(ModelForm):
    class Meta:
        model = Carona_Passageiros
        fields = [
            'id_cartao_passageiro',
        ]

        labels = {
            'id_cartao_passageiro': 'Escolha o cartão utilizado',
        }

    def __init__(self, user, *args, **kwargs):
        super(CaronaPassageiroCartaoForm, self).__init__(*args, **kwargs)
        profile_user = Profile.objects.get(user=user)
        self.fields['id_cartao_passageiro'].queryset = Cartao_Passageiro.objects.filter(id_passageiro=profile_user)