from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from bootcamp.notifications.models import Notification, notification_handler
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.

    STAFF = 'staff'
    STUDENT = 'student'

    USER_TYPE = (
        (STAFF, 'staff'),
        (STUDENT, 'student'),

    )

    name = models.CharField(_("User's name"), blank=True, max_length=255)
    picture = models.ImageField(
        _('Profile picture'), upload_to='profile_pics/', null=True, blank=True)
    mobile = PhoneNumberField()
    type = models.CharField(max_length=10, choices=USER_TYPE, default=STUDENT)
    is_new = models.BooleanField(default=False)
    is_ksko = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_profile_name(self):
        if self.name:
            return self.name

        return self.username

class Profile(models.Model):

    EIGHT = '8'
    NINE = '9'
    TEN = '10'

    CLASSES = (
        (EIGHT, '8th Class'),
        (NINE, '9th Class'),
        (TEN, '10th Class'),
    )

    VENUE1 = 'venue1'
    VENUE2 = 'venue2'
    VENUE3 = 'venue3'

    VENUES = (
        (VENUE1, 'venue1'),
        (VENUE2, 'venue2'),
        (VENUE3, 'venue3'),
    )

    education = models.CharField(_("Class"),max_length=20, choices=CLASSES)
    venue = models.CharField(_("Exam Center"), max_length=20, choices=VENUES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

def broadcast_login(sender, user, request, **kwargs):
    """Handler to be fired up upon user login signal to notify all users."""
    notification_handler(user, "global", Notification.LOGGED_IN)


def broadcast_logout(sender, user, request, **kwargs):
    """Handler to be fired up upon user logout signal to notify all users."""
    notification_handler(user, "global", Notification.LOGGED_OUT)


# user_logged_in.connect(broadcast_login)
# user_logged_out.connect(broadcast_logout)
