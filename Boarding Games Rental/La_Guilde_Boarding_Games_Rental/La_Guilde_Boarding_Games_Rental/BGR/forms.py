from django import forms
from .models import Genre, Game


class CommandForm(forms.Form):
    def __init__(self, *args, initial_game=None, **kwargs):
        super(CommandForm, self).__init__(*args, **kwargs)

        GAME = list(Game.objects.all())
        GAME.sort(key=lambda x: x.name)
        choices = [(game, game) for game in GAME]
        self.fields['games'] = forms.ChoiceField(required=True, initial=initial_game,
                                                 choices=choices, widget=forms.Select)
        self.fields["datestart"] = forms.DateField(
            required=True,
            widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            input_formats=["%Y-%m-%d"])
        self.fields["dateend"] = forms.DateField(required=True, widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date"}),
            input_formats=["%Y-%m-%d"])
        self.fields["infos"] = forms.CharField(
            required=True, widget=forms.Textarea(attrs={'rows': 10, 'cols': 60}))


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.fields['time_start'] = forms.IntegerField(
            required=False, min_value=0)
        self.fields['time_end'] = forms.IntegerField(required=False,
                                                     min_value=self.initial.get('time_start', 0))

        self.fields['player_min'] = forms.IntegerField(
            required=False, min_value=0)
        self.fields['player_max'] = forms.IntegerField(
            required=False, min_value=self.initial.get('player_min', 0))

        GENRE = Genre.objects.all()
        choices = [(genre.name, genre) for genre in GENRE]
        self.fields['category'] = forms.MultipleChoiceField(
            choices=choices, widget=forms.CheckboxSelectMultiple)
