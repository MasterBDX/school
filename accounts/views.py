
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth import (login, get_user_model, logout, authenticate)
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.utils.http import is_safe_url
from defender.decorators import watch_login
from django.utils.translation import get_language, ugettext as _,pgettext
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import (RegisterForm, LoginForm, UserEditForm, ChangePasswordForm)
from .decorators import anonymous_required,admin_only
from main.mixins import AdminPermission


User = get_user_model()

@login_required
@admin_only
def register_view(request):
    form = RegisterForm(request.POST or None)
    url = reverse('accounts:login')
    msg = _('You have been registered successfully Please wait for your account to be activated')

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            if request.user.is_authenticated:
                if request.user.is_admin:
                    obj.active = True
                    url = reverse('main:users-dashboard')
                    msg = _('User has been added successfully')
            obj.save()
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(url)
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@anonymous_required
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
                    remember_me = form.cleaned_data.get('remember_me', None)
                    if remember_me:
                        request.session.set_expiry(1209600)
                    next_ = request.POST.get('url')

                    if next_:
                        url_is_safe = is_safe_url(
                            url=next_,
                            allowed_hosts=settings.ALLOWED_HOSTS,
                            require_https=request.is_secure(),
                        )

                        if url_is_safe:
                            return redirect(next_)
                    return redirect('/')
                else:
                    return HttpResponse("Your account was inactive.")
            else:
                return HttpResponse("Invalid login details given")
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@login_required
def logout_view(request):    
    
    lang = request.session.get('lang')
    logout(request)
    request.session['lang'] = lang
    return HttpResponseRedirect(reverse('accounts:login'))


class UserEditView(LoginRequiredMixin,UpdateView):
    form_class = UserEditForm
    context_object_name = 'user_object'
    template_name = 'accounts/profile_edit.html'

    def get_object(self,queryset=None):
        obj = self.request.user
        return obj 


class MyPasswordChangeView(LoginRequiredMixin,auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('accounts:password_change_done')

@login_required
@admin_only
def users_activation_toggle_view(request, status, pk=None):
    text = _('Activate')
    users_status = User.objects.activetion_toggle(status, pk=pk)
    if users_status:
        text = _('Deactivate')
    if request.is_ajax:
        data = {'text': text, 'status': int(not bool(status))}
        return JsonResponse(data)
    return redirect('main:users-dashboard')


class UserDeleteView(LoginRequiredMixin,AdminPermission,DeleteView):
    queryset = User.objects.all_users()
    template_name = 'accounts/delete_user_confirm.html'
    success_url = reverse_lazy('main:users-dashboard')
