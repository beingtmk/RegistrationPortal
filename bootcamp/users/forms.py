from allauth.account.forms import SignupForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

class CustomSignupForm(SignupForm):

    mobile = PhoneNumberField(widget = PhoneNumberInternationalFallbackWidget())

    def signup(self, request, user):
        user.mobile = self.cleaned_data['mobile']
        user.save()
        return user
