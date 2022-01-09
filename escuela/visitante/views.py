from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def homeView(request):
    mensaje_adicional = {'mensaje':'Este es un titulo adicional'}
    return render(request,'home1.html',mensaje_adicional)

from django.views.generic.list import ListView
from core.models import curso

class CursoListBusquedaView(ListView):

    model = curso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        criterio = self.request.GET['criterio']
        lista = None
        if criterio == '*':
            lista = curso.objects.filter(completo=True)
        elif criterio != '':
            lista = curso.objects.filter(titulo__contains=criterio, completo=True) | curso.objects.filter(descripcion__contains=criterio, completo=True)

        context['lista'] = lista

        return context

from django.views.generic.edit import CreateView
from core.models import curso
from django.urls import reverse_lazy

from core.forms import CursoForm

from django.shortcuts import HttpResponseRedirect

class CursoCreateView(CreateView):
    model = curso
    form_class = CursoForm
    template_name = 'visitante/curso_form.html'
    # fields = ['titulo','descripcion','disciplina','avatar','precio']
    # success_url = reverse_lazy('core:home')
    
    def get_success_url(self):
        return reverse_lazy('core:home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_template'] = 'Registro de un nuevo curso'
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST,request.FILES)
        User = request.user
        if form.is_valid():
            Curso = form.save(commit=False)
            Curso.profesor = User
            Curso.save()
            # Vuelve al visitante, profesor
            if User.first_name == 'm':
                User.first_name = 'p'
            elif User.first_name == 'a':
                User.first_name = 'b'
            User.save()
            return HttpResponseRedirect(self.get_success_url())
        return render(request, 'core/curso_form.html', {'form': form})


from django.views.generic.edit import UpdateView

class CursoUpdateView(UpdateView):
    model = curso
    form_class = CursoForm
    template_name_suffix = '_update_form'  
    success_url = reverse_lazy('core:en_preparacion')      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Curso = self.object
        context['titulo_template'] = 'Registro de un nuevo curso'
        context['titulo'] = Curso.titulo
        # alcances
        lista_alcances = alcance.objects.filter(curso=Curso)
        context['lista_alcances'] = lista_alcances
        # recomendaciones
        lista_recomendaciones = recomendacion.objects.filter(curso=Curso)
        context['lista_recomendaciones'] = lista_recomendaciones
        # capitulos
        lista_capitulos = capitulo.objects.filter(curso=Curso)
        context['lista_capitulos'] = lista_capitulos
        return context

from django.views.generic.edit import DeleteView

class CursoDeleteView(DeleteView):
    model = curso
    success_url = reverse_lazy('core:en_preparacion')

from django.views.generic.detail import DetailView
from django.contrib.auth.models import AnonymousUser

class CursoDetailView(DetailView):

    model = curso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estado = 'n'
        if not self.request.user == AnonymousUser():
            estado = 's'
        context['estado'] = estado
        context['reviews'] = 60
        # alcances
        context['lista_alcances'] = alcance.objects.filter(curso=self.object)
        # recomendaciones
        context['lista_recomendaciones'] = recomendacion.objects.filter(curso=self.object)
        return context    

# Alcance

from .models import alcance
from .forms import AlcanceForm
from core.models import curso
from django.urls import reverse_lazy

class AlcanceCreateView(CreateView):
    model = alcance
    form_class = AlcanceForm

    def get_success_url(self, *args):
        return reverse_lazy('visitante:editar_curso', args=[args[0].id]) + '?correcto=ok'

    def get_context_data(self):
        context = super(AlcanceCreateView, self).get_context_data()
        Curso = curso.objects.get(id=self.request.GET['curso_id'])
        context['curso'] = Curso
        context['titulo_template'] = 'Nuevo alcance'
        context['titulo'] = Curso.titulo
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST,request.FILES)
        Curso = curso.objects.get(id = request.POST['curso_id'])
        if form.is_valid():
            Alcance = form.save(commit=False)
            Alcance.curso = Curso
            Alcance.save()
            return HttpResponseRedirect(self.get_success_url(Curso))
        return render(request, 'visitante/alcance_form.html', {'form': form,'curso':Curso})        

class AlcanceUpdateView(UpdateView):
    model = alcance
    form_class = AlcanceForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('visitante:editar_curso', args=[self.request.POST['curso_id']]) + '?correcto=ok'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = curso.objects.get(id= self.request.GET['curso_id'])
        context['titulo_template'] = 'Edicion de alcance'
        context['titulo'] = context['curso'].titulo

        return context

class AlcanceDeleteView(DeleteView):
    model = alcance

    def get_success_url(self):
        return reverse_lazy('visitante:editar_curso', args=[self.request.GET['curso_id']]) + '?correcto=ok'

# Recomendacion

from .models import recomendacion
from .forms import RecomendacionForm

class RecomendacionCreateView(CreateView):
    model = recomendacion
    form_class = RecomendacionForm

    def get_success_url(self, *args):
        return reverse_lazy('visitante:editar_curso', args=[args[0].id]) + '?correcto=ok'

    def get_context_data(self):
        context = super(RecomendacionCreateView, self).get_context_data()
        Curso = curso.objects.get(id=self.request.GET['curso_id'])
        context['curso'] = Curso
        context['titulo_template'] = 'Nueva recomendacion'
        context['titulo'] = Curso.titulo
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST,request.FILES)
        Curso = curso.objects.get(id = request.POST['curso_id'])
        if form.is_valid():
            Recomendacion = form.save(commit=False)
            Recomendacion.curso = Curso
            Recomendacion.save()
            return HttpResponseRedirect(self.get_success_url(Curso))
        return render(request, 'visitante/recomendacion_form.html', {'form': form,'curso':Curso})        

class RecomendacionUpdateView(UpdateView):
    model = recomendacion
    form_class = RecomendacionForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('visitante:editar_curso', args=[self.request.POST['curso_id']]) + '?correcto=ok'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = curso.objects.get(id= self.request.GET['curso_id'])
        context['titulo_template'] = 'Edicion de recomendacion'
        context['titulo'] = context['curso'].titulo

        return context

class RecomendacionDeleteView(DeleteView):
    model = recomendacion

    def get_success_url(self):
        return reverse_lazy('visitante:editar_curso', args=[self.request.GET['curso_id']]) + '?correcto=ok'


# Capitulos

from .models import capitulo
from .forms import CapituloForm

class CapituloCreateView(CreateView):
    model = capitulo
    form_class = CapituloForm

    def get_success_url(self, *args):
        return reverse_lazy('visitante:editar_curso', args=[args[0].id]) + '?correcto=ok'

    def get_context_data(self):
        context = super(CapituloCreateView, self).get_context_data()
        Curso = curso.objects.get(id=self.request.GET['curso_id'])
        context['curso'] = Curso
        context['titulo_template'] = 'Nueva capitulo'
        context['titulo'] = Curso.titulo
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST,request.FILES)
        Curso = curso.objects.get(id = request.POST['curso_id'])
        if form.is_valid():
            Capitulo = form.save(commit=False)
            Capitulo.curso = Curso
            Capitulo.save()
            return HttpResponseRedirect(self.get_success_url(Curso))
        return render(request, 'visitante/capitulo_form.html', {'form': form,'curso':Curso})        

class CapituloUpdateView(UpdateView):
    model = capitulo
    form_class = CapituloForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        curso_id = self.object.curso.id
        return reverse_lazy('visitante:editar_curso', args=[curso_id]) + '?correcto=ok'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = self.object.curso
        context['titulo_template'] = 'Edicion de capitulo'
        context['titulo'] = context['curso'].titulo
        # Temas
        lista_temas = tema.objects.filter(capitulo=self.object)
        context['lista_temas'] = lista_temas
        return context

class CapituloDeleteView(DeleteView):
    model = capitulo

    def get_success_url(self):
        curso_id = self.object.curso.id
        return reverse_lazy('visitante:editar_curso', args=[curso_id]) + '?correcto=ok'



# Temas de los capitulos

from .models import tema
from .forms import TemaForm

class TemaCreateView(CreateView):
    model = tema
    form_class = TemaForm

    def get_success_url(self, *args):
        return reverse_lazy('visitante:editar_capitulo', args=[args[0].id]) + '?curso_id=' + str(args[0].curso.id) + '&correcto=ok'

    def get_context_data(self):
        context = super(TemaCreateView, self).get_context_data()
        Capitulo = capitulo.objects.get(id=self.request.GET['capitulo_id'])
        context['capitulo'] = Capitulo
        context['titulo_template'] = 'Nuevo Tema'
        context['titulo'] = Capitulo.nombre + ' ' + Capitulo.curso.titulo
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST,request.FILES)
        capitulo_post = capitulo.objects.get(id = request.POST['capitulo_id'])
        if form.is_valid():
            Tema = form.save(commit=False)
            Tema.capitulo = capitulo_post
            Tema.save()
            return HttpResponseRedirect(self.get_success_url(capitulo_post))
        return render(request, 'visitante/capitulo_form.html', {'form': form,'capitulo':capitulo_post})        

class TemaUpdateView(UpdateView):
    model = tema
    form_class = TemaForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        Capitulo = capitulo.objects.get(id=self.request.POST['capitulo_id'])
        return reverse_lazy('visitante:editar_capitulo', args=[Capitulo.id]) + '?curso_id=' + str(Capitulo.curso.id) + '&correcto=ok'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Capitulo = capitulo.objects.get(id= self.request.GET['capitulo_id'])
        context['capitulo'] = Capitulo
        context['titulo_template'] = 'Edicion de Tema'
        context['titulo'] = Capitulo.nombre + ' ' + Capitulo.curso.titulo
        # Detalle
        # context['lista_detalles'] = detalle.objects.filter(tema = self.object)   
        lista = []
        for obj in detalle.objects.filter(tema = self.object):
            if obj.imagen != '':
                lista.append([obj,'imagen'])
            elif obj.media != '':
                lista.append([obj,'media'])
            elif obj.texto != '':
                lista.append([obj,'texto'])
            else:
                lista.append([obj,''])
        context['lista_detalles'] = lista
        return context

class TemaDeleteView(DeleteView):
    model = tema

    def get_success_url(self):
        curso_id =capitulo.objects.get(id=self.request.GET['capitulo_id']).curso.id
        return reverse_lazy('visitante:editar_capitulo', args=[self.request.GET['capitulo_id']]) + '?curso_id=' + str(curso_id) + '&correcto'

# Detalles para los temas

from .models import detalle
from .forms import DetalleForm

import os.path

class DetalleCreateView(CreateView):
    model = detalle
    form_class = DetalleForm

    def get_success_url(self, *args):
        return reverse_lazy('visitante:editar_tema', args=[args[0].id]) + '?capitulo_id=' + str(args[0].capitulo.id) + '&correcto=ok'

    def get_context_data(self):
        context = super(DetalleCreateView, self).get_context_data()
        Tema = tema.objects.get(id=self.request.GET['tema_id'])
        context['tema'] = Tema
        context['titulo_template'] = 'Nuevo Detalle'
        context['titulo'] = Tema.nombre + ' ' + Tema.capitulo.nombre
        return context

    def post(self,request,*args,**kwargs):
        videos = ['.mp4','.ogv','.webM']
        audios = ['.mp3','.wav']
        textos = ['.txt','.odt','.docs','.pdf']
        form = self.form_class(request.POST,request.FILES)
        tema_post = tema.objects.get(id = request.POST['tema_id'])
        if form.is_valid():
            nombre = request.FILES.get('media')
            Detalle = form.save(commit=False)
            Detalle.nombrearchivo = nombre
            # nombre, extension = os.path.splitext(os.getcwd() + '/media/visitante/' + str(nombre))
            extension = os.path.splitext(os.getcwd() + '/media/visitante/' + str(nombre))[1]
            # videos
            for tipo in videos:
                if tipo == extension:
                    Detalle.tipoarchivo = 'v'
                    break
            # audios
            for tipo in audios:
                if tipo == extension:
                    Detalle.tipoarchivo = 'a'
                    break
            # textos
            for tipo in textos:
                if tipo == extension:
                    Detalle.tipoarchivo = 't'
                    break
            if Detalle.tipoarchivo == 'n':
                Detalle.media = None
                Detalle.nombrearchivo = ''

            Detalle.tema = tema_post
            Detalle.save()
            return HttpResponseRedirect(self.get_success_url(tema_post))
        return render(request, 'visitante/detalle_form.html', {'form': form,'tema':tema_post})        

class DetalleUpdateView(UpdateView):
    model = detalle
    form_class = DetalleForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        Tema = tema.objects.get(id=self.request.POST['tema_id'])
        return reverse_lazy('visitante:editar_tema', args=[Tema.id]) + '?capitulo_id=' + str(Tema.capitulo.id) + '&correcto=ok'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Tema = tema.objects.get(id= self.request.GET['tema_id'])
        context['tema'] = Tema
        context['titulo_template'] = 'Edicion de Detalle'
        context['titulo'] = self.object.nombre + ' ' + self.object.tema.nombre

        return context

    def post(self,request,*args,**kwargs):
        videos = ['.mp4','.ogv','.webM']
        audios = ['.mp3','.wav']
        textos = ['.txt','.odt','.docs','.pdf']
        self.object = self.get_object()
        form = self.get_form()
        Detalle = form.save(commit=False)
        nombre = request.FILES.get('media')
        Detalle.nombrearchivo = nombre
        # nombre, extension = os.path.splitext(os.getcwd() + '/media/visitante/' + str(nombre))
        extension = os.path.splitext(os.getcwd() + '/media/visitante/' + str(nombre))[1]
        # videos
        for tipo in videos:
            if tipo == extension:
                Detalle.tipoarchivo = 'v'
                break
        # audios
        for tipo in audios:
            if tipo == extension:
                Detalle.tipoarchivo = 'a'
                break
        # textos
        for tipo in textos:
            if tipo == extension:
                Detalle.tipoarchivo = 't'
                break
        if Detalle.tipoarchivo == 'n':
            Detalle.media = None
            Detalle.nombrearchivo = ''
        Detalle.save()
        return HttpResponseRedirect(self.get_success_url())


class DetalleDeleteView(DeleteView):
    model = detalle

    def get_success_url(self):
        Tema =tema.objects.get(id=self.request.GET['tema_id'])
        return reverse_lazy('visitante:editar_tema', args=[Tema.id]) + '?capitulo_id=' + str(Tema.capitulo.id) + '&correcto'
