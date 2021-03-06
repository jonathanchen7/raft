from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

import random
import json

from .raftYelp import find_rafts, create_args
from .models import ViewedRafts

from .forms import SearchForm

# Homepage View
def home(request):
    if request.GET.get('get-location'):
        return HttpResponse("clicked button")
    
    form = SearchForm(request.GET, auto_id="%s-form")
    return render(request, 'home.html', {'form': form})

# Search Page View
def search(request):
    form = SearchForm(request.POST, auto_id="mini-%s-form")

    if form.is_valid(): 
        term = form.cleaned_data['term']
        location = form.cleaned_data['location']
    else: # If '/search' is manually entered in the url.
        term = ''
        location = 'Seattle'

    raft_list = find_rafts(location, term)
    
    if not raft_list: # Executes if no restaurants are found.
        return render(request, 'search.html', { 'form': form, 'name': 'NO RESTUARANTS FOUND.'})
        
    num_rafts = len(raft_list) + 1

    args = {
        'raft_list': json.dumps([raft.__dict__ for raft in raft_list], indent=4),
        'num_rafts': num_rafts,
        'form': form,
    }

    return render(request, 'search.html', args)

# About Page View
def about(request):
    return render(request, 'about.html')

# Contact Page View
def contact(request):
    return render(request, 'contact.html')
    