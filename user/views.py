from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm



class SignUp(View):
    form_class = RegisterForm()

    def get(self,request, *args, **kwargs):
        form = self.form_class
        return render(request, "./user/register.html", {"form": form})

    def post(self,request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/auction")

        return render(request, "./user/register.html", {"head": "Create Account", "form": form})


class SignIn(View):
    pass


def signout(request):
    pass


class EditProfile(View):
    pass
