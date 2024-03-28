from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from django.template.loader import render_to_string
import sys
if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
    from ..forms import *
from django.views.decorators.csrf import csrf_exempt
from ..models import User


def index(request):
    # User.objects.create_user("name", "mail", "password")
    current_site = get_current_site(request)

    # we get the static file path and concatenate it with the domain
    css_url = f'http://{current_site.domain}{static("CSS/styles.css")}'

    context = {
        'css_url': css_url,
        'form': Form
    }
    subject = 'Confirm your email address'
    message_html = render_to_string('email.html', context)
    email = "florian.de.boni@gmail.com"
    # send_mail(subject, None, None, [email], html_message=message_html)

    return render(request, "index.html", context={"form": Form})


@csrf_exempt
def index2(request):
    if request.method == "POST":
        context = {"success_message": "Bravo"}
        print(request.POST)
    else:
        context = {"error_message": "Pas Bravo"}
    return render(request, "index copy.html", context=context)
