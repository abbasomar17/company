from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from .models import *


def feedback_user(request):
    offices = Office.objects.all()
    context = {
        "offices": offices
    }
    return render(request, 'cs_template/user_feedback_hr.html', context)


def feedback_user_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('feedback_user')
    else:
        feedback = request.POST.get('feedback_message')
        communication = request.POST.get('communication')
        office_id = request.POST.get('office')

        office = Office.objects.get(id=office_id)

        try:
            add_feedback = FeedBack(office=office, communication=communication, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('feedback_user')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('feedback_user')
