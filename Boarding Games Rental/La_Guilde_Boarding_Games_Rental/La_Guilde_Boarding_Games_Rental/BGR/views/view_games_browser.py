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

    games = list(Game.objects.all())
    games.sort(key=lambda x: -len(x.favorites.all()))
    search_text = ""

    form = SearchForm(language=(
        request.user.is_authenticated and request.user.language_pref_fr))
    if request.method == "POST":
        post_request = request.POST
        if 'is_checked' in post_request:
            game = Game.objects.get(name=post_request['game_name'])
            if post_request['is_checked'] == 'false':
                game.favorites.remove(request.user)
                game.save()
            else:
                game.favorites.add(request.user)
                game.save()
        else:
            form = SearchForm(request.POST, language=(
                request.user.is_authenticated and request.user.language_pref_fr))

            post_request = request.POST
            tmin = 0
            tmax = 1000
            pmin = 0
            pmax = 1000
            categories = []
            search_text = post_request['Search text']

            if post_request['time_start'] != '':
                tmin = int(post_request['time_start'])
            if post_request['time_end'] != '':
                tmax = int(post_request['time_end'])
            if post_request['player_min'] != '':
                pmin = int(post_request['player_min'])
            if post_request['player_max'] != '':
                pmax = int(post_request['player_max'])
            if pmin > pmax:
                pmin, pmax = pmax, pmin
            if tmin > tmax:
                tmin, tmax = tmax, tmin
            if 'category' in post_request:
                categories = [Genre.objects.get(
                    name=category) for category in request.POST.getlist("category")]
                games = Game.objects.filter(genre__in=categories).distinct()
            else:
                games = Game.objects.all()
            res = []
            for game in games:
                if game.player_number_min >= pmin and game.player_number_max <= pmax:
                    duration = int(game.duration.removesuffix(" min"))
                    if duration >= tmin and duration <= tmax:
                        res.append(game)
            games = res
            if search_text != "":
                games = find_closest_names(search_text, games, request)
            else:
                games.sort(key=lambda x: -len(x.favorites.all()))

    dico = []
    for game in games:
        genres = list(game.genre.all())
        infos = {"game": game, "not_available": (game.quantity <= 0), "is_favorite": len(
            game.favorites.filter(email=request.user)) == 1, "genre1": genres[0]}
        if len(genres) >= 2:
            infos["genre2"] = " / " + genres[1].name
            if len(genres) >= 3:
                infos["genre3"] = " / " + genres[2].name
        dico.append(infos)
    return render(request, "games.html", context={"elements": dico, "form": form, "search": search_text})


def sort_by_alphabetic(input_text):
    return ''.join(sorted(input_text))


def find_closest_names(input_text, games, request):
    input_text_normalized = input_text.lower().replace(" ", "")
    sorted_input_text = sort_by_alphabetic(input_text_normalized)

    if request.user.is_authenticated and request.user.language_pref_fr:
        distances = [(game.name, Levenshtein.distance(sorted_input_text, sort_by_alphabetic(game.name.lower().replace(" ", ""))))
                     for game in games]
    else:
        distances = [(game.name_en, Levenshtein.distance(sorted_input_text, sort_by_alphabetic(game.name_en.lower().replace(" ", ""))))
                     for game in games]

    distances.sort(key=lambda x: x[1])
    closest_names = [name for name, _ in distances]
    closest_games = [Game.objects.get(name=name) for name in closest_names]
    return closest_games
