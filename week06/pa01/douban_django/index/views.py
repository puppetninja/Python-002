from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.db.models import Q

from .models import Review

def index(request):
    reviews = Review.objects.filter(
        Q(review_rating='推荐') | Q(review_rating='力荐')
    )
    return render(request, 'index.html', locals())
