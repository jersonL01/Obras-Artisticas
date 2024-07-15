
from datetime import datetime
from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class TipoObras(models.Model):
    tecnica = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.tecnica


class Producto(models.Model):
    codigo_producto = models.IntegerField(primary_key=True, null=False)
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.CharField(max_length=100)
    historia = models.CharField(max_length=100)
    imagen = CloudinaryField('imagen')
    tecnica = models.ForeignKey(TipoObras, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.nombre

#imagen = models.ImageField(null=True, blank=True) 
class Carrito(models.Model):
    codigo_producto = models.IntegerField()
    nombre_producto = models.CharField(max_length=50)
    precio_producto = models.IntegerField()
    cantidad = models.IntegerField()
    total = models.IntegerField()
    imagen = CloudinaryField('imagen')
    usuario_producto = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.cantidad} of {self.nombre_producto}"

#imagen = models.ImageField('imagen')    
class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=50)
   

    def __str__(self):
        return self.tipo
    

class Usuario(models.Model):
    codigo_usuario = models.IntegerField(primary_key=True)
    nombre_usuario = models.CharField(max_length=30)
    correo = models.CharField(max_length=20)
    telefono = models.CharField(max_length=12)
    direccion = models.CharField(max_length=30)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    

    def __str__(self):
        return self.nombre_usuario



class OrdenCompra(models.Model):
    codigo_producto = models.IntegerField()
    nombre_producto = models.CharField(max_length=50)
    precio_producto = models.IntegerField()
    cantidad = models.IntegerField()
    total = models.IntegerField()
    usuario_producto = models.CharField(max_length=100)
    fecha_compra = models.DateTimeField(auto_now_add=True)  # Fecha y hora de la compra

    def __str__(self):
        return f"Orden de compra de {self.nombre_producto} por {self.usuario_producto}"


