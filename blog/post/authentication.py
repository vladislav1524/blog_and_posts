from .models import UserProfile


def create_profile(backend, user, *args, **kwargs):
    """
    Create user profile for social authentication
    """
    UserProfile.objects.get_or_create(user=user)