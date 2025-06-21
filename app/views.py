# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)  # solo devuelve favoritos si está autenticado
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '').strip()

    if name != '':
        images = services.filterByCharacter(name)
        favourite_list = services.getAllFavourites(request)
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = []
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        images = [] # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    # Llamamos al servicio que obtiene la lista mapeada de favoritos
    favourite_list = services.getAllFavourites(request)

    # Pasamos la lista al template 'favourites.html' (el que usas)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})
    


@login_required
def saveFavourite(request):
    if request.method == 'POST':
        services.saveFavourite(request)

        # Obtener los favoritos actualizados del usuario
        favourites = Favourite.objects.filter(user=request.user)
        favourite_list = [f.name for f in favourites]  # Comparás por nombre

        # Obtener los pokémon igual que en 'home'
        pokemons = services.getAllImages()

        # Renderizar el home con los datos actualizados
        return render(request, 'home.html', {
            'images': pokemons,
            'favourite_list': favourite_list,
        })
    else:
        return redirect('home')


@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        success = services.deleteFavourite(request)
        return redirect('favoritos')
    else:
        return redirect('favoritos')


@login_required
def exit(request):
    logout(request)
    return redirect('home')