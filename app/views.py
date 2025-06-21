# capa de vista/presentación


from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app.models import Favourite
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from app.forms import RegisterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = []
    favourite_list = []

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = []
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemondef filter_by_type(request):
    type = request.POST.get('type', '').strip()

    if type != '':
        images = services.filterByType(type)
        favourite_list = services.getAllFavourites(request)
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')
    
def register(request): 
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Enviar correo
            try:
                subject = '¡Bienvenido a Pokedex!'
                from_email = settings.EMAIL_HOST_USER
                recipient = user.email

                context ={
                    'user': user,
                    'message': f'Hola {user.first_name}! Bienvenido a Pokedex, tu cuenta ha sido creada exitosamente.'
                    
                }
                
                html_content = render_to_string('registration/email.html', context)
                text_content = f'Hola {user.first_name}! Bienvenido a Pokedex, tu cuenta ha sido creada exitosamente. link: http://127.0.0.1:8000/login'

                email = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
                email.attach_alternative(html_content, "text/html")
                email.send()
            except Exception as e:
                print(f'Error al enviar el correo: {e}') 
            messages.success(request, 'Cuenta creada correctamente. Te enviamos un email de bienvenida.')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    pass

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('home')