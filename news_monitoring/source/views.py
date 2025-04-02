
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from news_monitoring.company.models import Company
from news_monitoring.source.models import Source
from news_monitoring.source.services import fetch_source_obj, validate_form_data, fetch_source_qs


@login_required
def add_or_edit_source(request, source_id=None):
    user = request.user
    companies = Company.objects.all()

    source_obj = None
    tagged_companies = []

    if request.method == "POST":
        is_validated, msg = validate_form_data(user, request.POST, source_id)
        print(is_validated)

        if not is_validated:
            # messages.error(request, "Name and URL are required!")
            render(
                request,
                "source/add_source.html",
                {
                    "error": "Name and URL are required!",
                    "source": source_obj,
                    "companies": companies,
                    "tagged_companies": tagged_companies.values_list("id", flat=True) if tagged_companies else []
                }
            )
        else:
            return redirect("source:list")

    if source_id:
        source_obj, tagged_companies = fetch_source_obj(user, source_id)

    return render(
        request,
        "source/add_source.html",
        {
            "source": source_obj,
            "companies": companies,
            "tagged_companies": tagged_companies,  # Pass selected companies for pre-filling
        },
    )


@login_required
def list_sources(request):
    return render(request, "source/list_sources.html", {"sources": fetch_source_qs(request.user)})


@login_required
def delete_source(request, source_id):
    source = get_object_or_404(Source, id=source_id, added_by=request.user)

    if request.method == "POST":
        source.delete()
        messages.success(request, "Source deleted successfully.")
        return redirect("source:list")
    return redirect("source:list")
