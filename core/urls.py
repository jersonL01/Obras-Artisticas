from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('productos', ProductoViewset)

urlpatterns = [

    #API
    path('api/', include(router.urls)),
    path('universo_api/', universo_api, name="universo_api"),
    path('api_proyecto/', api_proyecto, name="api_proyecto"),




    #RUTAS
    path('', index, name="index"),
    path('about', about, name="about"),
    path('contact', contact, name="contact"),
    path('shop', shop, name="shop"),
    path('shopCompra', shopCompra, name="shopCompra"),
    path('register/', register, name="register"),
    path('panel/', panel, name="panel"),
    path('cuenta/', cuenta, name="cuenta"),
    path('pago_exitoso/', pago_exitoso, name="pago_exitoso"),
    path('account_locked/', account_locked, name="account_locked"),
    path('historial/', historial ,name="historial"),
    path('generate_pdf/', generate_pdf,name="generate_pdf"),
    path('eliminar_historial/', eliminar_historial, name='eliminar_historial'),
    path('pagado/', pagado, name='pagado'),

    #CRUD
    path('agregar/', agregar, name="agregar"),
    path('actualizar/<codigo_producto>/', actualizar, name="actualizar"),
    path('eliminar/<codigo_producto>/', eliminar, name="eliminar"),
    path('buscar/', buscar, name='buscar'),


    #CARRITO
    path('cart', cart, name="cart"),
    path('vaciar_carrito/', vaciar_carrito, name='vaciar_carrito'),
     path('eliminar_carrito/<str:codigo_producto>/', eliminar_carrito, name='eliminar_carrito'),
    path('aumentar_cantidad/<codigo_producto>/', aumentar_cantidad, name='aumentar_cantidad'),
    path('disminuir_cantidad/<codigo_producto>/', disminuir_cantidad, name='disminuir_cantidad'),
    

    #PASSWORD
   
  
]
