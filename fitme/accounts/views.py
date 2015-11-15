from django.views.generic import DetailView, UpdateView
from django.utils.translation import ugettext_lazy as _
from common.mixins import FormMessagesMixin, LoginRequiredMixin
from .forms import UserProfileUpdateForm
from .models import UserProfile
# Create your views here.


class UserProfileDetailView(LoginRequiredMixin, DetailView):
        template_name = 'account/user_profile.html'
        context_object_name = 'user_profile'

        def get_object(self, queryset=None):
            authentication_user = self.request.user
            user, created = UserProfile.objects.get_or_create(
                authentication_user=authentication_user
            )
            return user

        def get_context_data(self, **kwargs):
            context = super(UserProfileDetailView, self).get_context_data(
                **kwargs
            )
            user = self.request.user
            context['user_accounts'] = user.socialaccount_set.all()
            return context


class UserProfileUpdateView(LoginRequiredMixin, FormMessagesMixin, UpdateView):
    """
        View to update an existing user an all its information
    """
    form_class = UserProfileUpdateForm
    template_name = 'account/update_user_profile.html'
    success_message = _('User profile successfully updated')
    error_message = _('An error ocurred trying to update the user profile')

    def get_success_url(self):
        return reverse('accounts:user_profile')

    def get_form_kwargs(self):
        kwargs = super(UserProfileUpdateView, self).get_form_kwargs()
        kwargs.update({
            'instance': self.request.user
        })
        return kwargs

    def get_object(self, queryset=None):
        authentication_user = self.request.user
        return UserProfile.objects.get(
            authentication_user=authentication_user
        )
