from django.shortcuts import redirect, render
from django.views import View

from .forms import UserCreationForm


class UserSignUp(View):
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, "registration/signup.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
            return redirect("account:login")
        return render(request, "registration/signup.html", {"form": form})
