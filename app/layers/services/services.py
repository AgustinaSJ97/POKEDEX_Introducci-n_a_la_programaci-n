# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    raw_images = transport.getAllImages()
    cards = []

    for raw in raw_images:
        card = translator.fromRequestIntoCard(raw)
        cards.append(card)

    return cards


# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        if name.lower() in card.name.lower():
            filtered_cards.append(card)

    return filtered_cards

def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        if type_filter.lower() in [t.lower() for t in card.types]:
            filtered_cards.append(card)

    return filtered_cards


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request)
    fav.user = get_user(request)
    return repositories.save_favourite(fav)


# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    
    user = get_user(request)
    favourite_list = repositories.get_all_favourites(user)
    mapped_favourites = []

    for favourite in favourite_list:
        card = translator.fromRepositoryIntoCard(favourite)
        mapped_favourites.append(card)

    return mapped_favourites


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId)


#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)
