from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from .models import Story
from .services import validate_form_data, get_filtered_stories, get_stories_json, fetch_story_obj
from ..company.models import Company


@login_required
def add_or_edit(request, story_id=None):
    story_obj = None
    tagged_companies = []
    companies = None

    if request.method == "POST":
        is_validated = validate_form_data(request.user, request.POST, story_id)

        if not is_validated:
            return render(
                request,
                "story/add_story.html",
                {
                    "error": "Title and URL are required!",
                    "story": story_obj,  # Pass css data if editing
                    "tagged_companies": tagged_companies
                },
            )
        return redirect("story:list")

    if story_id:
        story_obj, tagged_companies = fetch_story_obj(request.user, story_id)
        companies = Company.objects.filter(id__in=[company for company in tagged_companies])

    return render(
        request,
        "story/add_story.html",
        {
            "story": story_obj,
            "companies": companies,
            "tagged_companies": tagged_companies
        }
    )


@login_required
def list_stories(request):
    """List stories based on user role."""
    search_query = request.GET.get('q', '').strip()
    filter_date = request.GET.get('date', '').strip()
    page_number = request.GET.get('page')

    stories_qs = get_filtered_stories(request.user, search_query, filter_date)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return get_stories_json(stories_qs, page_number)

    paginator = Paginator(stories_qs, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, 'story/list_stories.html', {'stories': page_obj})


@login_required
def delete(request, story_id):
    story = get_object_or_404(Story, id=story_id, added_by=request.user)
    story.delete()
    messages.success(request, "Story deleted successfully.")
    return redirect("css:list")

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# API
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# @login_required
# def autocomplete_stories(request):
#     """API endpoint for jQuery autocomplete"""
#     search_query = request.GET.get('q', '').strip()
#
#     if search_query:
#         stories_qs = fetch_story_qs(request.user).filter(title__icontains=search_query)
#         suggestions = list(stories_qs.values_list('title', flat=True)[:10])  # Limit results to 10
#     else:
#         suggestions = []
#
#     return JsonResponse(suggestions, safe=False)


# @login_required
# def search_stories(request):
#     """API endpoint for live search"""
#     results = get_stories(request.user, request.GET)
#     return JsonResponse({"stories": results})
