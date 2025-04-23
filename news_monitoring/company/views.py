from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from news_monitoring.company import models


def add_company(request):
    """
    Handle the process of adding a new company.

        - If the request method is POST, it extracts the 'name' and 'domain' from the form data.
        - Validates that both fields are provided.
        - If the user is authenticated, the company is associated with the user via 'added_by'.
        - Otherwise, 'added_by' is set to None.
        - After successful creation, displays a success message and redirects to the same page.
        - If the request method is not POST, renders the company addition form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template or a redirect response.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        domain = request.POST.get("domain")

        if not name or not domain:
            return render(
                request,
                "company/add_company.html",
                {"error": "All fields are required!"},
            )

        if request.user.is_authenticated:
            added_by = request.user
        else:
            added_by = None

        models.Company.objects.create(name=name, domain=domain, added_by=added_by)
        messages.success(request, "Company Added Succesfully")
        return redirect("company:add_company")

    return render(request, "company/add_company.html")


def search_companies(request):
    """
    Search for companies based on a query string or a list of company IDs.

    - If 'ids' is provided in the GET parameters, returns companies matching those IDs.
    - If 'q' (query) is provided, performs a case-insensitive partial match search on the company name.
    - If neither is provided, returns an empty result set.
    - The result is returned as a JSON response with each company represented by its ID and name.

    GET Parameters:
        q (str, optional): A search keyword to filter companies by name.
        ids (str, optional): A comma-separated list of company IDs to retrieve specific companies.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON array of matching companies with fields 'id' and 'name'.
    """
    query = request.GET.get("q", "").strip()
    ids = request.GET.get("ids", "")

    if ids:
        ids_list = [int(i) for i in ids.split(",") if i.isdigit()]
        companies = models.Company.objects.filter(id__in=ids_list)
    elif query:
        companies = models.Company.objects.filter(name__icontains=query)
    else:
        companies = models.Company.objects.none()

    data = list(companies.values("id", "name"))
    return JsonResponse(data, safe=False)
