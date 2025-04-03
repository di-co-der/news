from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from news_monitoring.company.models import Company
from news_monitoring.source.services import fetch_source_obj, validate_form_data, import_stories_from_feed, \
    get_filtered_sources, get_sources_json


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
            "tagged_companies": tagged_companies,
        },
    )


def list_sources(request):
    """List sources with search and pagination."""
    search_query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page')

    sources_qs = get_filtered_sources(request.user, search_query)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return get_sources_json(sources_qs, page_number)

    paginator = Paginator(sources_qs, 10)  # Show 10 sources per page
    page_obj = paginator.get_page(page_number)

    return render(request, "source/list_sources.html", {"sources": page_obj})


@login_required
def delete_source(request, source_id):
    source = get_object_or_404(Source, id=source_id, added_by=request.user)

    if request.method == "POST":
        source.delete()
        messages.success(request, "Source deleted successfully.")
        return redirect("source:list")
    return redirect("source:list")


from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Source


@csrf_exempt
def fetch_story(request, source_id):
    if request.method == "POST":
        source = get_object_or_404(Source, id=source_id)
        import_stories_from_feed(source, request.user)
    return redirect("source:list")
