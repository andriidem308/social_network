"""Social Network Middlewares file."""
from datetime import timedelta as td

from dateutil.parser import parse
from django.utils import timezone

from .models import UserProfile


class SetLastVisitMiddleware(object):
    """Set last visit time middleware."""

    def __init__(self, get_response):
        """Init the middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Call the middleware."""
        if request.user.is_authenticated:
            last_activity = request.session.get('last-activity')
            too_old_time = timezone.now() - td(seconds=60)

            if not last_activity or parse(last_activity) < too_old_time:
                UserProfile.objects.filter(user=request.user.pk).update(
                    last_visit=timezone.now())

            request.session['last-activity'] = timezone.now().isoformat()

        response = self.get_response(request)
        return response
