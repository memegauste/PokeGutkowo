from pokegutkowo.models import Settings


def base(request):
    return {
        'settings': Settings.objects.filter().first()
    }
