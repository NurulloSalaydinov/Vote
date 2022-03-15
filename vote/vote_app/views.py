from django.shortcuts import render
from .models import *

def home_view(request):
    return render(request, 'index.html')

def vote_view(request):
    last_title = Title.objects.last()
    last_ten_category = Category.objects.all().order_by('-id')[:10]
    context = {
        'last_title': last_title,
        'last_categories': last_ten_category
    }
    return render(request, 'vote.html', context)
