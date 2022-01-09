from django import forms

from django.core.exceptions import ValidationError

from .models import curso, disciplina

LISTA_DISCIPLINAS = (('Elec','Electronica'),('Rep','Reposteria'),('Lit','Literatura'))

class CursoForm(forms.ModelForm):
	# titulo = forms.CharField(help_text="Ingrese un titulo")
	# descripcion = forms.CharField(widget=forms.Textarea,help_text="Ingrese una descripcion")
	# disciplina = forms.CharField(help_text="Ingrese una disciplina")
	# avatar = forms.ImageField()
	# precio = forms.DecimalField(widget=forms.NumberInput(attrs={'step':0.02}))
	# calificacion = forms.DecimalField(widget=forms.NumberInput(attrs={'step':0.5}))
	# alumnos = forms.IntegerField()
	# profesor = forms.CharField(help_text="Ingrese un profesor para el curso")

	class Meta:
		model = curso
		# fields = "__all__"
		fields = ['titulo','descripcion','disciplina','avatar','precio']
		
		widgets = {
				'titulo':forms.TextInput(attrs={'class':'form-control'}),
				'descripcion':forms.Textarea(attrs={'class':'form-control'}),
				'disciplina':forms.Select(choices=disciplina.objects.all(),attrs={'class':'form-control'}),
				'avatar':forms.ClearableFileInput(attrs={'class':'form-control'}),
				'precio':forms.NumberInput(attrs={'step':0.01,'class':'form-control'}),
				# 'profesor':forms.TextInput(attrs={'class':'form-control'})
		}

		labels = {
				'titulo':'Titulo del curso',
				'descripcion':'Descripcion del curso',
				'disciplina':'Disciplina del curso',
				'avatar':'Logo del curtso',
				'precio':'Precio de venta',
				# 'profesor':'Creador del curso'	
		}

	def clean_calificacion(self):
		calif = self.cleaned_data['calificacion']
		if calif <0 or calif > 5:
			raise ValidationError('La calificacion debe estar entre 0 y 5')
		return calif

class DisciplinaForm(forms.ModelForm):

	class Meta:
		model = disciplina
		fields = ['nombre']
		
		widgets = {
				'nombre':forms.TextInput(attrs={'class':'form-control'}),
		}

		labels = {
				'nombre':'Nombre de la Disciplina',
		}
