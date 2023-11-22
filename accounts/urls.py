from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('signup_condutor/', views.condutor_signup, name='condutor_signup'),
    path('signup_passageiro/', views.passageiro_signup, name='passageiro_signup'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/alterar', views.perfil_update, name='perfil_update'),
    path('perfil/alterar/condutor', views.perfil_update_condutor, name='perfil_update_condutor'),
    path('perfil/alterar/condutor/confirma', views.perfil_update_condutor_confirma, name='perfil_update_condutor_confirma'),
    path('perfil/alterar/confirma', views.perfil_update_confirma, name='perfil_update_confirma'),
    path('perfil/alterar_senha', views.alterar_senha, name='change_password'),
    path('perfil/<int:profile_id>/', views.admin_detail_profile, name='admin-detail-profile'),
    path('historico/', views.historico, name='historico'),
    path('historico/<int:carona_id>', views.historico_detail, name='historico_detail'),
    path('pagamento/', views.pagamento, name='pagamento'),
    path('pagamento/passageiro/<int:cart_id>', views.cart_detail, name='cart_detail'),
    path('pagamento/passageiro/alterar/<int:cart_id>', views.cart_update, name='cart_update'),
    path('pagamento/passageiro/alterar/<int:cart_id>/confirma', views.cart_update_confirma, name='cart_update_confirma'),
    path('pagamento/passageiro/apagar/<int:cart_id>', views.cart_delete, name='cart_delete'),
    path('pagamento/condutor/<int:conta_id>', views.conta_detail, name='conta_detail'),
    path('pagamento/condutor/alterar/<int:conta_id>', views.conta_update, name='conta_update'),
    path('pagamento/condutor/alterar/<int:conta_id>/confirma', views.conta_update_confirma, name='conta_update_confirma'),
    path('pagamento/condutor/apagar/<int:conta_id>', views.conta_delete, name='conta_delete'),
    path('veiculos/', views.veiculos, name='veiculos'),
    path('veiculos/<int:veic_id>', views.veic_detail, name='veic_detail'),
    path('veiculos/criar', views.criar_veiculos, name='veiculos_criar'),
    path('veiculos/apagar/<int:veic_id>', views.veic_delete, name='veic_delete'),
    path('veiculos/alterar/<int:veic_id>', views.veic_update, name='veic_update'),
    path('veiculos/alterar/<int:veic_id>/confirma', views.veic_update_confirma, name='veic_update_confirma'),
    path('pagamento/passageiro/criar', views.pagamento_passageiro, name='pagamento_passageiro'),
    path('pagamento/condutor/criar', views.conta_condutor, name='conta_condutor'),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('novos_condutores', views.novos_condutores, name='novos_condutores'),
    path('<int:profile_id>/verificar_condutor', views.verificar_condutor, name='verificar_condutor'),
]
