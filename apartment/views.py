import random

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User

from apartment.EmailBackEnd import EmailBackEnd
import os
import uuid
import sys
import zipfile
import company.settings
from datetime import datetime
from zipfile import ZipFile

from django.contrib import admin
from django.contrib.auth.backends import ModelBackend
from django.core.files.base import ContentFile
from company.settings import BASE_DIR


from PIL import Image

from .models import *
from .forms import AlbumForm, EditApartmentForm

# Create your views here.

def gallery(request):
    list = Album.objects.filter(is_visible=True).order_by('region')
    paginator = Paginator(list, 10)

    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        albums = paginator.page(
            paginator.num_pages)  # If page is out of range (e.g.  9999), deliver last page of results.

    return render(request, 'home_template/home.html', {'albums': list})


class AlbumDetail(DetailView):
     model = Album

     def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['images'] = AlbumImage.objects.filter(album=self.object.id)
        return context


def handler404(request, exception):
    assert isinstance(request, HttpRequest)
    return render(request, 'handler404.html', None, None, 404)


def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method == "POST":
        if User.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            user = User.objects.get(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                custom = CustomUser.objects.get(user=user)
                user_type = custom.user_type
                # return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
                if user_type == '1':
                    return redirect('admin_home')

                elif user_type == '2':
                    # return HttpResponse("Staff Login")
                    return redirect('staff_home')

                elif user_type == '3':
                    # return HttpResponse("Student Login")
                    return redirect('student_home')
                elif user_type == '4':
                    return redirect('user_home')
                elif user_type == '5':
                    return redirect("/")
                else:
                    messages.error(request, "Invalid Login!")
                    return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect('login')


def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: " + request.user.email + " User Type: " + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return redirect('login')


def cart_item_counter(request):
    user = Random_users.objects.get(id=request.user.id)
    qs = Order.objects.filter(user=user, ordered=False)
    orders = qs.items.count()

    context = {
        "user": user,
        "orders": orders,
    }
    return render(request, 'home_template/base_template.html', context)

