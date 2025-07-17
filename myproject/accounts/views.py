from django.contrib.auth import login as auth_login
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render

from .forms import SignUpForm


class SignUpResponse(HttpResponse):
    pass
    # maybe make a factory method to create one from HttpResponse
    # or
    # make the new response only accepts the another HttpResponse in the constructort
    # then just make assertions that the context has the required fields
    # no additional functionality would be added
    # it's also possible to use the SignUpProps or make a public field on the SignUpResponse
    # Class


class SignupProps:
    def __init__(self, form: SignUpForm):
        self.form = form


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", SignupProps(form).__dict__)
