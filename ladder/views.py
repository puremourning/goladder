from django.http import HttpResponse, Http404

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.urlresolvers import reverse_lazy

from ladder.models import Player, Match
from ladder.forms import MatchForm

from datetime import datetime

class LadderView(generic.ListView):
    template_name = 'ladder/ladder.html'
    context_object_name = 'ladder'

    def get_queryset(self):
        return Player.objects.order_by('-rating').filter(games_played__gte=3)

class MatchView (generic.DetailView):
    model = Match

class MatchCreate (generic.edit.CreateView):
    model = Match
    form_class = MatchForm

    def get_initial(self):
        return {
            'date': datetime.now()
        }

class MatchAmend (generic.edit.UpdateView):
    # note that changing the result does not fix the ratings
    model = Match
    form_class = MatchForm

class MatchDelete (generic.edit.DeleteView):
    # note: we can't undo the result of the match on the ratings
    model = Match
    success_url = reverse_lazy('ladder')

class PlayerView(generic.DetailView):
    model = Player

