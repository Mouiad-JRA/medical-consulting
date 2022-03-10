from .models import Doctor, Service


def footer_content(request):
    services = Service.objects.order_by('-hit_count_generic__hits')
    doctors = Doctor.objects.all()
    context = {
        'services': services,
        'doctors': doctors
    }
    return context
