import Levenshtein
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from django.template.loader import render_to_string
import sys
from django.views.decorators.csrf import csrf_exempt
from ..models import *
if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
    from ..forms import *


@csrf_exempt
def view_games(request):
    if request.method == "POST":
        post_request = request.POST
        if len(post_request) == 3:
            game = Game.objects.get(name=post_request['game_name'])
            if post_request['is_checked'] == 'false':
                game.favorites.remove(request.user)
                game.save()
            else:
                game.favorites.add(request.user)
                game.save()
        else:
            pass
    games = Game.objects.all()
    dico = []
    for game in games:
        genres = list(game.genre.all())
        infos = {"game": game, "not_available": (game.quantity <= 0), "is_favorite": len(
            game.favorites.filter(email=request.user)) == 1, "genre1": genres[0]}
        if len(genres) >= 2:
            infos["genre2"] = genres[1]
            if len(genres) >= 3:
                infos["genre3"] = genres[2]
        dico.append(infos)
    return render(request, "games.html", context={"elements": dico})


def find_closest_names(input_text, names, num_closest=3):
    input_text = input_text.lower()
    distances = [(name, Levenshtein.distance(input_text, name.lower()))
                 for name in names]
    distances.sort(key=lambda x: x[1])
    closest_names = [name for name, _ in distances[:num_closest]]
    return closest_names
