from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect

from .models import *
from .forms import *


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['name', 'email', 'picture', 'job_title', 'location', 'personal_url',
              'facebook_account', 'twitter_account', 'github_account',
              'linkedin_account', 'short_bio', 'bio', ]
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "users/user_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = User.objects.filter(type='student')
        return context

class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['education', 'venue']
    template_name = 'users/user_profile_create.html'
    def form_valid(self, form):
        model = form.save(commit=False)
        current_user = self.request.user
        model.user = current_user
        current_user.is_new = False
        current_user.is_ksko = True
        current_user.save()
        model.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('users:dashboard')
