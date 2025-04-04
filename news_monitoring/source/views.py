from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django import shortcuts

from news_monitoring.company import models as company_model
from news_monitoring.source import models as source_model
from news_monitoring.source import services


@login_required
def add_or_edit_source(request, source_id=None):
    user = request.user

    companies = None
    source_obj = None
    tagged_companies = []

    if request.method == "POST":
        is_validated, msg = services.validate_form_data(user, request.POST, source_id)

        if not is_validated:
            shortcuts.render(
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
            return shortcuts.redirect("source:list")

    if source_id:
        source_obj, tagged_companies = services.get_source(user, source_id)
        companies = company_model.Company.objects.all()

    return shortcuts.render(
        request,
        "source/add_source.html",
        {
            "source": source_obj,
            "companies": companies,
            "tagged_companies": tagged_companies,
        },
    )


@login_required
def list_sources(request):
    """List sources with search and pagination."""
    search_query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page')

    sources_qs = services.get_filtered_sources(request.user, search_query)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return services.get_sources_json(sources_qs, page_number)

    paginator = Paginator(sources_qs, 10)  # Show 10 sources per page
    page_obj = paginator.get_page(page_number)

    return shortcuts.render(request, "source/list_sources.html", {"sources": page_obj})


@login_required
def delete_source(request, source_id):
    source = shortcuts.get_object_or_404(source_model.Source, id=source_id, added_by=request.user)

    if request.method == "POST":
        source.delete()
        messages.success(request, "Source deleted successfully.")
        return shortcuts.redirect("source:list")
    return shortcuts.redirect("source:list")
