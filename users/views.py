import random

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from users.forms import UserRegisterForm, UserProfileForm

from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='Подтверждение адреса электронной почты',
            message=f'Почта подтверждена, приятного пользования нашим магазином.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        # new_user.save()

        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        return self.request.user


def email_activate(request):
    return render(request, "users/email_activate.html")


def activate(request, uid):
    user = User.objects.filter(email_verify=int(uid)).first()
    user.is_active = True
    user.save()
    return redirect(reverse('blog:index'))


def restore_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        new_password = gen_verify_code()
        send_mail(
            subject='Восстановление пароля',
            message=f'Ваш новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse('users:login'))
    return render(request, "users/restore_password.html")


def gen_verify_code():
    return ('a'.join([str(random.randint(0, 9)) for i in range(5)]))
