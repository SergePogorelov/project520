from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    """
    View for user sign-up.

    Allows users to register by creating a new account.
    """

    form_class = CreationForm
    template_name = "signup.html"

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request during user registration.

        Processes the form submission for user registration.
        Authenticates the user after successful registration and logs them in.

        :param request: HTTP request object sent by the client.
        :type request: HttpRequest
        :return: Redirects the user to the recipe list on successful registration.
        :rtype: HttpResponseRedirect
        """

        form = self.get_form()
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, user)
            return redirect("recipe_list")
        return render(request, "signup.html", {"form": form})
