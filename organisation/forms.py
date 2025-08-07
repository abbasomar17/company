#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from django import forms
from django.forms import Form
from django.contrib.auth.models import User
from .models import *
from apartment.models import *


class DateInput(forms.DateInput):
    input_type = "date"


class AddCEOForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    nida_number = forms.CharField(label="Nida Number", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Courses
    try:
        offices = Office.objects.all()
        office_list = []
        for office in offices:
            single_office = (office.id, office.title)
            office_list.append(single_office)
    except:
        office_list = []


    office = forms.ChoiceField(label="Office Name", choices=office_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))


class EditCEOForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Courses
    try:
        offices = Office.objects.all()
        office_list = []
        for office in offices:
            single_office = (office.id, office.title)
            office_list.append(single_office)
    except:
        office_list = []

    office = forms.ChoiceField(label="Office Name", choices=office_list,
                               widget=forms.Select(attrs={"class": "form-control"}))


class AddHRForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    nida_number = forms.CharField(label="Nida Number", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Courses
    try:
        offices = Office.objects.all()
        office_list = []
        for office in offices:
            single_office = (office.id, office.title)
            office_list.append(single_office)
    except:
        office_list = []


    office = forms.ChoiceField(label="Office Name", choices=office_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))


class EditHRForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))


class AddLawyerForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    nida_number = forms.CharField(label="Nida Number", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))



class EditLawyerForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))


class AddCSForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    nida_number = forms.CharField(label="Nida Number", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Courses
    try:
        offices = Office.objects.all()
        office_list = []
        for office in offices:
            single_office = (office.id, office.title)
            office_list.append(single_office)
    except:
        office_list = []


    office = forms.ChoiceField(label="Office Name", choices=office_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))


class EditCSForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))


class AddAccountantForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    nida_number = forms.CharField(label="Nida Number", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Courses
    try:
        offices = Office.objects.all()
        office_list = []
        for office in offices:
            single_office = (office.id, office.title)
            office_list.append(single_office)
    except:
        office_list = []


    office = forms.ChoiceField(label="Office Name", choices=office_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))


class EditAccountantForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))


class AddSWOForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    nida_number = forms.CharField(label="Nida Number", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Courses
    try:
        offices = Office.objects.all()
        office_list = []
        for office in offices:
            single_office = (office.id, office.title)
            office_list.append(single_office)
    except:
        office_list = []


    office = forms.ChoiceField(label="Office Name", choices=office_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))


class EditSWOForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))


class AddOfficeForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    spec_location = forms.CharField(label="Specific Location", max_length=50,
                                    widget=forms.TextInput(attrs={"class": "form-control"}))
    region = forms.CharField(label="Region", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    town = forms.CharField(label="Town", max_length=50,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))


class EditOfficeForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    spec_location = forms.CharField(label="Specific Location", max_length=50,
                                    widget=forms.TextInput(attrs={"class": "form-control"}))
    region = forms.CharField(label="Region", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    town = forms.CharField(label="Town", max_length=50,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))


class AddRateForm(forms.Form):
    rate = forms.FloatField(label="Increment",
                            widget=forms.NumberInput(attrs={"class": "form-control"}))


class EditRateForm(forms.Form):
    rate = forms.FloatField(label="Increment",
                            widget=forms.NumberInput(attrs={"class": "form-control"}))


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'first_name', 'last_name']


