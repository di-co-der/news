from django.shortcuts import redirect
from django.shortcuts import render

from .models import Company


def add_company(request):
    if request.method == "POST":
        name = request.POST.get("name")
        domain = request.POST.get("domain")

        if not name or not domain:
            return render(
                request,
                "company/add_company.html",
                {"error": "All fields are required!"},
            )

        # Creating company with 'added_by' as None (Unknown user)
        Company.objects.create(name=name, domain=domain, added_by=None)

        return redirect(
            "users:signup",
        )  # Redirect back to signup after adding a company

    return render(request, "company/add_company.html")
