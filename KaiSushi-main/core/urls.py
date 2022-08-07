from django.urls import path
#se importa todo de views
from . import views
from django.conf import settings
from django.conf.urls.static import static


#se asigna ruta, se toma funcion de views y se le da nombre
urlpatterns = [

    #path con render de template


    path('', views.tienda, name="Tienda"),
    path('confirm/',views.Confirm,name='confirm'),
    path('kitchen/',views.Kitchen,name='kitchen'),
    path('kitchenall/',views.KitchenAll,name='kitchenAll'),
    path('listahc/', views.ListaHC, name='listhc'),
    path('listakai/', views.ListaKai, name='listkai'),
    path('listasell/', views.ListaSell, name='listsell'),

    #formularios
    path('registros/',views.registros,name='registros'),
    path('newbowl/',views.NewBowl,name='newbowl'),
    path('newalmuerzo/',views.NewAlmuerzo,name='newalmuerzo'),
    path('newhandroll/',views.NewHandroll,name='newhandroll'),
    path('newdesayuno/',views.NewDesayuno,name='newdesayuno'),


    #ruta de funciones (sin rendear template)

    #Funciones de carrito
    path('agregar/<int:producto_id>/<str:typ>/', views.agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', views.restar_producto, name="Sub"),
    #path('restarhc/<int:producto_id>/', views.restar_producto, name="SubHC"),
    path('limpiar/', views.limpiar_carrito, name="CLS"),  
    path('tokitchen/',views.ToKitchen,name='tokitchen'),
    path('ready/<int:comd_id>',views.Ready,name='ready'),

    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
   path("logout", views.logout_request, name= "logout"),
   
    #no se estan usando
    path('listaproducto/', views.ListaProducto, name='listproduct'),
    path('nuevoproducto/', views.NuevoProducto, name='newproduct'),
    path('modificarproducto/<int:id>', views.Update, name='updateproduct'),
    path('eliminarproducto/<int:id>', views.EliminarProducto, name='deleteproduct'),
]   