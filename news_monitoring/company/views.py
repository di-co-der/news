from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
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

        # Check if the user is logged in
        if request.user.is_authenticated:
            # Create the company with the logged-in user's email as added_by
            added_by = request.user
        else:
            # Create the company with 'added_by' as None (Unknown user)
            added_by = None

        # Creating company with the appropriate 'added_by'
        Company.objects.create(name=name, domain=domain, added_by=added_by)

        # Redirect back to the page where the user came from
        # Using the HTTP_REFERER header to get the previous page URL
        # referer = request.META.get('HTTP_REFERER', 'home')  # Default to 'signup' if referer is not found
        # print(referer)
        messages.success(request,"Company Added Succesfully")
        return redirect("company:add_company")

    return render(request, "company/add_company.html")

def search_companies(request):
    """API endpoint to search companies."""
    query = request.GET.get("q", "").strip()
    companies = Company.objects.filter(name__icontains=query)[:10]  # Limit results to 10

    results = [{"id": company.id, "name": company.name} for company in companies]
    return JsonResponse(results, safe=False)
