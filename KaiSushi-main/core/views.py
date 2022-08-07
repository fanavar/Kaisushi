from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone
# Create your views here.
from core.Carrito import Carrito
from core.models import Producto
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .models import Product,Handroll,Article,Comanda,Selladitas,Desayuno,Almuerzo ,HandrollReady,Kai,Selladitas,Bowl
from .forms import NewUserForm,ProductForm,BowlForm,DesayunoForm,AlmuerzoForm,HandrollForm, ComentForm
from .Carrito import Carrito
from django.shortcuts import (get_object_or_404,
							render,
							HttpResponseRedirect)
from django.db.models import Q

def tienda(request):
    #Se obtiene todos los objetos de cada tipp=o
    productos = Product.objects.all()
    bowls = Bowl.objects.all()
    hc = HandrollReady.objects.all()
    al = Almuerzo.objects.all()
    des = Desayuno.objects.all()
    sell = Selladitas.objects.all()
    #se asigna a una variable lo obtenido del buscador
    queryset= request.GET.get("buscar")
    #si el campo del objeto contiene el queryset lo filtra. Distinct para que no haya conflicto con dos o mas iguales
    if queryset:
        productos = Product.objects.filter(
            Q(id__icontains = queryset)
        ).distinct()
        bowls = Bowl.objects.filter(
            Q(id__icontains = queryset)
        ).distinct()
        hc = HandrollReady.objects.filter(
            Q(id__icontains = queryset)
        ).distinct()
        al = Almuerzo.objects.filter(
            Q(id__icontains = queryset)
        ).distinct()
        des = Desayuno.objects.filter(
            Q(id__icontains = queryset)
        ).distinct()
        sell = Selladitas.objects.filter(
            Q(id__icontains = queryset)
        ).distinct()
    #Contezto de datos
    context={
        'productos':productos,
        "b":bowls,
        "hc":hc,
        "al":al,
        "des":des,
        "sell":sell
    }
    #Se retorna un render del template correspondiente a la ruta y le pasa el contexto
    return render(request, "core/tienda.html",context)

#Funcion agregar que tiene como parametro id y tipo del objeto
def agregar_producto(request, producto_id,typ):
    #Se obtiene el carrito
    carrito = Carrito(request)
    #Segun el tipo del objeto, lo obtiene por id
    if typ == 'hc':
        producto = HandrollReady.objects.get(id=producto_id)
    elif typ == 'h':
        producto = Handroll.objects.get(id=producto_id)
    elif typ == 'kai':
        producto = Kai.objects.get(id=producto_id)
    elif typ == 'al':
        producto = Almuerzo.objects.get(id=producto_id)
    elif typ == 'b':
        producto = Bowl.objects.get(id=producto_id)
    elif typ == 'des':
        producto = Desayuno.objects.get(id=producto_id)
    elif typ == 'sell':
        producto = Selladitas.objects.get(id=producto_id)
        
    else:
        producto=''
    #Se agrega objeto en carrito
    carrito.agregar(producto)
    #Redirecciona a tienda
    return redirect("Tienda")

#Funciones que ejecutan funciones de Carrito.py
def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Product.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("Tienda")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Product.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("Tienda")

# def restar_handclassic(request, producto_id):
#     carrito = Carrito(request)
#     producto = HandrollReady.objects.get(id=producto_id)
#     carrito.restar_hc(producto)
#     return redirect("Tienda")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("Tienda")


def Confirm(request):
    return render(request, 'core/confirm.html')

def ToKitchen(request):
    #Generar una comanda
    comd = Comanda()
    #si hay items en el carrito entonces lo recorre
    if request.session["carrito"].items:
        for key, value in request.session["carrito"].items():
            #Crea un nuevo articulo, asigna valor y lo guarda
            article = Article()
            article.cod=value["nombre"]
            article.name=value["nombre"]
            article.cantidad=value["cantidad"]
            article.total=value["acumulado"]
            article.save()
            comd.save()
            #agrega el articulo en la comanda
            comd.article.add(article)
            comd.save()
        #Cambia el estado de la comanda cuando pasa a cocina
        comd.cooking=True
        form=ComentForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save(commit=True)
        #Asigna hora de paso a cocina
        comd.time_to_kitchen = timezone.now()
        g=request.user.username
        comd.save()
        print(g)
        #limpia carrito
        request.session["carrito"]={}
    else:
        print('no hay carirto')

    return redirect("Tienda")
      
def Kitchen(request):
    cmd = Comanda.objects.all()
    artcl = Article.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(cmd, 6)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context={
        "cmd":users,
        "artcl":artcl,
    }
    return render(request, 'core/kitchen.html',context)

def KitchenAll(request):
    cmd = Comanda.objects.all()
    artcl = Article.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(cmd, 6)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context={
        "cmd":users,
        "artcl":artcl,
    }
    return render(request, 'core/kitchenall.html',context)

def Ready(request,comd_id):
    cmd = Comanda.objects.get(id=comd_id)
    cmd.cooking=False
    cmd.finished=True
    cmd.time_finished= timezone.now()    
    cmd.save()
    return print(request.user)


#Listar productos
def ListaProducto(request):
    p=Product.objects.all()
    context={
        "product":p,
    }
    return render(request, 'core/list_product.html',context)

def ListaHC(request):
    p=HandrollReady.objects.all()
    context={
        "product":p,
    }
    return render(request, 'core/list_hc.html',context)

def ListaKai(request):
    p=Kai.objects.all()
    context={
        "product":p,
    }
    return render(request, 'core/list_kai.html',context)

def ListaSell(request):
    p=Selladitas.objects.all()
    context={
        "product":p,
    }
    return render(request, 'core/list_sell.html',context)

def NuevoProducto(request):
    p=Product.objects.all()
    form=ProductForm(request.POST or None)
    if request.method == 'POST':
        

        if form.is_valid():
            a=form.save(commit=True)

            return HttpResponseRedirect("/listaproducto/")
        else:
            print('error')  
    context={
        "product":p,
        "form":form,
    }
    return render(request, 'core/new_product.html',context)



def Update(request,id):
    context={

    }
    obj = get_object_or_404(Product, id = id)

    form = ProductForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/listaproducto/")
    else:
        print('error')

    context["form"] = form

    return render(request, 'core/update_product.html',context)
def EliminarProducto(request,id):
    # dictionary for initial data with
    # field names as keys
    
 
    # fetch the object related to passed id
    obj = get_object_or_404(Product, id = id)
    context ={
        'product':obj
    }
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/")
 
    
    return render(request, 'core/delete_product.html',context)


def registros(request):
    bf= BowlForm()
    dsyn = DesayunoForm()
    almrz = AlmuerzoForm()
    hr = HandrollForm()
    hrcls = HandrollReady.objects.all()
    kai = Kai.objects.all()
    sll = Selladitas.objects.all()
    context={
        "bf":bf,
        "dsyn":dsyn,
        "almrz":almrz,
        "hr":hr,
        "hrcls":hrcls,
        "kai":kai,
        "sll":sll,
    }
    return render(request, 'core/registros.html',context)


def NewBowl(request):
    bf= BowlForm()
    form= BowlForm()
    form=BowlForm(request.POST or None)
    if request.method == 'POST':
        

        if form.is_valid():
            a=form.save(commit=True)
            b = agregar_producto(request,a.id, a.typ)
            return HttpResponseRedirect("/")
        else:
            print('error') 
    context={
        "bf":bf,
        "form":form,
    }
    return render(request, 'core/newbowl.html',context)

def NewAlmuerzo(request):
    form= AlmuerzoForm()
    form=AlmuerzoForm(request.POST or None)
    if request.method == 'POST':
        

        if form.is_valid():
            a=form.save(commit=True)
            b = agregar_producto(request,a.id, a.typ)
            return HttpResponseRedirect("/")
        else:
            print('error') 
    context={
        "form":form,
    }
    return render(request, 'core/newalmuerzo.html',context)


def NewHandroll(request):
    form= HandrollForm()
    form=HandrollForm(request.POST or None)
    if request.method == 'POST':
        

        if form.is_valid():
            a=form.save(commit=True)
            b = agregar_producto(request,a.id, a.typ)
            return HttpResponseRedirect("/")
        else:
            print('error') 
    context={
        "form":form,
    }
    return render(request, 'core/newhandroll.html',context)


def NewDesayuno(request):
    form= DesayunoForm()
    form=DesayunoForm(request.POST or None)
    if request.method == 'POST':
        

        if form.is_valid():
            a=form.save(commit=True)
            b = agregar_producto(request,a.id, a.typ)
            return HttpResponseRedirect("/")
        else:
            print('error') 
    context={
        "form":form,
    }
    return render(request, 'core/newdesayuno.html',context)




#Registro
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="core/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="core/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")