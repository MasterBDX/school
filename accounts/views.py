from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import (login, get_user_model, logout, authenticate)
from django.contrib.auth.views import LoginView

from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth import views as auth_views
from django.contrib import messages
from defender.decorators import watch_login

from .forms import (RegisterForm, LoginForm, UserEditForm, ChangePasswordForm)

User = get_user_model()


def register_view(request):
    form = RegisterForm(request.POST or None)
    url = reverse('accounts:login')
    msg = 'تم تسجيلك بنجاح يرجى الإنتظار حتى يتم تفعيل حسابك'

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            if request.user.is_authenticated:
                if request.user.is_admin:
                    obj.active = True
                    url = reverse('main:users-dashboard')
                    msg = 'تم إضافة المستخدم بنجاح'
            obj.save()
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(url)
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@watch_login()
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('main:home'))
                else:
                    return HttpResponse("Your account was inactive.")
            else:
                return HttpResponse("Invalid login details given")
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


# class UserLoginView(LoginView):
#     # form_class = LoginForm
#     template_name = 'accounts/register.html'


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))


class UserEditView(UpdateView):
    queryset = User.objects.all()
    form_class = UserEditForm
    context_object_name = 'user_object'
    template_name = 'accounts/profile_edit.html'


class MyPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('accounts:password_change_done')


def users_activation_toggle_view(request, status, pk=None):
    text = 'تنشيط'
    users_status = User.objects.activetion_toggle(status, pk=pk)
    if users_status:
        text = 'إلغاء تنشيط'
    if request.is_ajax:
        data = {'text': text, 'status': int(not bool(status))}
        return JsonResponse(data)
    return redirect('main:users-dashboard')


class UserDeleteView(DeleteView):
    queryset = User.objects.all_users()
    template_name = 'accounts/delete_user_confirm.html'
    success_url = reverse_lazy('main:users-dashboard')
