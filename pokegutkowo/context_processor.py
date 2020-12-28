"""Context processor file."""
# Project
from pokegutkowo.models import Settings


def base(request):  # noqa: D103
    return {
        'settings': Settings.objects.filter().first(),
    }
