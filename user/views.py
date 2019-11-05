from django.views import View
from django.http import HttpRequest
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, UpdateProfile
from django.contrib import messages, auth
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpRequest





class SignUp(View):
    form_class = RegisterForm()

    def get(self, request):
        form = self.form_class
        return render(request, "./user/register.html", {"head": "Create Account", "form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "User Created")
            return redirect("/signin")
        else:
            return render(request, "./user/register.html", {"head": "Create Account", "form": form})


class SignIn(View):

    form_class = LoginForm()

    def get(self, request):
        form = self.form_class
        return render(request, "./registration/login.html", {"head": "Login here", "form": form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect("/auction")

        else:
            return render(request, "./registration/login.html", {"head": "LogIn", "form": form})


def signout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "Logged out successfully!")
    return redirect("/signin")


class EditProfile(View):
    def get(self, request, *args, **kwargs):
        form = UpdateProfile(user=request.user)
        return render(request, "./registration/update_profile.html", {"head": "Update Profile", "form": form})

    def post(self, request, *args, **kwargs):
        form = UpdateProfile(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            auth.update_session_auth_hash(request, user)
            messages.add_message(request, messages.INFO, 'Updated successfully!')
            return redirect("/auction")
        else:
            return render(request, "./registration/update_profile.html", {"head": "Update Profile", "form": form})

