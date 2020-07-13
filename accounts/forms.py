import re
from django import forms
from django.contrib.auth import (
    password_validation, authenticate, get_user_model)

from django.contrib.auth.forms import (ReadOnlyPasswordHashField,
                                       PasswordChangeForm,
                                       SetPasswordForm)
from django.utils.translation import ugettext_lazy as _
User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ('phone_number', 'email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('Confirm Password'), widget=forms.PasswordInput)

    class Meta:
        model = User
        error_messages = {'phone_number': {
            'unique': _('User with this phone number already exists')}}
        fields = ('phone_number', 'username', 'email')
        labels = {'phone_number': _('Phone Number'),
                  'username': _('Username'),
                  'email': _('Email'), }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # matches = re.findall(r'^09\d{8}$', phone_number)
        # if not matches:
        if not phone_number.isdigit():   
            raise forms.ValidationError(_('Please enter a valid phone number'))
        return phone_number

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        password_validation.validate_password(password)
        return password

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:

            raise forms.ValidationError_(("Password fields do not match"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Phone Number'))
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label=_('Remember Me'),required=False)

    def clean(self):
        phone_number = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        qs = User.objects.filter(phone_number=phone_number)
        if qs.exists() and qs.count() == 1:
            user = qs.first()
            if not user.is_active:
                raise forms.ValidationError(
                    _('Your account is not active, please check admin to activate your account'))
        user_authenticate = authenticate(
            username=phone_number, password=password)

        if not user_authenticate:
            raise(forms.ValidationError(_('username or password provided is incorrect')))

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ('phone_number', 'username', 'email', 'password',
                  'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        labels = {
                  'username': _('Username'),
                  'email': _('Email')}

        fields = ('username', 'email',)


class ChangePasswordForm(PasswordChangeForm):
    error_messages = {
                      'password_mismatch': _('The two password fields didn’t match'),
                      'password_incorrect': _('Your old password was entered incorrectly. Please enter it again')}


    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        password_validation.validate_password(password, self.user)
        return password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2


class MySetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        password_validation.validate_password(password, self.user)
        return password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

# class MyPasswordResetForm(PasswordResetForm):
#     pass
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     qs = User.objects.filter(email=email)
    #     if not qs.count() == 1:
    #         raise forms.ValidationError(
    #             'لا يوجد حساب مسجل مع هذا البريد الإلكتروني')
    #     return email
