from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroConMail(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Campo requerido y debe ser valido, hasta 254 caracteres como maximo')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('El email ya existe, ingresa uno nuevo')
        return email

from .models import perfil
from django.core.exceptions import ValidationError

LISTA_SEXOS = (('F','Femenino'),('M','Masculino'))

class PerfilForm(forms.ModelForm):

    class Meta:
        model = perfil
        fields = ('nombre','avatar','biografia','recibemails','sexo','nacimiento')
    
        widgets = {'nombre': forms.TextInput(attrs={'class':'form-control'}),
               'avatar':forms.ClearableFileInput(attrs={'class':'form-control'}),
               'biografia': forms.Textarea(attrs={'class':'form-control'}),
               'recibemails':forms.CheckboxInput(),
               'sexo':forms.RadioSelect(choices=LISTA_SEXOS),
               'nacimiento': forms.DateInput(attrs={'class':'form-control'},format="%m/%d/%y")
               }

        labels = {'nombre':'Nombre del visitante',
                    'avatar':'Avatar del visitante',
                    'biografia':'Experiencia',
                    'recibemails':'Recibe Mails'
                    }

    # def clean_nombre(self):
    #     nombre = self.cleaned_data['nombre']
    #     if nombre != 'Hola':
    #         raise ValidationError('El nombre debe ser Hola')
    #     return nombre                    

    # def clean_biografia(self):
    #     biografia = self.cleaned_data['biografia']
    #     if biografia != 'Como estas':
    #         raise ValidationError('La biografia debe ser Como estas')
    #     return biografia                            

    def clean(self):
        data = self.cleaned_data
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        if nombre != "Hola" and  descripcion != "Como estas":
            raise ValidationError('El nombre debe ser Hola y la biografia como estas')
