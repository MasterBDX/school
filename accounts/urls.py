from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import MyPasswordResetForm
from .views import (register_view, login_view, logout_view,
                    UserEditView, MyPasswordChangeView,
                    users_activation_toggle_view, UserDeleteView)

app_name = 'accounts'
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user-<int:pk>/edit/', UserEditView.as_view(), name='profile_edit'),
    path('change-password/', MyPasswordChangeView.as_view(),
         name='password_change'),
    path('password-change-done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    path('activetion-toggle/status-<int:status>/',
         users_activation_toggle_view,
         name='activetion-toggle'),
    path('user-<int:pk>/activetion-toggle/status-<int:status>/',
         users_activation_toggle_view,
         name='user-activetion-toggle'),
    path('<int:pk>/delete/',
         UserDeleteView.as_view(),
         name='delete'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
                                                                 email_template_name='accounts/password_reset_email.html',
                                                                 subject_template_name='accounts/password_reset_subject.txt',
                                                                 form_class=MyPasswordResetForm,
                                                                 success_url=reverse_lazy('accounts:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',
                                                                                success_url=reverse_lazy('accounts:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]
