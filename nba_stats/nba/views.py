from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator

from nba.models import Player

# Create your views here.

class PlayerList(ListView):
	model = Player
	context_object_name = 'players'
	paginate_by = 50
