from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from django.template.loader import render_to_string
import sys
from django.views.decorators.csrf import csrf_exempt
from ..models import *
if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
    from ..forms import *
from .view_index import index


@csrf_exempt
def favorites(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            post_request = request.POST
            game = Game.objects.get(name=post_request['game_name'])
            if post_request['is_checked'] == 'false':
                game.favorites.remove(request.user)
                game.save()
            else:
                game.favorites.add(request.user)
                game.save()
        else:
            games = list(Game.objects.all())
            res = []
            for game in games:
                if len(game.favorites.filter(email=request.user)) == 1:
                    res.append(game)
            games = res
            games.sort(key=lambda x: -len(x.favorites.all()))
            dico = []
            for game in games:
                genres = list(game.genre.all())
                infos = {"game": game, "not_available": (
                    game.quantity <= 0), "is_favorite": True, "genre1": genres[0]}
                if len(genres) >= 2:
                    infos["genre2"] = " / " + genres[1].name
                    if len(genres) >= 3:
                        infos["genre3"] = " / " + genres[2].name
                dico.append(infos)
            favs = FavCommand.objects.filter(commander=request.user)

            return render(request, "favorites.html", context={"elements": dico, "games": zip([list(fav.games.all()) for fav in favs], favs)})
    else:
        games = list(Game.objects.filter(new=True))
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
        return render(request, "index.html", context={"elements": dico})
