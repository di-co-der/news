from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
from django.shortcuts import redirect
from django.shortcuts import render

from ..company.models import Company
from .models import Source


@login_required
def add_or_edit_source(request, source_id=None):
    source = None
    selected_companies = []

    if source_id:
        # Fetch the source object (staff users can edit any source)
        if request.user.is_staff:
            source = get_object_or_404(Source, id=source_id)
        else:
            source = get_object_or_404(Source, id=source_id, added_by=request.user)

        # Get selected companies for pre-filling
        selected_companies = source.companies.values_list("id", flat=True)

    companies = Company.objects.all()  # Fetch all companies

    if request.method == "POST":
        name = request.POST.get("name")
        url = request.POST.get("url")
        selected_companies = list(
            map(int, request.POST.getlist("companies")),
        )  # Ensure IDs are integers

        if not name or not url:
            return render(
                request,
                "source/add_source.html",
                {
                    "error": "All fields are required!",
                    "source": source,
                    "companies": companies,
                    "selected_companies": selected_companies,  # Pass selected companies
                },
            )

        if source:
            # Updating existing source
            source.name = name
            source.url = url
            source.save()
        else:
            # Creating new source
            source = Source.objects.create(name=name, url=url, added_by=request.user)

        # Assign selected companies
        source.companies.set(selected_companies)

        return redirect("source:list")  # Redirect to source list

    return render(
        request,
        "source/add_source.html",
        {
            "source": source,
            "companies": companies,
            "selected_companies": selected_companies,  # Pass selected companies for pre-filling
        },
    )


@login_required
def list_sources(request):
    """List sources based on user role."""
    if request.user.is_staff:
        sources = Source.objects.all()  # Staff sees all sources
    else:
        sources = Source.objects.filter(
            added_by=request.user,
        )  # Users see only their sources

    return render(request, "source/list_sources.html", {"sources": sources})


@login_required
def delete_source(request, source_id):
    source = get_object_or_404(Source, id=source_id, added_by=request.user)

    if request.method == "POST":
        source.delete()
        messages.success(request, "Source deleted successfully.")
        return redirect("source:list")

    return redirect("source:list")
