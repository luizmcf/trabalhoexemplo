from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, fields, Sum
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
from django.forms import ModelForm
from accounts.forms import ExtendedUserCreationForm , ProfileSignUpForm, CondutorForm, Cartao_PassageiroForm, Conta_CondutorForm, VeicForm, PasswordChangeForm
from caronas.models import *


def condutor_signup(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = ProfileSignUpForm(request.POST)
        condutor_form = CondutorForm(request.POST)

        if form.is_valid() and profile_form.is_valid() and condutor_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            condutor = condutor_form.save(commit=False)

            profile.user = user
            profile.is_condutor = True
            profile.status = Status.objects.get(descricao='Aguardando verificação')
            profile.save()

            condutor.id_user = profile
            condutor.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return HttpResponseRedirect(reverse('caronas:index'))
    else:
        form = ExtendedUserCreationForm()
        profile_form = ProfileSignUpForm()
        condutor_form = CondutorForm()

    context = {'form':form, 'profile_form':profile_form, 'condutor_form':condutor_form}
    return render(request, 'accounts/condutor_signup.html', context)


def passageiro_signup(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = ProfileSignUpForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)

            profile.user = user
            profile.is_passageiro = True
            profile.status = Status.objects.get(descricao='Ativo')
            profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return HttpResponseRedirect(reverse('caronas:index'))
    else:
        form = ExtendedUserCreationForm()
        profile_form = ProfileSignUpForm()

    context = {'form':form, 'profile_form':profile_form}
    return render(request, 'accounts/passageiro_signup.html', context)


@login_required
def perfil(request):
    Usu=get_object_or_404(Profile, user=request.user)
    nota = 0

    if Usu.is_condutor:
        Cond=get_object_or_404(Condutor, id_user=Usu)

        if Avaliacao.objects.filter(id_condutor = Cond, passageiro_avaliou=True).exists():
            n_avaliacoes = Avaliacao.objects.filter(id_condutor = Cond, passageiro_avaliou=True).count()
            avaliacoes_list = Avaliacao.objects.filter(id_condutor = Cond, passageiro_avaliou=True)

            for avaliacao in avaliacoes_list:
                nota += avaliacao.nota_avaliacao
            nota = nota / n_avaliacoes
        else:
            nota = 5

        context = {'Ext':"base_condutor.html",'Usuario': Usu,'Condutor': Cond, 'Nota': nota}
    elif Usu.is_admin:
        context = {'Ext':"base_admin.html",'Usuario': Usu}
    else:
        if Avaliacao.objects.filter(id_passageiro = Usu, passageiro_avaliou=False).exists():
            n_avaliacoes = Avaliacao.objects.filter(id_passageiro = Usu, passageiro_avaliou=False).count()
            avaliacoes_list = Avaliacao.objects.filter(id_passageiro = Usu, passageiro_avaliou=False)

            for avaliacao in avaliacoes_list:
                nota += avaliacao.nota_avaliacao
            nota = nota / n_avaliacoes
        else:
            nota = 5

        context = {'Ext':"base_passageiro.html",'Usuario': Usu, 'Nota': nota}
    return render(request, 'accounts/profile.html', context)


@login_required
def pagamento_passageiro(request):
    if request.user.profile.is_passageiro==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    if request.method == 'POST':
        pag_pass_form = Cartao_PassageiroForm(request.POST, initial={'apelido_cart': 'Cartão 1'})
        if pag_pass_form.is_valid():
            pag_pass = pag_pass_form.save(commit=False)
            if pag_pass.apelido_cart==None:
                if Cartao_Passageiro.objects.filter(id_passageiro=Profile.objects.get(user=request.user)):
                    pag_pass.apelido_cart = 'Cartão '+ str(int((Cartao_Passageiro.objects.filter(id_passageiro=Profile.objects.get(user=request.user)).order_by('id').reverse()[0].id)+1))
                else:
                    pag_pass.apelido_cart = 'Cartão 1'
            if Cartao_Passageiro.objects.filter(id_passageiro=Profile.objects.get(user=request.user),apelido_cart=pag_pass.apelido_cart):
                pag_pass.apelido_cart=str(pag_pass.apelido_cart)+'_2'
            pag_pass.id_passageiro = Profile.objects.get(user=request.user)
            pag_pass.save()
            return HttpResponseRedirect(
                reverse('pagamento'))
    else:
        pag_pass_form = Cartao_PassageiroForm()
    context = {'cartao_form': pag_pass_form}
    return render(request, 'accounts/pagamento_passageiro.html', context)

    
@login_required
def conta_condutor(request):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    if request.method == 'POST':
        form = Conta_CondutorForm(request.POST)
        if form.is_valid():
            formulario = form.save(commit=False)
            if formulario.apelido_conta==None:
                if Conta_Cond.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user))):
                    formulario.apelido_conta='Conta '+ str(int((Conta_Cond.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user))).order_by('id').reverse()[0].id)+1))
                else:
                    formulario.apelido_conta='Conta 1'
            if Conta_Cond.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)),apelido_conta=formulario.apelido_conta):
                formulario.apelido_conta=str(formulario.apelido_conta)+'_2'
            formulario.id_condutor = Condutor.objects.get(id_user=Profile.objects.get(user=request.user))
            formulario.save()
            return HttpResponseRedirect(
                reverse('pagamento'))
    else:
        form = Conta_CondutorForm()
    context = {'form': form}
    return render(request, 'accounts/conta_condutor.html', context)

@login_required
def pagamento(request):
    Usu=get_object_or_404(Profile, user=request.user)
    if Usu.is_condutor:
        pag_list=Conta_Cond.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)))
        context = {'Ext':"base_condutor.html",'Usuario': Usu,'pag_list': pag_list}
    elif Usu.is_admin:
        context = {'Ext':"base_admin.html",'Usuario': Usu}
    else:
        pag_list = Cartao_Passageiro.objects.filter(id_passageiro=Profile.objects.get(user=request.user))
        context = {'Ext':"base_passageiro.html",'Usuario': Usu,'pag_list': pag_list}
    return render(request, 'accounts/pagamento.html', context)

@login_required
def criar_veiculos(request):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    if request.method == 'POST':
        form = VeicForm(request.POST)
        if form.is_valid():
            formulario = form.save(commit=False)
            if formulario.apelido_veic==None:
                if Veiculo.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user))):
                    formulario.apelido_veic='Veículo '+ str(int((Veiculo.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user))).order_by('id').reverse()[0].id)+1))
                else:
                    formulario.apelido_veic='Veículo 1'
            if Veiculo.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)),apelido_veic=formulario.apelido_veic):
                formulario.apelido_veic=str(formulario.apelido_veic)+'_2'
            formulario.id_condutor = Condutor.objects.get(id_user=Profile.objects.get(user=request.user))
            formulario.save()
            return HttpResponseRedirect(
                reverse('veiculos'))
    else:
        form = VeicForm()
    context = {'form': form}
    return render(request, 'accounts/veiculos_criar.html', context)

@login_required
def veiculos(request):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    veic_list=Veiculo.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)))
    context={'veic_list':veic_list}
    return render(request, 'accounts/veiculos.html', context)


@login_required
def veic_detail(request, veic_id):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    veic_list=get_object_or_404(Veiculo, id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)), id=veic_id)
    context={'veic':veic_list}
    return render(request, 'accounts/veic_detail.html', context)

@login_required
def conta_detail(request, conta_id):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    conta_list=get_object_or_404(Conta_Cond,id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)),id=conta_id)
    context={'conta':conta_list}
    return render(request, 'accounts/conta_detail.html', context)

@login_required
def cart_detail(request, cart_id):
    if request.user.profile.is_passageiro==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    cart_list=get_object_or_404(Cartao_Passageiro,id_passageiro=Profile.objects.get(user=request.user),id=cart_id)
    context={'cart':cart_list}
    return render(request, 'accounts/cart_detail.html', context)

@login_required
def veic_delete(request, veic_id):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    veic=get_object_or_404(Veiculo, id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)), id=veic_id)

    if request.method == 'POST':
        veic.delete()          
        return HttpResponseRedirect(reverse('veiculos'))

    context = {'veic': veic}
    return render(request, 'accounts/veic_delete.html', context)

@login_required
def conta_delete(request, conta_id):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    conta=get_object_or_404(Conta_Cond,id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)),id=conta_id)
    if request.method == 'POST':
        conta.delete()          
        return HttpResponseRedirect(reverse('pagamento'))

    context = {'conta': conta}
    return render(request, 'accounts/conta_delete.html', context)

@login_required
def cart_delete(request, cart_id):
    if request.user.profile.is_passageiro==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    cart=get_object_or_404(Cartao_Passageiro,id_passageiro=Profile.objects.get(user=request.user),id=cart_id)
    if request.method == 'POST':
        cart.delete()          
        return HttpResponseRedirect(reverse('pagamento'))

    context = {'cart': cart}
    return render(request, 'accounts/cart_delete.html', context)

def alterar_senha(request):
    form = PasswordChangeForm(request.user, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('perfil'))
    else:        
        form = PasswordChangeForm(request.user)
    Usu=get_object_or_404(Profile, user=request.user)
    if Usu.is_condutor:
        context = {'Ext':"base_condutor.html",'form':form}
    elif Usu.is_admin:
        context = {'Ext':"base_admin.html",'form':form}
    else:
        context = {'Ext':"base_passageiro.html",'form':form}
    return render(request, 'accounts/change_password.html', context)

@login_required
def veic_update(request, veic_id):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    try:
        del request.session['update_veic']
    except KeyError:
        pass
    veic=get_object_or_404(Veiculo, id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)), id=veic_id)
    cores=['Amarelo','Azul','Bege','Branca','Cinza','Dourada','Grena','Laranja','Marrom','Prata','Preta','Rosa','Roxa','Verde','Vermelha','Fantasia']
    if request.method == 'POST':
        apelido_veic=request.POST['apelido_veic']
        cor_veic=request.POST['cor_sel']
        request.session['update_veic'] = [apelido_veic,cor_veic]
        return HttpResponseRedirect(reverse('veic_update_confirma',args=(veic_id, )))

    context = {'veic': veic,'cores':cores}
    return render(request, 'accounts/veic_update.html', context)

@login_required
def veic_update_confirma(request, veic_id):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    veic=get_object_or_404(Veiculo, id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)), id=veic_id)
    if 'update_veic' in request.session:
        cookie=request.session['update_veic']
        if cookie[0]==None:
            if Veiculo.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user))):
                cookie[0]='Veículo '+ str(int((Veiculo.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user))).order_by('id').reverse()[0].id)+1))
            else:
                cookie[0]='Veículo 1'
        if Veiculo.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)),apelido_veic=cookie[0]) and cookie[0]!=veic.apelido_veic:
            cookie[0]=str(cookie[0])+'_2'
        veic.apelido_veic=cookie[0]
        veic.cor_veic=cookie[1]
    cores=['Amarelo','Azul','Bege','Branca','Cinza','Dourada','Grena','Laranja','Marrom','Prata','Preta','Rosa','Roxa','Verde','Vermelha','Fantasia']
    if request.method == 'POST':
        veic.save()   
        return HttpResponseRedirect(reverse('veic_detail',args=(veic_id, )))

    context = {'veic': veic,'cores':cores}
    return render(request, 'accounts/veic_update_confirma.html', context)

@login_required
def cart_update(request, cart_id):
    if request.user.profile.is_passageiro==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    try:
        del request.session['update_cart']
    except KeyError:
        pass
    cart=get_object_or_404(Cartao_Passageiro,id_passageiro=Profile.objects.get(user=request.user),id=cart_id)
    if request.method == 'POST':
        apelido_cart=request.POST['apelido_cart']
        request.session['update_cart'] = [apelido_cart]
        return HttpResponseRedirect(reverse('cart_update_confirma',args=(cart_id, )))

    context = {'cart': cart}
    return render(request, 'accounts/cart_update.html', context)

@login_required
def cart_update_confirma(request, cart_id):
    if request.user.profile.is_passageiro==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    cart=get_object_or_404(Cartao_Passageiro,id_passageiro=Profile.objects.get(user=request.user),id=cart_id)
    if 'update_cart' in request.session:
        cookie=request.session['update_cart']
        if cookie[0]==None:
            if Cartao_Passageiro.objects.filter(id_passageiro=Profile.objects.get(user=request.user)):
                cookie[0] = 'Cartão '+ str(int((Cartao_Passageiro.objects.filter(id_passageiro=Profile.objects.get(user=request.user)).order_by('id').reverse()[0].id)+1))
            else:
                cookie[0] = 'Cartão 1'
        if Cartao_Passageiro.objects.filter(id_passageiro=Profile.objects.get(user=request.user),apelido_cart=cookie[0]) and cookie[0]!=cart.apelido_cart:
            cookie[0]=str(cookie[0])+'_2'
        cart.apelido_cart=cookie[0]
    if request.method == 'POST':
        cart.save()   
        return HttpResponseRedirect(reverse('cart_detail',args=(cart_id, )))

    context = {'cart': cart}
    return render(request, 'accounts/cart_update_confirma.html', context)

@login_required
def conta_update(request, conta_id):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    try:
        del request.session['update_conta']
    except KeyError:
        pass
    conta=get_object_or_404(Conta_Cond,id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)),id=conta_id)
    if request.method == 'POST':
        apelido_conta=request.POST['apelido_conta']
        request.session['update_conta'] = [apelido_conta]
        return HttpResponseRedirect(reverse('conta_update_confirma',args=(conta_id, )))

    context = {'conta': conta}
    return render(request, 'accounts/conta_update.html', context)

@login_required
def conta_update_confirma(request, conta_id):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    conta=get_object_or_404(Conta_Cond,id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)),id=conta_id)
    if 'update_conta' in request.session:
        cookie=request.session['update_conta']
        if cookie[0]==None:
            if Conta_Cond.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user))):
                cookie[0]='Conta '+ str(int((Conta_Cond.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user))).order_by('id').reverse()[0].id)+1))
            else:
                cookie[0]='Conta 1'
        if Conta_Cond.objects.filter(id_condutor=Condutor.objects.get(id_user=Profile.objects.get(user=request.user)),apelido_conta=cookie[0]) and cookie[0]!=conta.apelido_conta:
                cookie[0]=str(cookie[0])+'_2'
        conta.apelido_conta=cookie[0]
    if request.method == 'POST':
        conta.save()   
        return HttpResponseRedirect(reverse('conta_detail',args=(conta_id, )))

    context = {'conta': conta}
    return render(request, 'accounts/conta_update_confirma.html', context)

@login_required
def perfil_update(request):
    try:
        del request.session['update_perfil']
    except KeyError:
        pass 
    Usu=get_object_or_404(Profile, user=request.user)
    Estados=['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
               'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
               'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    Erro=""
    if request.method == 'POST':
        primeiro_nome=request.POST.get('primeiro_nome',False)
        segundo_nome=request.POST.get('segundo_nome',False)
        email=request.POST.get('email',False)
        cpf=request.POST.get('cpf',False)
        nascimento=request.POST.get('nascimento',False)
        telefone=request.POST.get('telefone',False)
        cep=request.POST.get('cep',False)
        endereco=request.POST.get('endereco',False)
        num_residencia=request.POST.get('num_residencia',False)
        complemento=request.POST.get('complemento',False)
        bairro=request.POST.get('bairro',False)
        cidade=request.POST.get('cidade',False)
        estado=request.POST.get('estado',False)
        i=0
        i_arroba=int(len(email))
        val_1=False
        val_2=False
        val_3=False
        val_4=telefone.isnumeric()
        val_5=cpf.isnumeric()
        val_6=cep.isnumeric()
        val_7=False
        if num_residencia.isnumeric():
            if int(num_residencia)>0:
                val_7=True
        for c in email:
            if c == '@' and i!=0 and i<int(len(email)-3):
                val_1=True
                i_arroba=i
            if c=='.' and i>=i_arroba:
                val_2=True
            if c=='@' and i_arroba!=int(len(email)):
                val_3=True
            i=i+1
        if not(val_1 and val_2 and val_3):
            Erro="Email inválido"
        if not(val_4):
            Erro="Telefone inválido"
        if not(val_5):
            Erro="CPF inválido"
        if not(val_6):
            Erro="CEP inválido"
        if not(val_7):
            Erro="Número da residência inválido"
        if complemento=="":
            complemento="-"
        if val_1 and val_2 and val_3 and val_4 and val_5 and val_6 and val_7:
            request.session['update_perfil'] = [primeiro_nome,segundo_nome,email,cpf,nascimento,telefone,cep,endereco,num_residencia,complemento,bairro,cidade,estado]
            return HttpResponseRedirect(reverse('perfil_update_confirma'))
    if Usu.is_condutor:
        context = {'Ext':"base_condutor.html",'Usuario': Usu,'Estados':Estados,'Erro':Erro}
    elif Usu.is_admin:
        context = {'Ext':"base_admin.html",'Usuario': Usu,'Estados':Estados,'Erro':Erro}
    else:
        context = {'Ext':"base_passageiro.html",'Usuario': Usu,'Estados':Estados,'Erro':Erro}
    return render(request, 'accounts/profile_update.html', context)

@login_required
def perfil_update_confirma(request):
    user=request.user
    Usu=get_object_or_404(Profile, user=request.user)
    Estados=['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
               'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
               'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    if 'update_perfil' in request.session:
        cookie=request.session['update_perfil']
        user.first_name=cookie[0]
        user.last_name=cookie[1]
        user.email=cookie[2]
        Usu.cpf=cookie[3]
        Usu.nascimento=datetime.date(int(cookie[4][0:4]),int(cookie[4][5:7]),int(cookie[4][8:10]))
        Usu.telefone=cookie[5]
        Usu.cep=cookie[6]
        Usu.endereco=cookie[7]
        Usu.num_residencia=cookie[8]
        Usu.complemento=cookie[9]
        Usu.bairro=cookie[10]
        Usu.cidade=cookie[11]
        Usu.estado=cookie[12]
    if request.method == 'POST':
        user.save()
        Usu.save() 

        return HttpResponseRedirect(reverse('perfil'))
    if Usu.is_condutor:
        context = {'Ext':"base_condutor.html",'Usuario': Usu,'Estados':Estados}
    elif Usu.is_admin:
        context = {'Ext':"base_admin.html",'Usuario': Usu,'Estados':Estados}
    else:
        context = {'Ext':"base_passageiro.html",'Usuario': Usu,'Estados':Estados}
    return render(request, 'accounts/profile_update_confirma.html', context)

@login_required
def perfil_update_condutor(request):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    try:
        del request.session['update_perfil']
    except KeyError:
        pass 
    Usu=get_object_or_404(Profile, user=request.user)
    Cond=get_object_or_404(Condutor, id_user=Usu)
    Erro=""
    if request.method == 'POST':
        num_carteira_motorista=request.POST['num_carteira_motorista']
        validade_carteira=request.POST['validade_carteira']
        val_1=False
        if num_carteira_motorista.isnumeric():
            if len(num_carteira_motorista)==15:
                val_1=True
        if not(val_1):
            Erro="Número da carteira inválido"

        if val_1:
            request.session['update_perfil_condutor'] = [num_carteira_motorista,validade_carteira]
            return HttpResponseRedirect(reverse('perfil_update_condutor_confirma'))
    context={'Usuario':Usu,'Condutor':Cond,'Erro':Erro}
    return render(request, 'accounts/profile_update_condutor.html', context)

@login_required
def perfil_update_condutor_confirma(request):
    if request.user.profile.is_condutor==False:
        return HttpResponseRedirect(reverse('sem_acesso'))
    Usu=get_object_or_404(Profile, user=request.user)
    Cond=get_object_or_404(Condutor, id_user=Usu)
    if 'update_perfil_condutor' in request.session:
        cookie=request.session['update_perfil_condutor']
        Cond.num_carteira_motorista=cookie[0]
        Cond.validade_carteira=datetime.date(int(cookie[1][0:4]),int(cookie[1][5:7]),int(cookie[1][8:10]))
    if request.method == 'POST':
        Cond.save() 

        return HttpResponseRedirect(reverse('perfil'))
    context={'Usuario':Usu,'Condutor':Cond}
    return render(request, 'accounts/profile_update_condutor_confirma.html', context)


@login_required
def historico(request):
    Usu=get_object_or_404(Profile, user=request.user)
    filtro="Data_Inv"
    if request.method == 'POST':
        if request.POST['order']=="Data_Inv":
            filtro="Data_Inv"
        if request.POST['order']=="horario_carona":
            filtro="horario_carona"
        if request.POST['order']=="cidade_origem":
            filtro="cidade_origem"
        if request.POST['order']=="cidade_destino":
            filtro="cidade_destino"
    if Usu.is_condutor:
        caronas_list=Carona.objects.filter(id_condutor__id_user__user=request.user)
        caronas_list=caronas_list.filter(carona_passageiros__log_carona__status_carona__descricao="Carona finalizada").annotate(vagas=Sum('carona_passageiros__num_pessoas'))
        context = {'Ext':"base_condutor.html",'caronas_list': caronas_list,'filtro':filtro}
    elif Usu.is_admin:
        return HttpResponseRedirect(reverse('sem_acesso'))
    else:
        caronas_list=Carona.objects.filter(carona_passageiros__id_passageiro__user=request.user)
        caronas_list=caronas_list.filter(carona_passageiros__log_carona__status_carona__descricao="Carona finalizada")
        context = {'Ext':"base_passageiro.html",'caronas_list': caronas_list,'filtro':filtro}
    return render(request, 'accounts/historico.html', context)

@login_required
def historico_detail(request,carona_id):
    Usu=get_object_or_404(Profile, user=request.user)
    if Usu.is_condutor:
        carona=Carona.objects.filter(id_condutor__id_user__user=request.user,pk=carona_id)
        carona=carona.filter(carona_passageiros__log_carona__status_carona__descricao="Carona finalizada").annotate(vagas=Sum('carona_passageiros__num_pessoas'))
        carona=carona[0]
        context = {'Ext':"base_condutor.html",'carona': carona}
    elif Usu.is_admin:
        return HttpResponseRedirect(reverse('sem_acesso'))
    else:
        carona=Carona.objects.filter(carona_passageiros__id_passageiro__user=request.user,pk=carona_id)
        carona=carona.filter(carona_passageiros__log_carona__status_carona__descricao="Carona finalizada")
        carona=carona[0]
        context = {'Ext':"base_passageiro.html",'carona': carona}
    return render(request, 'accounts/historico_detail.html', context)

def admin_detail_profile(request, profile_id):
    usuario = get_object_or_404(Profile, user=request.user)
    
    if usuario.is_admin:
        profile = get_object_or_404(Profile, pk=profile_id)
        
        if profile.is_condutor:
            condutor = get_object_or_404(Condutor, id_user=profile.id)
            veiculos = Veiculo.objects.filter(id_condutor=condutor)
            caronas = Carona.objects.filter(id_condutor=condutor)
            context = { 
                'profile' : profile,
                'condutor' : condutor,
                'veiculos' : veiculos,
                'caronas' : caronas
            }

        elif profile.is_passageiro:
            caronas_passageiro = Carona_Passageiros.objects.filter(id_passageiro=profile)
            caronas = Carona.objects.filter(id__in=caronas_passageiro.values_list('id_carona'),)  
            context = { 
                'profile' : profile,
                'caronas' : caronas,
                'caronas_passageiro' : caronas_passageiro,
            }
        else: #is_admin
            context = { 
                'profile' : profile,
            }
        return render(request, 'accounts/profile_admin.html', context)
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))


@login_required
def novos_condutores(request):
    usuario = get_object_or_404(Profile, user=request.user)

    if usuario.is_admin:
        if Profile.objects.filter(status = Status.objects.get(descricao="Aguardando verificação")).exists():
            profile_list = Profile.objects.filter(status = Status.objects.get(descricao="Aguardando verificação"))
            condutor_list = Condutor.objects.all() 

            context = {'usuario': usuario, 'profile_list': profile_list, 'condutor_list': condutor_list}
        else:
            context = {'usuario': usuario}
        return render(request, 'accounts/novos_condutores.html', context)
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))


@login_required
def verificar_condutor(request, profile_id):
    usuario = get_object_or_404(Profile, user=request.user)
    profile_condutor = get_object_or_404(Profile, id=profile_id)
    condutor = get_object_or_404(Condutor, id_user=profile_id)

    if usuario.is_admin:
        if request.method == 'POST' and 'btn_ativo' in request.POST:
            profile_condutor.status = Status.objects.get(descricao='Ativo')
            profile_condutor.save()
            return HttpResponseRedirect(reverse('novos_condutores'))

        elif request.method=='POST' and 'btn_inativo' in request.POST:
            profile_condutor.status = Status.objects.get(descricao='Inativo')
            profile_condutor.save()
            return HttpResponseRedirect(reverse('novos_condutores'))

        context = {'Usuario': profile_condutor, 'Condutor': condutor}
        return render(request, 'accounts/verificar_condutor.html', context)
    else:
        return HttpResponseRedirect(reverse('sem_acesso'))