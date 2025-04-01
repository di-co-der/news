from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from news_monitoring.company.models import Company
from news_monitoring.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


def signup(request):
    companies = Company.objects.all()  # Fetch all companies

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        company_id = request.POST.get("company")

        if password != confirm_password:
            return render(
                request,
                "users/signup.html",
                {"error": "Passwords do not match!", "companies": companies},
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "users/signup.html",
                {"error": "Email already in use!", "companies": companies},
            )

        # Assign company if selected
        company = None
        if company_id:
            company = Company.objects.get(id=company_id)

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            company=company,
        )
        user = authenticate(request, email=email, password=password)
        auth_login(request, user)

        return redirect("source:add")

    return render(request, "users/signup.html", {"companies": companies})


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            if (not user.added_sources.exists()):
                return redirect("source:add")
            return redirect("story:list")
        messages.error(request, "Invalid email or password!")

    return render(request, "users/login.html")


@login_required
def logout(request):
    """Logs out the user and redirects to the login page."""
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("users:login")
