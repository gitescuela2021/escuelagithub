from django.shortcuts import render
from django.http import HttpResponse

from .models import curso

# Create your views here.
def homeView(request):
    lista_ultimos = curso.objects.filter(completo=True).order_by('created').reverse()[0:5]
    mejores_gratuitos = curso.objects.filter(precio=0, completo=True).order_by('alumnos').reverse()[0:5]
    print('Lista de cursos ',lista_ultimos)
    return render(request,'home.html',{'lista':lista_ultimos,'mejores_gratuitos':mejores_gratuitos})

from .forms import CursoForm

from django.http import HttpResponseRedirect
from django.urls import reverse

def NuevoCursoView(request):
    titulo_template = "Nuevo curso"
    mensaje = "Esta es la etapa inicial"
    form = CursoForm(request.FILES)
    if request.method == 'POST':
        # print('campo ',request.GET['campo'])
        form = CursoForm(request.POST, request.FILES)
        mensaje = "Todo fue exitoso"
        if form.is_valid():
            Curso = form.save(commit=False)
            Curso.profesor = request.user.username
            Curso.save()
            User = request.user
            if User.first_name == 'm':
                User.first_name = 'p'
            elif User.first_name == 'a':
                User.first_name = 'b'
            User.save()
            # Curso.alumnos = 0
            # Curso.calificacion = 0
            # calificacion = float(request.POST['calificacion'])
            # if calificacion <0 or calificacion > 5:
            #     mensaje = 'La calificacion debe estar entre 0 y 5'
            # else:
            return HttpResponseRedirect(reverse('core:home'))
        else:
            mensaje = "Ha ocurrido un error"
    return render(request, 'curso.html', {'form': form,'mensaje':mensaje,'titulo_template':titulo_template})             

from django.contrib.auth.models import AnonymousUser
from registration.models import perfil

def DetalleCursoView(request,pk):
    Curso = curso.objects.get(id=pk)
    reviews = 56
    User = request.user
    estado = 'n'
    if not request.user == AnonymousUser():
        Perfil = perfil.objects.get(user=request.user)
        estado = 's'
    return render(request,'detalle_curso.html',{'curso':Curso,'reviews':reviews,'estado':estado})

def ListaCursosBusquedaView(request):
    criterio = request.GET['criterio']
    lista = None
    if criterio == '*':
        lista = curso.objects.all()
    elif criterio != '':
        lista = curso.objects.filter(titulo__contains=criterio) | curso.objects.filter(descripcion__contains=criterio)
    return render(request,'lista_cursos_busqueda.html',{'lista':lista})

def EnPreparacionView(request):
    lista = None
    lista = curso.objects.filter(completo=False, profesor=request.user)
    return render(request,'en_preparacion.html',{'lista':lista})

def EditarCursoView(request, pk):
    mensaje = ''
    Curso = curso.objects.get(id=pk)
    titulo_template = 'Edicion del curso'
    titulo = Curso.titulo
    form = CursoForm(instance=Curso)
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES,instance=Curso)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('core:en_preparacion'))
        else:
            mensaje = "Ha ocurrido un error"
    return render(request, 'curso.html', {'form': form,'mensaje':mensaje,'titulo_template':titulo_template,'titulo':titulo})

def BorrarCursoView(request, pk):
    Curso = curso.objects.get(id=pk)
    Curso.delete()
    return HttpResponseRedirect(reverse('core:en_preparacion'))

from .models import disciplina
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

class DisciplinaListView(ListView):

    model = disciplina

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = disciplina.objects.all()
        context['lista'] = lista
        return context

from .forms import DisciplinaForm

class DisciplinaCreateView(CreateView):
    model = disciplina
    form_class = DisciplinaForm
    template_name = 'core/disciplina_form.html'
    # fields = ['titulo','descripcion','disciplina','avatar','precio']
    success_url = reverse_lazy('core:lista_disciplinas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_template'] = 'Registro de una Disciplina'
        return context

class DisciplinaUpdateView(UpdateView):
    model = disciplina
    form_class = DisciplinaForm
    template_name_suffix = '_update_form'  
    success_url = reverse_lazy('core:lista_disciplinas')      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Disciplina = self.object
        context['titulo_template'] = 'Actualizacion de la disciplina'
        context['titulo'] = Disciplina.nombre
        return context

class DisciplinaDeleteView(DeleteView):
    model = disciplina
    success_url = reverse_lazy('core:lista_disciplinas')


from .models import inscripcion

def InscripcionView(request, **kwargs):
    user = request.user
    # Busca si esta ya inscrito
    if kwargs['curso'] > 0:
        Curso = curso.objects.get(id=kwargs['curso'])
        lista = inscripcion.objects.filter(curso=Curso, alumno=user)
        if lista.count() == 0:
            Inscripcion = inscripcion()
            Inscripcion.alumno = user
            Inscripcion.curso = Curso
            Inscripcion.save()
            Curso.alumnos += 1
            Curso.save()
            if user.first_name == 'p':
                user.first_name = 'b'
            else:
                user.first_name = 'a'
            user.save()
            Perfil = perfil.objects.get(user=user)
            Perfil.alumno = True
            Perfil.save()
    lista = inscripcion.objects.filter(alumno=user)
    return render(request, 'core/inscripcion_lista.html',{'lista_inscripciones': lista})

from visitante.models import capitulo, tema,detalle

def EstudioView(request, **kwargs):
    Curso = curso.objects.get(id=kwargs['curso'])
    capitulos = []
    temas = []
    detalles = []

    for cap in capitulo.objects.filter(curso=Curso):
        capitulos.append(cap)
        for tem in tema.objects.filter(capitulo=cap):
            temas.append(tem)
            for det in detalle.objects.filter(tema=tem):
                detalles.append(det)

    contenido =[]
    for cap in capitulo.objects.filter(curso=Curso):
        contenido.append([cap,'capitulo'])
        for tem in tema.objects.filter(capitulo=cap):
            contenido.append([tem,'tema'])
            for det in detalle.objects.filter(tema=tem):
                contenido.append([det,'detalle'])

    return render(request, 'core/estudio.html',{'capitulos': capitulos,'temas':temas,'detalles':detalles,'curso':Curso,'contenido':contenido})

def ConstruidoView(request):
    User = request.user
    lista = curso.objects.filter(profesor=User,completo=True)
    return render(request,'core/construido.html', {'lista':lista,'ingresos':12.34})