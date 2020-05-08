import re
from django import forms
from django.contrib.auth import (
    password_validation, authenticate, get_user_model)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm

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
        label='كلمة المرور', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='تأكيد  كلمة المرور', widget=forms.PasswordInput)

    class Meta:
        model = User
        error_messages = {'phone_number': {
            'null': 'لا يمكن ترك هذا الحقل فارغ',
            'unique': 'المسخدم برقم الهاتف هذا موجود بالفعل'}}
        fields = ('phone_number', 'username', 'email')
        labels = {'phone_number': 'رقم الهاتف',
                  'username': 'إسم المستخدم',
                  'email': 'البريد الإلكتروني', }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        matches = re.findall(r'^09\d{8}$', phone_number)
        if not matches:
            raise forms.ValidationError('يرجي إدخال رقم هاتف صحيح ')
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

            raise forms.ValidationError("حقلي كلمة المرور غير متطابقين.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='رقم الهاتف')
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)

    def clean(self):
        phone_number = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        qs = User.objects.filter(phone_number=phone_number)
        if qs.exists() and qs.count() == 1:
            user = qs.first()
            if not user.is_active:
                raise forms.ValidationError(
                    'الحساب غير مفعل يرجى التأكد من المشرف حتى يتم تفعيل حسابك')
        user_authenticate = authenticate(
            username=phone_number, password=password)

        if not user_authenticate:
            raise(forms.ValidationError(
                'إسم المستخدم أو كلمة المرور غير صحيح يرجى التأكد من البيانات'))


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
        labels = {'phone_number': 'رقم الهاتف',
                  'username': 'إسم  المستخدم',
                  'email': 'البريد الإلكتروني'}

        fields = ('username', 'email',)


def get_data(self):
    for x in dir(self.fields['new_password1']):
        print(x)


class ChangePasswordForm(PasswordChangeForm):
    error_messages = {'password_mismatch': 'حقلي كلمة المرور غير متطابقين.',
                      'password_incorrect': 'تم إدخال كلمة المرور القديمة بشكل غير صحيح. يرجى إدخاله مرة أخرى.'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'كلمة المرور القديمة'
        self.fields['new_password1'].label = 'كلمة المرور الجديدة'
        self.fields['new_password1'].help_text = '''
                    <ul class='text-right'>
                        <li>يجب أن تكون كلمة المرور الخاصة بك على الأقل 8 حرورف</li>
                        <li> يجب إستخدام الأبجدية الإنجليزية A-Z , a-z</li>
                        <li>يجب أن تحتوي كلمة المرور على الأقل على حرف أبجدي صغير وحرف كبير</li>
                        <li>يجب أن تحتوي كلمة المرور على الأقل على رقم واحد و رمز واحد مثل 
                        :
                        <br />
                        ()[\]{}|\\`~!@#$%^&*_",<>./? .</li>
                    </ul>
                    '''

        self.fields['new_password2'].label = 'تأكيد كلمة المرور الجديدة'

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


class MyPasswordResetForm(PasswordResetForm):
    pass
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     qs = User.objects.filter(email=email)
    #     if not qs.count() == 1:
    #         raise forms.ValidationError(
    #             'لا يوجد حساب مسجل مع هذا البريد الإلكتروني')
    #     return email
