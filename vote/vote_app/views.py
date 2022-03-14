from django.shortcuts import render

def home_view(request):
    return render(request, 'index.html')

def vote_view(request):
    return render(request, 'vote.html')
