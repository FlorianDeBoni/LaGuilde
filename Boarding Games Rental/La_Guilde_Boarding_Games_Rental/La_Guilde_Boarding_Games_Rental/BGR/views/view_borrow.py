from django.shortcuts import render
import sys
from django.views.decorators.csrf import csrf_exempt
import random
if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
    from ..forms import *
from ..models import *
from .view_bot import send_message, delete_message, edit_message


def add_fav_command(request):
    if request.user.is_authenticated:
        command = Command.objects.get(commander=request.user)
        init = {}
        if request.user.is_authenticated and request.user.language_pref_fr:
            context = {
                "success_message": "Ajouté à vos commandes favorites avec succès"}
        else:
            context = {
                "success_message": "Successfully added to your favorites commands"}
        command = Command.objects.get(commander=request.user)
        init["games"] = command.games.all()
        init["datestart"] = command.start_date
        init["dateend"] = command.end_date
        init["infos"] = request.user.contact
        form = CommandForm(initial=init, language=(
            request.user.is_authenticated and request.user.language_pref_fr))
        context["games"] = []
        games = list(command.games.all())

        if command.wait:
            new_fav = FavCommand(commander=request.user)
            new_fav.save()
            new_fav.games.set(games)

        res = []
        for game in games:
            if request.user.language_pref_fr:
                initial_game = (game, game)
            else:
                initial_game = (game.name_en, game)
            instance = CommandForm(initial_game=initial_game, language=(
                request.user.is_authenticated and request.user.language_pref_fr))
            res.append(instance)
        context["games"] = res
        context["form"] = form
        command = Command.objects.get(
            commander=request.user)
        context["wait"] = command.wait
        context["is_active"] = not (command.is_active)
        return render(request, "borrow.html", context=context)

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


def borrowform(request):
    if request.user.is_authenticated:
        init = {}
        command = Command.objects.get(commander=request.user)
        init["games"] = command.games.all()
        games = command.games.all()
        init["datestart"] = command.start_date
        init["dateend"] = command.end_date
        init["infos"] = request.user.contact
        form = CommandForm(initial=init, language=(
            request.user.is_authenticated and request.user.language_pref_fr))
        context = {}

        if request.method == "POST":
            post_request = request.POST
            games = post_request.getlist("games")
            games = [Game.objects.get(name=game)
                     for game in games]
            games = list(set(games))
            command.games.clear()
            command.games.set(games)
            command.start_date = post_request["datestart"]
            command.end_date = post_request["dateend"]
            request.user.contact = post_request["infos"]
            request.user.save()
            form = CommandForm(post_request, language=(
                request.user.is_authenticated and request.user.language_pref_fr))
            res = not (command.is_active)
            for game in games:
                if game.quantity <= 0:
                    res = False
                    pb = game
                    break
            if command.is_active:
                if request.user.is_authenticated and request.user.language_pref_fr:
                    context = {
                        "error_message": "Tu dois d'abord rendre ta commande en cours"}
                else:
                    context = {
                        "error_message": "You must give your previous order back first"}
            elif res and not (command.is_active):
                message = "From " + command.commander.email + "\n"
                message += "Start "+command.end_date+". End "+command.start_date+".\n"
                message += "Content:"+"\n"
                for game in games:
                    message += "- " + game.name + "\n"
                if request.user.contact != "":
                    info = request.user.contact
                    message = message + "\n" + "Here are some extra informations:" + \
                        "\n" + info
                if (command.wait):
                    id = str(command.message_id)
                    message = "Command n°"+id+"\n"+message
                    if request.user.is_authenticated and request.user.language_pref_fr:
                        context = {"success_message": "Commande mise à jour"}
                    else:
                        context = {"success_message": "Command updated"}
                    edit_message(message, command.message_id)
                    command.save()
                else:
                    if request.user.is_authenticated and request.user.language_pref_fr:
                        context = {"success_message": "Commande envoyée"}
                    else:
                        context = {"success_message": "Command sent"}
                    command.wait = True
                    command.message_id = send_message(message)
                    command.save()
                    id = str(command.message_id)
                    message = "Command n°"+id+"\n"+message
                    edit_message(message, command.message_id)
            else:
                if request.user.is_authenticated and request.user.language_pref_fr:
                    context = {"error_message": pb.name +
                               " n'est pas disponible"}
                else:
                    context = {"error_message": pb.name_en+" is not available"}
        context["games"] = []
        games = list(games)
        res = []
        for game in games:
            if request.user.language_pref_fr:
                initial_game = (game, game)
            else:
                initial_game = (game.name_en, game)
            instance = CommandForm(initial_game=initial_game, language=(
                request.user.is_authenticated and request.user.language_pref_fr))
            res.append(instance)

        context["games"] = res
        context["form"] = form
        command = Command.objects.get(
            commander=request.user)
        context["wait"] = command.wait
        context["is_active"] = not (command.is_active)
        return render(request, "borrow.html", context=context)

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


def delete(request):
    if request.user.is_authenticated:

        command = Command.objects.get(commander=request.user)
        if command.wait and not (command.is_active):
            command.wait = False
            command.is_active = False
            command.save()
            delete_message(command.message_id)
            if request.user.is_authenticated and request.user.language_pref_fr:
                context = {"success_message": "Commande annulée"}
            else:
                context = {"success_message": "Command canceled"}
        else:
            if request.user.is_authenticated and request.user.language_pref_fr:
                context = {"error_message": "Rien à annuler"}
            else:
                context = {"error_message": "Nothing to cancel"}
        init = {}
        command = Command.objects.get(commander=request.user)
        init["games"] = command.games.all()
        init["datestart"] = command.start_date
        init["dateend"] = command.end_date
        init["infos"] = request.user.contact
        form = CommandForm(initial=init, language=(
            request.user.is_authenticated and request.user.language_pref_fr))
        context["games"] = []
        games = list(command.games.all())
        res = []
        for game in games:
            if request.user.language_pref_fr:
                initial_game = (game, game)
            else:
                initial_game = (game.name_en, game)
            instance = CommandForm(initial_game=initial_game, language=(
                request.user.is_authenticated and request.user.language_pref_fr))
            res.append(instance)

        context["games"] = res
        context["form"] = form
        command = Command.objects.get(
            commander=request.user)
        context["wait"] = command.wait
        context["is_active"] = not (command.is_active)
        return render(request, "borrow.html", context=context)

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
