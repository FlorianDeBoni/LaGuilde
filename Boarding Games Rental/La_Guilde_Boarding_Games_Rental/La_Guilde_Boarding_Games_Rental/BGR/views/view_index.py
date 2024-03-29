from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from django.template.loader import render_to_string
import sys
from django.views.decorators.csrf import csrf_exempt
import random
if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
    from ..forms import *
from django.core.mail import send_mail
from django.contrib.auth import login, get_user_model, logout, authenticate


def index(request):
    return render(request, "index.html", context={})


def disconnect(request):
    try:
        logout(request)
        context = {"success_message": "Successfully logged out"}
    except:
        context = {"error_message": "Fail to log out"}
    return render(request, "index.html", context=context)


def create_account(request):
    if request.user.is_authenticated:
        return render(request, "index.html", context={"success_message": "You are logged in"})
    if request.method == "POST":

        if request.POST["password"] != request.POST["confirm_password"]:
            context = {
                'password': request.POST["password"],
                'email': request.POST["email"],
                'confirm_password': request.POST["confirm_password"],
                'error_message': "You entered 2 different passwords",
            }
            return render(request, "sign.html", context=context)

        email = request.POST["email"]
        password = request.POST["password"]
        code1 = random.randint(0, 9)
        code2 = random.randint(0, 9)
        code3 = random.randint(0, 9)
        code4 = random.randint(0, 9)
        context = {
            'code1': code1,
            'code2': code2,
            'code3': code3,
            'code4': code4,
            'email': email,
            'password': password,
        }
        subject = 'Confirm your email address: ' + \
            str(code1)+'-'+str(code2)+'-'+str(code3)+'-'+str(code4)
        message_html = render_to_string('email.html', context)
        try:
            user = User.objects.get(email=email)
            return render(request, "sign.html", context={"error_message": "This email is already used", "form": LoginForm()})
        except:
            send_mail(subject, None, None, [email], html_message=message_html)
            return render(request, "confirmation.html", context=context)
    else:
        return render(request, "sign.html", context={})


def connect(request):
    if request.user.is_authenticated:
        return render(request, "index.html", context={"success_message": "You are logged in"})
    if request.method == "POST":
        user = authenticate(
            username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return render(request, "index.html", context={"success_message": "Successfully logged in"})
        else:
            return render(request, "log.html", context={"error_message": "Your email or password is wrong", "email": request.POST['email'], "password": request.POST['password']})
    else:
        return render(request, "log.html", context={})


def verify_email(request):
    if request.method == "POST":
        password = request.POST['password']
        email = request.POST['email']
        code1 = request.POST['code1']
        code2 = request.POST['code2']
        code3 = request.POST['code3']
        code4 = request.POST['code4']
        entry1 = request.POST['Entry1']
        entry2 = request.POST['Entry2']
        entry3 = request.POST['Entry3']
        entry4 = request.POST['Entry4']
        if not (code1 == entry1 and code2 == entry2 and code3 == entry3 and code4 == entry4):
            context = {"email": email, "password": password, "code1": code1, "code2": code2, "code3": code3, "code4": code4,
                       "Entry1": entry1, "Entry2": entry2, "Entry3": entry3, "Entry4": entry4,
                       "error_message": "Wrong password submitted",
                       }
            return render(request, "confirmation.html", context=context)
        User = get_user_model()
        user = User.objects.create_user(email, password)
        login(request, user)
        return render(request, "index.html", context={"success_message": "You have successfully verified your email"})
    else:
        return render(request, "index.html")


def reset(request):
    if request.method == "POST":
        if request.POST["password"] != request.POST["confirm_password"]:
            context = {
                'password': request.POST["password"],
                'email': request.POST["email"],
                'confirm_password': request.POST["confirm_password"],
                'error_message': "You entered 2 different passwords",
            }
            return render(request, "resetform.html", context=context)
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        code1 = random.randint(0, 9)
        code2 = random.randint(0, 9)
        code3 = random.randint(0, 9)
        code4 = random.randint(0, 9)
        context = {
            'code1': code1,
            'code2': code2,
            'code3': code3,
            'code4': code4,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
        }
        subject = 'Reset your password: ' + \
            str(code1)+'-'+str(code2)+'-'+str(code3)+'-'+str(code4)
        message_html = render_to_string('resetemail.html', context)
        try:
            user = User.objects.get(email=email)
            send_mail(subject, None, None, [email], html_message=message_html)
            return render(request, "confirm_reset.html", context=context)
        except:
            context["error_message"] = "There is no account registered with this email"
            return render(request, "resetform.html", context=context)

    return render(request, "resetform.html", context={})


def confirm_reset(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        code1 = request.POST['code1']
        code2 = request.POST['code2']
        code3 = request.POST['code3']
        code4 = request.POST['code4']
        entry1 = request.POST['Entry1']
        entry2 = request.POST['Entry2']
        entry3 = request.POST['Entry3']
        entry4 = request.POST['Entry4']
        if not (code1 == entry1 and code2 == entry2 and code3 == entry3 and code4 == entry4):
            context = {"email": email, "password": password, "code1": code1, "code2": code2, "code3": code3, "code4": code4,
                       "Entry1": entry1, "Entry2": entry2, "Entry3": entry3, "Entry4": entry4,
                       "error_message": "Wrong password submitted",
                       }
            return render(request, "confirm_reset.html", context=context)
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return render(request, "index.html", context={"success_message": "Password successfully changed"})
    return render(request, "index.html", context={})


def reset_password(request):
    if request.method == "POST":
        return render(request, "index.html", context={})
    return render(request, "index.html", context={})


@csrf_exempt
def test(request):
    if request.method == "POST":
        print(request.POST)
        return render(request, "test.html")
    return render(request, "test.html")


def test2(request):
    return render(request, "test2.html")
