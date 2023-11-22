from django import forms
from django.forms import ModelForm
from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models.base import Model

from caronas.models import Profile, Condutor, Cartao_Passageiro, Conta_Cond, Veiculo

class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Nome")
    last_name = forms.CharField(max_length=200, required=True, label="Sobrenome")
    
    class Meta:
        model = User
        fields = [ 'username', 'email', 'first_name', 'last_name', 'password1', 'password2' ]


    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user

class ProfileSignUpForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'nascimento',
            'cpf',
            'telefone',
            'cep',
            'endereco',
            'num_residencia',
            'complemento',
            'bairro',
            'cidade',
            'estado',
        ]
        
        UFs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
               'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
               'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
        for i in range(len(UFs)):
            UFs[i] = (UFs[i],UFs[i])
        widgets = { 
            'nascimento': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'type':'date'}),
            'estado':  forms.Select(choices=UFs), 
            }

        labels = {
            'nascimento':'Data de nascimento',
            'cpf':'CPF (apenas números)',
            'telefone':'Telefone',
            'cep':'CEP',
            'estado':'Estado',
            'cidade':'Cidade',
            'bairro':'Bairro',
            'endereco':'Endereço',
            'num_residencia':'Número',
            'complemento':'Complemento',
        }

class CondutorForm(ModelForm):
    class Meta:
        model = Condutor
        fields = [
            'num_carteira_motorista',
            'validade_carteira',
        ]
        
        widgets = { 
            'validade_carteira': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'type':'date'}),
        }

        labels = {
            'num_carteira_motorista':'Nº registro',
            'validade_carteira':'Data de validade',
        }

    def save(self, commit=True):
        user = super().save(commit=False)

        user.num_carteira_motorista = self.cleaned_data['num_carteira_motorista']
        user.validade_carteira = self.cleaned_data['validade_carteira']

        if commit:
            user.save()
        return user

class Cartao_PassageiroForm(ModelForm):
    class Meta:
        model = Cartao_Passageiro
        fields = [
            'numero_cart',
            'validade_cart',
            'cvn_cart',
            'nome_cart',
            'apelido_cart',
        ]

        widgets = { 
            'validade_cart': forms.DateInput(format=('%m%Y'), attrs={'class':'form-control', 'type':'month'}),
            }

        labels = {
            'numero_cart':'Número do cartão:',
            'validade_cart':'Validade:',
            'cvn_cart':'CVN:',
            'nome_cart':'Nome no cartão:',
            'apelido_cart':'*Apelido para o cartão:',
        }


class Conta_CondutorForm(ModelForm):
    class Meta:
        model = Conta_Cond
        fields = [
            'banco_conta',
            'agencia_conta',
            'num_conta',
            'apelido_conta',
        ]
        Bancos = ['001 – Banco do Brasil S.A.',
        '341 – Banco Itaú S.A.',
        '033 – Banco Santander (Brasil) S.A.',
        '356 – Banco Real S.A. (antigo)',
        '652 – Itaú Unibanco Holding S.A.',
        '237 – Banco Bradesco S.A.',
        '745 – Banco Citibank S.A.',
        '399 – HSBC Bank Brasil S.A. – Banco Múltiplo',
        '104 – Caixa Econômica Federal',
        '389 – Banco Mercantil do Brasil S.A.',
        '453 – Banco Rural S.A.',
        '422 – Banco Safra S.A.',
        '633 – Banco Rendimento S.A.',]
        for i in range(len(Bancos)):
            Bancos[i] = (Bancos[i],Bancos[i])
        widgets = { 
            'banco_conta':  forms.Select(choices=Bancos), 
            }
        labels = {
            'banco_conta':'Banco:',
            'agencia_conta':'Agencia:',
            'num_conta':'Conta:',
            'apelido_conta':'*Apelido da conta:',
        }

class VeicForm(ModelForm):
    class Meta:
        model = Veiculo
        fields = [
            'fabricante_veic',
            'modelo_veic',
            'placa_veic',
            'cor_veic',
            'capacidade_veic',
            'apelido_veic',
        ]
        Veiculos = ['Acura','Agrale','Alfa Romeo','Asia','AM General','Aston Martin','Audi','Adly','Aprilia','Atala','Amazonas','Austin','Apperson','Ashok Leyland','Alpina','Adler','Ascari','Abarth','Autobianchi','Aixam','AMG','AZLK','Avtokam','ACMAT','Albion','Argyle','Askam','Aspark Owl','A.D. Tramontana','BMW','Buggy','BRM','Bugre','Bugatti','Bentley','Buick','Baker','Biddle','Bajaj','Bitter','Borgward','Briggs','Belsize','Bertone','Bianchi','Brilliance','Byd Auto','Baic','Birrana','Brabus','Birkin','Bailey','Chevrolet','Cadillac','CBT','Chana','Changan','Chery','Chrysler','Citroen','Cross Lander','Chinkara','Caterham','Chater-Lea','Covini','Caresto','Changhe','Cizeta','Daewoo','Daihatsu','Dodge','De Tomaso','Ducati','Delorean','DKW','DR Motor','De La Chapelle','Dongfeng','DRB','Derways','Dragon Motors','Daimler','Datsun','Dacia','DoniRosset','Effa','Engesa','Envemo','Eicher','Esther','Elfin','Eagle','Eterniti','ERF','Elva','Ferrari','FIAT','Fibravan','Ford','Foton','Fyber','Force','Fornasari','Fisker','Freightliner','Faw','FPV','Facel Vega','Fioravanti','Franklin','Geely','GM','Great Wall','Gurgel','GMC','Gorhan','Gumpert','Ginetta','Geo','GAC','Giocattolo','Gaz','Genesis','Gillet','Grinnall','Hafei','Honda','Hyunday','Harley-Davidson','Husqvarna','Hummer','Hindustan','Hongqi','Holden','HSV','Hino','Harper','Hero Motors','Isuzu','Iveco','ICML Motors','Infiniti','Isdera','Invicta','Isotta Fraschini','Irizar','Innoson','Ivema','Jeep','Jaguar','JPX','Jinbei','JAC','James & Browne','Josse Car','Jiefang','Kia','Kahena','Kasinski','KTM','Keinath','Koenigsegg','Kamaz','Kawasaki','Karma','Kaz','Karrier','Kantanka','Kiira','Lada','Lamborghini','Lancia','Land Rover','Lexus','Lifan','Lotus','Lobini','Lincoln','Laferrari','Ligier','Lagonda','Lucid','Luxgen','Laraki','Mahindra','Maserati','Matra','MG','Mazda','Mclaren','Mercedes-Benz','Mercury','Miura','Mini','Mitsubishi','Maruti','Mitsuoka','Maybach','Microcar','Mack','Moskvich','Marussia','MAN','Marcos','Mazzanti','Morris','Mustang','MAZ','Mobius','Nissan','Navistar','Nota','Nami Okhta','Noble','Opel','Oldsmobile','Ohta Jidosha','Otosan','ÖAF','Peugeot','Plymouth','Pontiac','Porsche','Puma','Polaris','Panoz','Premier','Prince','Pagani','Panhard','PGO','Pyeonghwa','Proto','Perodua','Paccar','Pininfarina','Paramount Automotive','Proforce','Perana','Qvale','Qoros','RAM','Rely','Rover','Renault','Rolls-Royce','Rootes','Rambler','Riley','Rossion','RUF','Ronart','Rimac','SAAB','Saturn','SEAT','Shineray','Smart','Ssangyong','Subaru','Suzuki','Sundown','Sino Truck','Scania','Scion','Saic','Spetsteh','Skoda','Shelby','Saleen','Sterling','Saroukh El-jamahiriya','Shaka Nynya','TAC','Toyota','Troller','Tata','Triumph','Traxx','Tesla','Tatra','Trion','The Turtle','Tropical','UAZ','Unimog','UEV','Ultima','Uri','URO','Volvo','Volkswagen','Venturi','Volga','Vauxhall','Vector','Venucia','Vulcan','Vomag','Vanaja','Wake','Walk','Wuyang','Wheego','Willeme','Wallys','Xbasiralsanayei','XBehnam','Yamaha','Yale','Yuna','Yugo','Yulon','Yarovit','Yorkshire','Zimmer','Zyle Daewoo','Zotye','Zil','Zastava','Zolfe','Zenvo','Zender','Zwicky',]
        Cores=['Amarelo','Azul','Bege','Branca','Cinza','Dourada','Grena','Laranja','Marrom','Prata','Preta','Rosa','Roxa','Verde','Vermelha','Fantasia',]
        for i in range(len(Veiculos)):
            Veiculos[i] = (Veiculos[i],Veiculos[i])
        for i in range(len(Cores)):
            Cores[i] = (Cores[i],Cores[i])
        widgets = { 
            'fabricante_veic':  forms.Select(choices=Veiculos), 
            'cor_veic': forms.Select(choices=Cores), 
            }
        labels = {
            'fabricante_veic':'Fabricante:',
            'modelo_veic':'Modelo:',
            'placa_veic':'Placa:',
            'cor_veic':'Cor:',
            'capacidade_veic':'Capacidade de passageiros:',
            'apelido_veic':'*Apelido do veículo:',
        }