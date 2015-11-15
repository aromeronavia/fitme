from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import UserProfile


class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name'
        ]

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def signup(self, request, user):
        user.save()
        UserProfile.objects.create(authentication_user=user)


class UserProfileUpdateForm(forms.ModelForm):
    """
        Form to update and existing user and all its information
    """
    image_profile = forms.ImageField(
        required=False,
        label='Profile image'
    )
    age = forms.IntegerField(label='Age')
    gender = forms.ChoiceField(
        label='Gender',
        choices=UserProfile.GENDER_CHOICES
    )
    biography = forms.CharField(
        widget=forms.Textarea
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'age', 'gender',
            'email', 'image_profile', 'biography'
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        try:
            user_profile = UserProfile.objects.get(
                authentication_user=kwargs['instance']
            )
        except UserProfile.DoesNotExist:
            raise forms.ValidationError(
                _('username "%(username)s" does not have a related'
                  'UserProfile'),
                code='invalid_username',
                params={
                    'username': kwargs['instance'].username
                }
            )
        self.initial.update({
            'image_profile': user_profile.image_profile,
            'gender': user_profile.gender,
        })

    def save(self, commit=True):
        user = super(UserProfileUpdateForm, self).save(commit=False)
        user_profile = UserProfile.objects.get(authentication_user=user)
        user_profile.age = self.cleaned_data['age']
        user_profile.gender = self.cleaned_data['gender']
        user_profile.image_profile = self.cleaned_data['image_profile']
        user_profile.bio = self.cleaned_data['biography']
        if commit:
            user_profile.save()
            user.save()
        return user
