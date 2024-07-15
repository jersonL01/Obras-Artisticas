from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from captcha.fields import CaptchaField
from django_recaptcha.fields import ReCaptchaField
# EL TEMPLATE DEL FORMULARIO

class ProductoForm(ModelForm):
    
    #captcha = CaptchaField()
    captcha = ReCaptchaField()
   
    class Meta:
        model = Producto
        #fields = ['nombre', 'precio','stock', 'descripcion', 'tipo']
        fields = '__all__'

class RegistroUsuarioForm(UserCreationForm):
    captcha = ReCaptchaField()
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']
    
  