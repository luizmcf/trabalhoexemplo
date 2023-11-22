from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import ModelForm
from caronas.forms import CaronaForm, CaronaPassageiroForm, CaronaPassageiroCartaoForm
from caronas.models import *
from django.utils.timezone import datetime


def index(request):
    profile = get_object_or_404(Profile, user=request.user)

    if profile.is_condutor:
        condutor = get_object_or_404(Condutor, id_user=profile.id)
        veiculos_list = Veiculo.objects.filter(id_condutor=condutor)

        upcoming_caronas_list = Carona.objects.filter(
            id_condutor = condutor,
            horario_carona__gte = datetime.now()
        )
        caronas_passageiro_list = {}
        for carona in upcoming_caronas_list:
            caronas_passageiro_list[carona.id] = Carona_Passageiros.objects.filter(id_carona=carona).count()

            carona_passageiros_list = Carona_Passageiros.objects.filter(id_carona = carona)
            vagas_reservadas = 0

            for carona_passageiro in carona_passageiros_list:
                log = Log_Carona.objects.filter(id_carona_passageiros = carona_passageiro).latest('horario_log')

                if log.status_carona.descricao == 'Reserva confirmada':
                    carona_passageiros = log.id_carona_passageiros
                    vagas_reservadas += int(carona_passageiros.num_pessoas)

        context = { 
            "upcoming_caronas_list" : upcoming_caronas_list,
            "veiculos_list" : veiculos_list,
            "caronas_passageiro_list" : caronas_passageiro_list,
            "vagas_reservadas" : vagas_reservadas,
            }

        print(upcoming_caronas_list, caronas_passageiro_list, sep='\n')

        return render(request,'caronas/index_condutor.html', context)

    elif profile.is_passageiro:
        caronas_passageiro = Carona_Passageiros.objects.values_list('id_carona').filter(id_passageiro=profile)
        
        condutor_list = Condutor.objects.all()
        veiculos_list = Veiculo.objects.all()

        upcoming_caronas_list = Carona.objects.filter(
            id__in=caronas_passageiro,
            horario_carona__gte = datetime.now()
        )        
        
        context = { 
            "upcoming_caronas_list" : upcoming_caronas_list,
            "condutor_list" : condutor_list,
            "veiculos_list" : veiculos_list,
            }

        print(upcoming_caronas_list, caronas_passageiro, sep='\n')

        return render(request,'caronas/index_passageiro.html', context)

    elif profile.is_admin:
        return render(request,'caronas/index_admin.html')


@login_required
def minhas_caronas(request):
    profile = get_object_or_404(Profile, user=request.user)

    if profile.is_condutor:
        condutor = get_object_or_404(Condutor, id_user=profile.id)
        veiculos_list = Veiculo.objects.filter(id_condutor=condutor)

        caronas_list = Carona.objects.filter(
            id_condutor = condutor,
        )
        caronas_passageiro_list = {}
        for carona in caronas_list:
            caronas_passageiro_list[carona.id] = Carona_Passageiros.objects.filter(id_carona=carona).count()

        context = { 
            "caronas_list" : caronas_list,
            "veiculos_list" : veiculos_list,
            "caronas_passageiro_list" : caronas_passageiro_list,
            }

        return render(request,'caronas/minhas_caronas_condutor.html', context)

    elif profile.is_passageiro:
        caronas_passageiro_list = Carona_Passageiros.objects.filter(id_passageiro=profile)
        caronas_list = []
        log_list = []
 
        condutor_list = Condutor.objects.all()
        veiculos_list = Veiculo.objects.all()

        for carona_passageiro in caronas_passageiro_list:
            carona = carona_passageiro.id_carona
            caronas_list.append(carona)

            log = Log_Carona.objects.filter(id_carona_passageiros = carona_passageiro).latest('horario_log')
            log_list.append(log)

        context = { 
            "caronas_list" : caronas_list,
            "condutor_list" : condutor_list,
            "veiculos_list" : veiculos_list,
            "log_list" : log_list
            }

        return render(request,'caronas/minhas_caronas_passageiro.html', context)

    elif profile.is_admin:
        return HttpResponseRedirect(reverse('sem_acesso'))


@login_required
def create_carona(request):
    usuario = get_object_or_404(Profile, user=request.user)
    if usuario.is_condutor and usuario.status.descricao == 'Ativo':
        if request.method == 'POST':
            carona_form = CaronaForm(request.user, request.POST, 
                                        initial={'valor_carona': '0.00', 'vagas_disponiveis': '1'})
            if carona_form.is_valid():
                carona = carona_form.save(commit=False)
                carona.id_condutor = Condutor.objects.get(id_user=Profile.objects.get(user=request.user))
                carona.observacoes = request.POST['observacoes']
                carona.cep_origem = request.POST['cep_origem']
                carona.endereco_origem = request.POST['endereco_origem']
                carona.num_origem = request.POST['num_origem']
                carona.bairro_origem = request.POST['bairro_origem']
                carona.cidade_origem = request.POST['cidade_origem']
                carona.estado_origem = request.POST['estado_origem']
                carona.cep_destino = request.POST['cep_destino']
                carona.endereco_destino = request.POST['endereco_destino']
                carona.num_destino = request.POST['num_destino']
                carona.bairro_destino = request.POST['bairro_destino']
                carona.cidade_destino = request.POST['cidade_destino']
                carona.estado_destino = request.POST['estado_destino']
                carona.save()
                return HttpResponseRedirect(
                    reverse('detail_carona_condutor', args=(carona.pk, )))
        else:
            carona_form = CaronaForm(request.user, initial={'valor_carona': '0.00', 'vagas_disponiveis': '1'})
        context = {'carona_form': carona_form}
        return render(request, 'caronas/create_carona.html', context)
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))


@login_required
def search_carona(request):
    usuario = get_object_or_404(Profile, user=request.user)
    if usuario.is_passageiro:
        context = {}
        if  request.GET.get('q_data', False) and request.GET.get('q_cid_ori', False) and request.GET.get('q_est_ori', False) and request.GET.get('q_cid_des', False) and request.GET.get('q_est_des', False):
            data_term = request.GET['q_data']
            cid_ori_term = request.GET['q_cid_ori'].lower()
            est_ori_term = request.GET['q_est_ori']
            cid_des_term = request.GET['q_cid_des'].lower()
            est_des_term = request.GET['q_est_des']
            carona_list = Carona.objects.filter(Q(horario_carona__date=datetime.strptime(data_term, '%Y-%m-%d').date()),
                                                Q(cidade_origem__icontains=cid_ori_term),
                                                Q(estado_origem__icontains=est_ori_term),
                                                Q(cidade_destino__icontains=cid_des_term),
                                                Q(estado_destino__icontains=est_des_term))
            context = {"carona_list": carona_list}
        return render(request, 'caronas/search_carona.html', context)
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))

@login_required
def detail_carona_condutor(request, carona_id):
    usuario = get_object_or_404(Profile, user=request.user)
    carona = get_object_or_404(Carona, pk=carona_id)
    if usuario.is_condutor and carona.id_condutor.id_user.user==request.user:
        profile_condutor = get_object_or_404(Profile, user=carona.id_condutor.id_user.user)
        profile_passageiro = Profile.objects.get(user=request.user)

        vagas_reservadas = 0

        if Carona_Passageiros.objects.filter(id_carona = carona).exists():
            carona_passageiros_list = Carona_Passageiros.objects.filter(id_carona = carona)

            log_list = []
            
            for carona_passageiro in carona_passageiros_list:
                log = Log_Carona.objects.filter(id_carona_passageiros = carona_passageiro).latest('horario_log')
                log_list.append(log)

                if log.status_carona.descricao == 'Reserva confirmada':
                    carona_passageiros = log.id_carona_passageiros
                    vagas_reservadas += int(carona_passageiros.num_pessoas)

            vagas_disponiveis = carona.vagas_disponiveis - vagas_reservadas
                
            context = {'carona': carona, 'veiculo': carona.id_veiculo, 'log_list': log_list, 'carona_passageiros_list': carona_passageiros_list, 'vagas_disponiveis': vagas_disponiveis}
        else:
            vagas_disponiveis = carona.vagas_disponiveis - vagas_reservadas

            context = {'carona': carona, 'veiculo': carona.id_veiculo, 'vagas_disponiveis': vagas_disponiveis}
        return render(request, 'caronas/detail_carona_condutor.html', context)
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))


@login_required
def detail_carona_passageiro(request, carona_id):
    usuario = get_object_or_404(Profile, user=request.user)
    if usuario.is_passageiro:
        carona = get_object_or_404(Carona, pk=carona_id)
        condutor = carona.id_condutor
        profile_condutor = get_object_or_404(Profile, user=condutor.id_user.user)
        profile_passageiro = Profile.objects.get(user=request.user)

        nota = 0

        if Avaliacao.objects.filter(id_condutor = condutor, passageiro_avaliou=True).exists():
            n_avaliacoes = Avaliacao.objects.filter(id_condutor = condutor, passageiro_avaliou=True).count()
            avaliacoes_list = Avaliacao.objects.filter(id_condutor = condutor, passageiro_avaliou=True)

            for avaliacao in avaliacoes_list:
                nota += avaliacao.nota_avaliacao
            nota = nota / n_avaliacoes
        else:
            nota = 5

        if Carona_Passageiros.objects.filter(id_carona = carona, id_passageiro=profile_passageiro).exists():
            carona_passageiros = Carona_Passageiros.objects.get(id_carona = carona, id_passageiro=profile_passageiro)
            log = Log_Carona.objects.filter(id_carona_passageiros = carona_passageiros).latest('horario_log')

            context = {'carona': carona, 'condutor': profile_condutor, 'veiculo': carona.id_veiculo, 'nota': nota, 'log': log, 'carona_passageiros': carona_passageiros}
        else:
            context = {'carona': carona, 'condutor': profile_condutor, 'veiculo': carona.id_veiculo, 'nota': nota}

        return render(request, 'caronas/detail_carona_passageiro.html', context)
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))

@login_required
def reservar_carona(request, carona_id):
    usuario = get_object_or_404(Profile, user=request.user)
    if usuario.is_passageiro:
        if request.method == 'POST':
            carona = get_object_or_404(Carona, pk=carona_id)
            carona_passageiros_form = CaronaPassageiroForm(Carona.objects.get(pk = carona_id), request.POST, initial={'num_pessoas': '1'})
            if carona_passageiros_form.is_valid():
                carona_passageiros = carona_passageiros_form.save(commit=False)
                carona_passageiros.id_passageiro = Profile.objects.get(user=request.user)
                carona_passageiros.id_carona = Carona.objects.get(pk = carona_id)
                carona_passageiros.save()
                if carona_passageiros.tipo_pagamento == 'dinheiro':
                    log_carona_passageiros_id = carona_passageiros
                    log_carona_passageiros_horario = datetime.now()
                    log_carona_passageiros_status = Status.objects.get(descricao='Reserva solicitada')

                    log_carona_passageiros = Log_Carona(id_carona_passageiros=log_carona_passageiros_id,
                                                        horario_log=log_carona_passageiros_horario,
                                                        status_carona=log_carona_passageiros_status)
                    log_carona_passageiros.save()
                    return HttpResponseRedirect(reverse('detail_carona_passageiro', args=(carona.pk, )))
                else:
                    return HttpResponseRedirect(reverse('pagamento_cartao', args=(carona_passageiros.id, )))
        
        else:
            carona_passageiros_form = CaronaPassageiroForm(Carona.objects.get(pk = carona_id), initial={'num_pessoas': '1'})
            carona = get_object_or_404(Carona, pk=carona_id)

        context = {'carona_passageiros_form': carona_passageiros_form, 'carona': carona}
        return render(request, 'caronas/reservar_carona.html', context)
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))


@login_required
def pagamento_cartao(request, carona_passageiros_id):
    usuario = get_object_or_404(Profile, user=request.user)
    if usuario.is_passageiro:
        carona_passageiros = get_object_or_404(Carona_Passageiros, pk=carona_passageiros_id)
        carona = carona_passageiros.id_carona

        if request.method == 'POST':
            carona_passageiros_form = CaronaPassageiroCartaoForm(request.user, request.POST)
            if carona_passageiros_form.is_valid():
                carona_passageiros.id_cartao_passageiro = carona_passageiros_form.cleaned_data['id_cartao_passageiro']
                carona_passageiros.save()
                
                log_carona_passageiros_id = carona_passageiros
                log_carona_passageiros_horario = datetime.now()
                log_carona_passageiros_status = Status.objects.get(descricao='Reserva solicitada')

                log_carona_passageiros = Log_Carona(id_carona_passageiros=log_carona_passageiros_id,
                                                    horario_log=log_carona_passageiros_horario,
                                                    status_carona=log_carona_passageiros_status)
                log_carona_passageiros.save()
                
                return HttpResponseRedirect(reverse('detail_carona_passageiro', args=(carona.pk, )))
        else:
            carona_passageiros_form = CaronaPassageiroCartaoForm(request.user)

        context = {'carona_passageiros_form': carona_passageiros_form, 'carona_passageiros': carona_passageiros}
        return render(request, 'caronas/pagamento_cartao.html', context)
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))


@login_required
def cancelar_reserva(request, carona_passageiros_id):
    usuario = get_object_or_404(Profile, user=request.user)
    if usuario.is_passageiro:
        carona_passageiros = get_object_or_404(Carona_Passageiros, pk=carona_passageiros_id)
        carona = carona_passageiros.id_carona

        if request.method == 'POST':
            carona = carona_passageiros.id_carona
            carona_passageiros.delete()          
            return HttpResponseRedirect(reverse('detail_carona_passageiro', args=(carona.pk, )))

        context = {'carona_passageiros': carona_passageiros, 'carona': carona}
        return render(request, 'caronas/cancelar_reserva.html', context)
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))


@login_required
def update_carona(request, carona_id):
    usuario = get_object_or_404(Profile, user=request.user)
    carona = get_object_or_404(Carona, pk=carona_id)

    if usuario.is_condutor and carona.id_condutor.id_user.user==request.user:
        UFs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
               'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
               'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

        if request.method == "POST":
            carona_form = CaronaForm(request.user, request.POST)
            if carona_form.is_valid():
                carona.id_veiculo = carona_form.cleaned_data['id_veiculo']
                carona.horario_carona = carona_form.cleaned_data['horario_carona']
                carona.valor_carona = carona_form.cleaned_data['valor_carona']
                carona.vagas_disponiveis = carona_form.cleaned_data['vagas_disponiveis']
                carona.observacoes = request.POST['observacoes']
                carona.cep_origem = request.POST['cep_origem']
                carona.endereco_origem = request.POST['endereco_origem']
                carona.num_origem = request.POST['num_origem']
                carona.bairro_origem = request.POST['bairro_origem']
                carona.cidade_origem = request.POST['cidade_origem']
                carona.estado_origem = request.POST['estado_origem']
                carona.cep_destino = request.POST['cep_destino']
                carona.endereco_destino = request.POST['endereco_destino']
                carona.num_destino = request.POST['num_destino']
                carona.bairro_destino = request.POST['bairro_destino']
                carona.cidade_destino = request.POST['cidade_destino']
                carona.estado_destino = request.POST['estado_destino']
                carona.save()
                return HttpResponseRedirect(
                    reverse('detail_carona_condutor', args=(carona.id, )))
        else:
            carona_form = CaronaForm(request.user,
                initial={
                    'id_veiculo': carona.id_veiculo,
                    'horario_carona': carona.horario_carona,
                    'valor_carona': carona.valor_carona,
                    'vagas_disponiveis': carona.vagas_disponiveis,
                })

        context = {'carona': carona, 'carona_form': carona_form, 'UFs': UFs}
        return render(request, 'caronas/update_carona.html', context) 
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))


@login_required
def delete_carona(request, carona_id):
    usuario = get_object_or_404(Profile, user=request.user)
    carona = get_object_or_404(Carona, pk=carona_id)

    if usuario.is_condutor and carona.id_condutor.id_user.user==request.user:   
        if request.method == "POST":
            carona.delete()          
            return HttpResponseRedirect(reverse('index'))

        context = {'carona': carona}
        return render(request, 'caronas/delete_carona.html', context) 
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))


@login_required
def finalizar_carona(request, carona_id):
    usuario = get_object_or_404(Profile, user=request.user)
    carona = get_object_or_404(Carona, pk=carona_id)

    if usuario.is_condutor and carona.id_condutor.id_user.user==request.user:   
        if request.method == "POST":
            if Carona_Passageiros.objects.filter(id_carona = carona).exists():
                carona_passageiros_list = Carona_Passageiros.objects.filter(id_carona = carona)
            
                for carona_passageiro in carona_passageiros_list:
                    log_carona_passageiros_id = carona_passageiro
                    log_carona_passageiros_horario = datetime.now()
                    log_carona_passageiros_status = Status.objects.get(descricao='Carona finalizada')

                    log_carona_passageiros = Log_Carona(id_carona_passageiros=log_carona_passageiros_id,
                                                        horario_log=log_carona_passageiros_horario,
                                                        status_carona=log_carona_passageiros_status)
                    log_carona_passageiros.save()

            return HttpResponseRedirect(
                    reverse('detail_carona_condutor', args=(carona.id, )))

        context = {'carona': carona}
        return render(request, 'caronas/finalizar_carona.html', context) 
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))


def sem_acesso(request):
    usuario = get_object_or_404(Profile, user=request.user)
    if usuario.is_condutor:
        condutor=get_object_or_404(Condutor, id_user=usuario)
        context = {'base':"base_condutor.html",'usuario': usuario,'condutor': condutor}
    elif usuario.is_passageiro:
        context = {'base':"base_passageiro.html",'usuario': usuario}
    else:
        context = {'base':"base_admin.html",'usuario': usuario}
    return render(request, 'caronas/usuario_sem_acesso.html', context)


@login_required
def aceitar_solicitacao(request, carona_id, carona_passageiros_id):
    usuario = get_object_or_404(Profile, user=request.user)
    carona = get_object_or_404(Carona, pk=carona_id)
    carona_passageiros = get_object_or_404(Carona_Passageiros, pk=carona_passageiros_id)

    if usuario.is_condutor and carona.id_condutor.id_user.user==request.user: 
        nota = 0

        if Avaliacao.objects.filter(id_passageiro = carona_passageiros.id_passageiro, passageiro_avaliou=False).exists():
            n_avaliacoes = Avaliacao.objects.filter(id_passageiro = carona_passageiros.id_passageiro, passageiro_avaliou=False).count()
            avaliacoes_list = Avaliacao.objects.filter(id_passageiro = carona_passageiros.id_passageiro, passageiro_avaliou=False)

            for avaliacao in avaliacoes_list:
                nota += avaliacao.nota_avaliacao
            nota = nota / n_avaliacoes
        else:
            nota = 5

        if request.method == 'POST' and 'btn_aceitar' in request.POST:
            log_carona_passageiros_id_carona_passageiros = carona_passageiros
            log_carona_passageiros_horario_log = datetime.now()
            log_carona_passageiros_status = Status.objects.get(descricao='Reserva confirmada')

            log_carona_passageiros = Log_Carona(id_carona_passageiros=log_carona_passageiros_id_carona_passageiros,
                                                horario_log=log_carona_passageiros_horario_log,
                                                status_carona=log_carona_passageiros_status)
            log_carona_passageiros.save()
            return HttpResponseRedirect(reverse('detail_carona_condutor', args=(carona.pk, )))
        elif request.method=='POST' and 'btn_rejeitar' in request.POST:
            log_carona_passageiros_id_carona_passageiros = carona_passageiros
            log_carona_passageiros_horario_log = datetime.now()
            log_carona_passageiros_status = Status.objects.get(descricao='Reserva cancelada')

            log_carona_passageiros = Log_Carona(id_carona_passageiros=log_carona_passageiros_id_carona_passageiros,
                                                horario_log=log_carona_passageiros_horario_log,
                                                status_carona=log_carona_passageiros_status)
            log_carona_passageiros.save()
            return HttpResponseRedirect(reverse('detail_carona_condutor', args=(carona.pk, )))

        context = {'carona_passageiros': carona_passageiros, 'carona': carona, 'nota': nota}
        return render(request, 'caronas/aceitar_solicitacao.html', context)
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))

@login_required
def avaliacao(request, carona_id, carona_passageiros_id):
    usuario = get_object_or_404(Profile, user=request.user)
    carona = get_object_or_404(Carona, pk=carona_id)
    carona_passageiros = Carona_Passageiros.objects.get(pk=carona_passageiros_id, id_carona=carona)

    if usuario.is_condutor:
        condutor = Condutor.objects.get(id_user=usuario)
        if carona.id_condutor==condutor:
            if request.method == 'POST':
                avaliacao_id_carona_passageiros = carona_passageiros
                avaliacao_id_condutor = condutor
                avaliacao_id_passageiro = carona_passageiros.id_passageiro
                avaliacao_passageiro_avaliou = False
                avaliacao_nota_avaliacao = request.POST['nota_avaliacao']
                avaliacao_comentario_avaliacao = request.POST['comentario_avaliacao']
                avaliacao_horario_avaliacao = datetime.now()
                avaliacao = Avaliacao(id_carona_passageiros=avaliacao_id_carona_passageiros,
                                        id_condutor=avaliacao_id_condutor,
                                        id_passageiro=avaliacao_id_passageiro,
                                        passageiro_avaliou=avaliacao_passageiro_avaliou,
                                        nota_avaliacao=avaliacao_nota_avaliacao,
                                        comentario_avaliacao=avaliacao_comentario_avaliacao,
                                        horario_avaliacao=avaliacao_horario_avaliacao)
                avaliacao.save()
                return HttpResponseRedirect(reverse('index'))

            passageiro = carona_passageiros.id_passageiro
            context = {'base':"base_condutor.html",'carona': carona, 'carona_passageiros': carona_passageiros, 'avaliado': passageiro}
        else: 
            return HttpResponseRedirect(reverse('sem_acesso'))  
    elif usuario.is_passageiro and carona_passageiros.id_passageiro==usuario:
        if request.method == 'POST':
            avaliacao_id_carona_passageiros = carona_passageiros
            avaliacao_id_condutor = carona.id_condutor
            avaliacao_id_passageiro = usuario
            avaliacao_passageiro_avaliou = True
            avaliacao_nota_avaliacao = request.POST['nota_avaliacao']
            avaliacao_comentario_avaliacao = request.POST['comentario_avaliacao']
            avaliacao_horario_avaliacao = datetime.now()
            avaliacao = Avaliacao(id_carona_passageiros=avaliacao_id_carona_passageiros,
                                    id_condutor=avaliacao_id_condutor,
                                    id_passageiro=avaliacao_id_passageiro,
                                    passageiro_avaliou=avaliacao_passageiro_avaliou,
                                    nota_avaliacao=avaliacao_nota_avaliacao,
                                    comentario_avaliacao=avaliacao_comentario_avaliacao,
                                    horario_avaliacao=avaliacao_horario_avaliacao)
            avaliacao.save()
            return HttpResponseRedirect(reverse('index'))

        condutor = carona.id_condutor
        context = {'base':"base_passageiro.html",'carona': carona, 'carona_passageiros': carona_passageiros, 'avaliado': condutor}

    else: 
        return HttpResponseRedirect(reverse('sem_acesso'))

    return render(request, 'caronas/avaliacao.html', context)


@login_required
def denuncia(request, carona_id, carona_passageiros_id):
    usuario = get_object_or_404(Profile, user=request.user)
    carona = get_object_or_404(Carona, pk=carona_id)
    carona_passageiros = Carona_Passageiros.objects.get(pk=carona_passageiros_id, id_carona=carona)

    if usuario.is_condutor:
        condutor = Condutor.objects.get(id_user=usuario)
        if carona.id_condutor==condutor:
            if request.method == 'POST':
                denuncia_id_carona_passageiros = carona_passageiros
                denuncia_id_condutor = condutor
                denuncia_id_passageiro = carona_passageiros.id_passageiro
                denuncia_passageiro_denunciou = False
                denuncia_motivo_denuncia = request.POST['motivo_denuncia']
                denuncia_comentario_denuncia = request.POST['comentario_denuncia']
                denuncia_status_denuncia = Status.objects.get(descricao="Aguardando verificação")
                denuncia = Denuncia(id_carona_passageiros=denuncia_id_carona_passageiros,
                                        id_condutor=denuncia_id_condutor,
                                        id_passageiro=denuncia_id_passageiro,
                                        passageiro_denunciou=denuncia_passageiro_denunciou,
                                        motivo_denuncia=denuncia_motivo_denuncia,
                                        comentario_denuncia=denuncia_comentario_denuncia,
                                        status_denuncia=denuncia_status_denuncia)
                denuncia.save()
                return HttpResponseRedirect(reverse('index'))

            passageiro = carona_passageiros.id_passageiro
            context = {'base':"base_condutor.html",'carona': carona, 'carona_passageiros': carona_passageiros, 'avaliado': passageiro}
        else: 
            return HttpResponseRedirect(reverse('sem_acesso')) 

    elif usuario.is_passageiro and carona_passageiros.id_passageiro==usuario:
        if request.method == 'POST':
            denuncia_id_carona_passageiros = carona_passageiros
            denuncia_id_condutor = carona.id_condutor
            denuncia_id_passageiro = usuario
            denuncia_passageiro_denunciou = True
            denuncia_motivo_denuncia = request.POST['motivo_denuncia']
            denuncia_comentario_denuncia = request.POST['comentario_denuncia']
            denuncia_status_denuncia = Status.objects.get(descricao="Aguardando verificação")
            denuncia = Denuncia(id_carona_passageiros=denuncia_id_carona_passageiros,
                                    id_condutor=denuncia_id_condutor,
                                    id_passageiro=denuncia_id_passageiro,
                                    passageiro_denunciou=denuncia_passageiro_denunciou,
                                    motivo_denuncia=denuncia_motivo_denuncia,
                                    comentario_denuncia=denuncia_comentario_denuncia,
                                    status_denuncia=denuncia_status_denuncia)
            denuncia.save()
            return HttpResponseRedirect(reverse('index'))

        condutor = carona.id_condutor
        context = {'base':"base_passageiro.html",'carona': carona, 'carona_passageiros': carona_passageiros, 'avaliado': condutor}

    else: 
        return HttpResponseRedirect(reverse('sem_acesso'))

    return render(request, 'caronas/denuncia.html', context)

@login_required
def usuarios_list(request):
    usuario = get_object_or_404(Profile, user=request.user)
    if usuario.is_admin:
        users_list = User.objects.all()

        context = {
            'users_list': users_list,
        }
        return render(request, 'caronas/usuarios_list.html', context)

    else:
        return HttpResponseRedirect(reverse('sem_acesso'))
