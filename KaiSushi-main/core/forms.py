from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Bowl,Desayuno,Almuerzo,Handroll,HandrollReady, Comanda

#se define clase forms
#se asigna tipo de objeto y declarar parametros del formulario


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price',)

class BowlForm(forms.ModelForm):

    class Meta:
        model = Bowl
        fields = ('proteina', 'base','salsa1','salsa2','extra1','extra2','extra3',
        'extra4','extra5','extra6','extra7','extra8','extra9','extra10',)


class DesayunoForm(forms.ModelForm):

    class Meta:
        model = Desayuno
        fields = ('queso', 'proteina','vegetal1','vegetal2')

class AlmuerzoForm(forms.ModelForm):

    class Meta:
        model = Almuerzo
        fields = ('proteina', 'agregado')

class HandrollForm(forms.ModelForm):

    class Meta:
        model = Handroll
        fields = ('proteina1','proteina2','proteina3','vegetal1','vegetal2','vegetal3')


class ComentForm(forms.ModelForm):
    
    class Meta:
        model = Comanda
        fields = ('coments',)

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

