from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('nova_carona/', views.create_carona, name='create_carona'),
     path('minhas_caronas/', views.minhas_caronas, name='minhas_caronas'), 
     path('minhas_caronas/<int:carona_id>/', views.detail_carona_condutor, name='detail_carona_condutor'), 
     path('minhas_caronas/<int:carona_id>/aceitar_solicitacao/<int:carona_passageiros_id>/', views.aceitar_solicitacao, name='aceitar_solicitacao'), 
     path('minhas_caronas/<int:carona_id>/update', views.update_carona, name='update_carona'),
     path('minhas_caronas/<int:carona_id>/delete', views.delete_carona, name='delete_carona'),
     path('<int:carona_id>/', views.detail_carona_passageiro, name='detail_carona_passageiro'), 
     path('buscar_carona/', views.search_carona, name='search_carona'),
     path('<int:carona_id>/reservar', views.reservar_carona, name='reservar_carona'),
     path('reservar/<int:carona_passageiros_id>/pagamento', views.pagamento_cartao, name='pagamento_cartao'),
     path('reservar/<int:carona_passageiros_id>/cancelar', views.cancelar_reserva, name='cancelar_reserva'),
     path('minhas_caronas/<int:carona_id>/finalizar', views.finalizar_carona, name='finalizar_carona'),
     path('minhas_caronas/<int:carona_id>/<int:carona_passageiros_id>/avaliacao', views.avaliacao, name='avaliacao'),
     path('minhas_caronas/<int:carona_id>/<int:carona_passageiros_id>/denuncia', views.denuncia, name='denuncia'),
     path('usuarios/', views.usuarios_list, name='usuarios_list'), 
     path('sem_acesso', views.sem_acesso, name='sem_acesso'),
]