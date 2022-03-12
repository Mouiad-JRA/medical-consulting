from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from hitcount.utils import get_hitcount_model

from hitcount.views import HitCountDetailView

from .models import Slider, Service, Doctor, Faq, Gallery
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from accounts.forms import ConsultationForm


class HomeView(ListView):
    template_name = 'hospital/index.html'
    queryset = Service.objects.all()
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['sliders'] = Slider.objects.all()
        context['experts'] = Doctor.objects.all()
        context.update({
            'services': Service.objects.order_by('-hit_count_generic__hits'),
        })
        return context


class ServiceListView(ListView):
    queryset = Service.objects.all()
    template_name = "hospital/services.html"

    def get_queryset(self):
        return Service.objects.order_by('-hit_count_generic__hits')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'services': Service.objects.order_by('-hit_count_generic__hits'),
        })
        print(context["services"])
        return context


class ServiceDetailView(HitCountDetailView):
    queryset = Service.objects.all()
    count_hit = True
    template_name = "hospital/service_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.order_by('-hit_count_generic__hits')
        return context


class DoctorListView(ListView):
    template_name = 'hospital/team.html'
    queryset = Doctor.objects.all()
    paginate_by = 8


class DoctorDetailView(DetailView):
    template_name = 'hospital/team-details.html'
    queryset = Doctor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all()
        return context


class FaqListView(ListView):
    template_name = 'hospital/faqs.html'
    queryset = Faq.objects.all()


class GalleryListView(ListView):
    template_name = 'hospital/gallery.html'
    queryset = Gallery.objects.all()
    paginate_by = 9


class ContactView(TemplateView):
    template_name = "hospital/contact.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if subject == '':
            subject = "Healthcare Contact"

        if name and message and email and phone:
            send_mail(
                subject + "-" + phone,
                message,
                email,
                ['kncareerskwait@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, " Email has been sent successfully...")

        return redirect('contact')


class consultationView(CreateView):
    form_class = ConsultationForm
    template_name = "hospital/consultation.html"

    extra_context = {
        'title': 'Add consultation'
    }

    # def dispatch(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         return HttpResponseRedirect(self.get_success_url())
    #     return super().dispatch(self.request, *args, **kwargs)
    #
    def get_success_url(self):
        return reverse('accounts:login')
