from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(("email address"), unique=True)
    contact = models.TextField(blank=True, max_length=200, help_text="Contact")
    language_pref_fr = models.BooleanField(blank=True,
                                           default=False, help_text="English is prefered language")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Genre(models.Model):

    name = models.CharField(unique=True, max_length=200,
                            help_text="Genre name fr")
    name_en = models.CharField(unique=True, max_length=200,
                               help_text="Genre name en")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Game(models.Model):

    name = models.CharField(unique=True, max_length=200,
                            help_text="French name")
    name_en = models.CharField(
        default=name, max_length=200, help_text="English name")
    description_en = models.CharField(
        max_length=100, help_text="short english description")
    description_fr = models.CharField(
        max_length=100, help_text="short french description")
    quantity = models.IntegerField(help_text="Quantity available")
    genre = models.ManyToManyField(
        Genre, blank=True, max_length=3, help_text="Genres")
    duration = models.CharField(max_length=10,
                                help_text="Average game duration in minutes (x-x min)")
    favorites = models.ManyToManyField(User, blank=True, help_text="Genres")
    image = models.ImageField(default='media/logo.png',
                              upload_to='media/', help_text="Illustration (please use 1:1 aspect ratio for better results)")
    new = models.BooleanField(
        blank=True, default=False, help_text="Is a new game")
    player_number_max = models.IntegerField(
        default=4, help_text="max numbers of players")
    player_number_min = models.IntegerField(
        default=2, help_text="max numbers of players")

    def __str__(self):
        return self.name


class Command(models.Model):

    message_id = models.IntegerField(default=0)

    wait = models.BooleanField(
        default=False, help_text="Is the command waiting a validation")
    is_active = models.BooleanField(
        default=False, help_text="Is the command active")
    commander = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="Who did the command")
    games = models.ManyToManyField(
        Game, blank=True, help_text="Command content")
    start_date = models.DateField(default=None, null=True,
                                  blank=True, help_text="When the command should start")
    end_date = models.DateField(default=None, null=True,
                                blank=True, help_text="When the command should end")

    def __str__(self):
        return self.commander.email


class FavCommand(models.Model):

    games = models.ManyToManyField(
        Game, help_text="Command content")
    commander = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="Who did the command")

    def __str__(self):
        return self.commander.email
