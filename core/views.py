
import json
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import ProductoForm, RegistroUsuarioForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework import viewsets
import requests
from .serializers import ProductoSerializer,TipoProductoSerializer
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from xhtml2pdf import pisa  
from django.template.loader import get_template


#PERMISOS DE USUARIO
def grupo_requerido(nombre_grupo):
    def decorator(view_fuc):
        @user_passes_test(lambda user: user.groups.filter(name=nombre_grupo).exists())
        def wrapper(request, *args, **kwargs):
            return view_fuc(request, *args, **kwargs)
        return wrapper
    return decorator

# @grupo_requerido('admin')


# SE ENCARGA DE MOSTRAR EN LA VISTA LOS DATOS
class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()  
    serializer_class = ProductoSerializer


def universo_api(request):

    respuesta = requests.get('https://rickandmortyapi.com/api/character')
    respuesta1 = requests.get('https://digimon-api.vercel.app/api/digimon')


    aux = respuesta.json()
    personajes = aux['results']
    digimon = respuesta1.json()

    # PAGINATOR
    paginator = Paginator(digimon, 3) # CANTIDAD DE DATOS A MOSTRAR
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    data ={
        'personajes' : personajes,
        'digimon' : digimon,
        'page_obj' : page_obj,
    }
    

    return render(request, 'core/universo_api.html', data)


@login_required
def api_proyecto(request):

    #REALIZAMOS LA SOLICITUD AL API
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    respuesta2 = requests.get('https://mindicador.cl/api')
    #TRANSFROMAMOS EL JSON PARA LEERLO
    productos = respuesta.json()
    usdt = respuesta2.json()

    data = {
        'listaProductos' : productos,
        'usdt' : usdt, 
        
    }
    return render(request, 'core/api_proyecto.html', data)


# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')


def account_locked(request):
    return render(request, 'core/account_locked.html')

@login_required
def cart(request):
    return render(request, 'core/cart.html')

@login_required
def cuenta(request):
    return render(request, 'core/crud/cuenta.html')
def register(request):
    
    data ={
        'form' : RegistroUsuarioForm()
    }
    
    if request.method == 'POST':
        formulario = RegistroUsuarioForm(data = request.POST)
        if formulario.is_valid():
            formulario.save()
            #user = authenticate(username=formulario.cleaned_data["username"], password = formulario.cleaned_data["password1"])
            #login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="index")
        data ["form"] = formulario

    return render(request, 'registration/register.html', data)

@login_required
def panel(request):
    ProductoAll = Producto.objects.all() 
    data = {
        'listaProductos' : ProductoAll

    }

    return render(request, 'core/crud/panel.html', data)



#CRUD

def shop(request):
    ProductoAll = Producto.objects.all() 
    data = {
        'listaProductos' : ProductoAll

    }

    return render(request, 'core/shop.html', data)

@login_required
def shopCompra(request):
    ProductoAll = Producto.objects.all() 
    data = {
        'listaProductos' : ProductoAll,
       
    }

    if request.method == 'POST':
        codigo_producto = request.POST.get('codigo_producto')
        user = request.user.get_username()
        nombre_producto = request.POST.get('nombre')
        precio = request.POST.get('precio')
        producto = Producto.objects.get(codigo_producto=codigo_producto)
        producto.stock -= 1
        producto.save()

        if Carrito.objects.filter(codigo_producto=codigo_producto, usuario_producto=user, nombre_producto=nombre_producto).exists():
            carrito = Carrito.objects.get(codigo_producto=codigo_producto, usuario_producto=user, nombre_producto=nombre_producto)
            carrito.cantidad += 1
            carrito.total += int(precio)
            carrito.save()
        else:
            carrito = Carrito()
            carrito.codigo_producto = codigo_producto
            carrito.nombre_producto = nombre_producto
            carrito.precio_producto = precio  
            carrito.total = precio
            carrito.cantidad = 1
            carrito.usuario_producto = user
            carrito.imagen = request.POST.get('imagen')
            carrito.save()

    return render(request, 'core/shopCompra.html', data)

#AGREGAR
@login_required
def agregar(request):

    data = {
        'form' : ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Guardado correctamente"
            
        else:
            data['form'] = formulario 
    return render (request, 'core/crud/agregar.html', data)

#MODIFICAR
@login_required
def actualizar(request,codigo_producto):
    producto = Producto.objects.get(codigo_producto=codigo_producto)
    data = {
        'form' :ProductoForm(instance=producto)
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST,instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "actualizado correctamente")
            data['mensaje'] = "Actualizado correctamente" 
        else:
            data['form'] = formulario
        
    
    return render(request, 'core/crud/actualizar.html', data)

#ELIMINAR
@login_required
def eliminar(request,codigo_producto):
    producto = Producto.objects.get(codigo_producto=codigo_producto)
    producto.delete()

    return redirect(to="panel")
#BUSCAR
@login_required
def buscar(request):
    query = request.GET.get('q', '')
    productos = []
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    
    context = {
        'productos': productos,
        'query': query,
    }
    return render(request, 'core/buscar.html', context)

@login_required
def cart(request):
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']

    carrito = Carrito.objects.filter(usuario_producto=request.user.username)  # Filtra por usuario_producto
    total_precio = 0
    total_iva = 0
    total_final = 0  # Inicializa total_final antes del bucle

    for item in carrito:
        total_precio += item.total
        total_iva += round(item.total * 0.19)  # Calcula el IVA del 19%
        total_final = round((total_precio + total_iva) / valor_usd, 2)
        total_final = str(total_final).replace(",", ".")

    data = {
        'listaCarrito': carrito,
        'total_precio': total_precio,
        'total_iva': total_iva,
        'total_final': total_final,
    }

    return render(request, 'core/cart.html', data)


@login_required
#FUNCIONALIDAD DEL CARRITO
def vaciar_carrito(request):
    # Obtener todos los elementos del carrito para el usuario actual
    carrito_usuario = Carrito.objects.filter(usuario_producto=request.user)

    # Restaurar el stock de cada producto en el carrito
    for item in carrito_usuario:
        producto = Producto.objects.get(codigo_producto=item.codigo_producto)
        producto.stock += item.cantidad
        producto.save()

    # Eliminar todos los elementos del carrito del usuario actual
    carrito_usuario.delete()

    return redirect('cart')


@login_required
#Eliminar Carro
def eliminar_carrito(request, codigo_producto):
    # Obtén el ítem del carrito
    aux = get_object_or_404(Carrito, codigo_producto=codigo_producto)
    
    producto = get_object_or_404(Producto, codigo_producto=aux.codigo_producto)
    
    # Devuelve el stock del producto
    producto.stock += aux.cantidad
    producto.save()
    
    # Elimina el ítem del carrito
    aux.delete()
    
    # Redirige al carrito
    return redirect('cart')

#Aumentar Carro
@login_required
def aumentar_cantidad(request, codigo_producto):
    aux = get_object_or_404(Carrito, codigo_producto=codigo_producto)

    producto = get_object_or_404(Producto, codigo_producto=aux.codigo_producto)
    
    if producto.stock > 0:
        # Aumenta la cantidad del ítem del carrito
        aux.cantidad += 1
        aux.total = aux.cantidad * aux.precio_producto  # Actualiza el total
        aux.save()
        
        # Reduce el stock del producto
        producto.stock -= 1
        producto.save()
    return redirect('cart')

#Restar Carrito
@login_required
def disminuir_cantidad(request, codigo_producto):

    aux = get_object_or_404(Carrito, codigo_producto=codigo_producto)
    if aux.cantidad > 1:
        aux.cantidad -= 1
        aux.total = aux.cantidad * aux.precio_producto  
        aux.save()
        producto = get_object_or_404(Producto, codigo_producto=aux.codigo_producto)
        producto.stock += 1  #
    else:
        eliminar_carrito(request, codigo_producto)  
    return redirect('cart')


def pago_exitoso(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_data = data.get('paymentData')
            
            for item in payment_data:
                nueva_orden = OrdenCompra.objects.create(
                    codigo_producto=item.get('codigo_producto'),
                    nombre_producto=item.get('nombre_producto'),
                    precio_producto=item.get('precio_producto'),
                    cantidad=item.get('cantidad'),
                    total=item.get('total'),
                    usuario_producto=item.get('usuario_producto')
                )
            
            # Eliminar el contenido del carrito del usuario
            Carrito.objects.filter(usuario_producto=item.get('usuario_producto')).delete()
            
            return JsonResponse({'mensaje': 'Pago registrado correctamente'}, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required 
def historial(request):
    ordenes = OrdenCompra.objects.filter(usuario_producto=request.user.username)
    
    data = {
        'ordenes': ordenes
    }
    
    return render(request, 'core/historial.html', data)


def eliminar_historial(request):
    if request.method == 'POST':
        # Obtener todas las órdenes de compra del usuario actual y eliminarlas
        OrdenCompra.objects.filter(usuario_producto=request.user.username).delete()
        
        messages.success(request, 'Historial eliminado correctamente.')
        return redirect('historial')
    
    # Si se accede directamente a esta vista por GET u otro método, redireccionar a una página de error o manejarlo adecuadamente
    return redirect('historial')  # Redirigir de vuelta al historial después de la eliminación
def generate_pdf(request):
    # Obtener las órdenes de compra del usuario actual
    ordenes = OrdenCompra.objects.filter(usuario_producto=request.user.username)
 

    # Obtener la plantilla HTML para el PDF
    template_path = 'core/generate_pdf.html'
    template = get_template(template_path)
    
    # Renderizar la plantilla con los datos de las órdenes de compra
    context = {'ordenes': ordenes}
    html = template.render(context)
    
    # Crear un objeto HttpResponse con el contenido HTML renderizado
    response = HttpResponse(content_type='application/pdf' )
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    
    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Si falla la creación del PDF, regresar un error
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF: %s' % html )
    
    return response

def pagado(request):
    return render(request, 'core/pagado.html')
