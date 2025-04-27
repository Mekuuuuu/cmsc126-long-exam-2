from django.utils import timezone
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

def index(request):
    return render(request, "accounts/index.html")