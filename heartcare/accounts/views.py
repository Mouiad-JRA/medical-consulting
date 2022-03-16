import os

from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, FormView, RedirectView

from .bayes import sklearn_algorithm
from .bayes_hard import sklearn_algorithm_from_scratch
from .forms import *
from .id3_real import id3_hard
from .models import User


class RegisterPatientView(CreateView):
    """
        Provides the ability to register as a Patient.
    """
    model = User
    form_class = PatientRegistrationForm
    template_name = 'accounts/patient/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/patient/register.html', {'form': form})


class RegisterDoctorView(CreateView):
    """
       Provides the ability to register as a Doctor.
    """
    model = User
    form_class = DoctorRegistrationForm
    template_name = 'accounts/doctor/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/doctor/register.html', {'form': form})


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
        Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out from our site (Mouiad, Mazen, Milad and Abdullah) :)')
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterPersonView(CreateView):
    """
        Provides the ability to register as a Patient.
    """
    model = Person
    form_class = PersonForm
    template_name = 'accounts/heartHealth.html'
    success_url = '/'

    extra_context = {
        'title': 'Check'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            Person = form.save(commit=False)
            real_result_naive = sklearn_algorithm(os.path.abspath("heart_disease_male.csv"), Person.age,
                                                  Person.chest_pain_type, Person.rest_blood_pressure,
                                                  Person.blood_sugar,
                                                  Person.rest_electro, Person.max_heart_rate, Person.exercice_angina)
            fake_result_naive = sklearn_algorithm_from_scratch(
                os.path.abspath("heart_disease_handled_male.csv"),
                Person.age,
                Person.chest_pain_type, Person.rest_blood_pressure,
                Person.rest_blood_pressure,
                Person.rest_electro, Person.max_heart_rate, Person.exercice_angina)
            real_result_id3 = id3_hard(os.path.abspath("heart_disease_male.csv"), Person.age,
                                       Person.chest_pain_type, Person.rest_blood_pressure, Person.blood_sugar,
                                       Person.rest_electro, Person.max_heart_rate, Person.exercice_angina)
            # fake_result_id3 = sklearn_algorithm_from_scratch(os.path.abspath("accounts/heart_disease_handled_male.csv"),
            #                                          Person.age,
            #                                          Person.chest_pain_type, Person.rest_blood_pressure,
            #                                          Person.rest_blood_pressure,
            #                                          Person.rest_electro, Person.max_heart_rate, Person.exercice_angina)

            return render(request, 'accounts/results.html',
                          {"fake_result_naive": fake_result_naive,
                           "real_result_naive": real_result_naive,
                           "real_result_id3": real_result_id3
                           })
        else:
            return render(request, 'accounts/patient/register.html', {'form': form})
