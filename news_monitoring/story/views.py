
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from news_monitoring.source.models import Source

from .models import Story
from .services import fetch_story_obj, validate_form_data, update_or_create_story, fetch_story_qs
from ..company.models import Company


@login_required
def add_or_edit(request, story_id=None):
    companies = Company.objects.all()
    story_obj = None
    tagged_companies = []

    if story_id:
        story_obj, tagged_companies = fetch_story_obj(request.user, story_id)

    if request.method == "POST":
        is_validated = validate_form_data(request.user, request.POST, story_obj)

        if not is_validated:
            return render(
                request,
                "story/add_story.html",
                {
                    "error": "Title and URL are required!",
                    "companies": companies,
                    "story": story_obj,  # Pass story data if editing
                    "tagged_companies": tagged_companies
                },
            )
        return redirect("story:list")

    return render(
        request,
        "story/add_story.html",
        {
            "companies": companies,
            "story": story_obj,
            "tagged_companies": tagged_companies.values_list("id", flat=True) if story_obj else [],
        }
    )

@login_required
def list(request):
    """List stories based on user role."""
    stories_qs = fetch_story_qs(request.user)
    print(stories_qs)
    paginator = Paginator(stories_qs, 10)  # Show 10 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'story/list_stories.html', {'stories': page_obj})
    # return render(request, "story/list_stories.html", {"stories": fetch_story_qs(request.user)})

@login_required
def delete(request, story_id):
    story = get_object_or_404(Story, id=story_id, added_by=request.user)
    story.delete()
    messages.success(request, "Story deleted successfully.")
    return redirect("story:list")

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# API
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@login_required
def autocomplete_stories(request):
    """API endpoint for jQuery autocomplete"""
    search_query = request.GET.get('q', '').strip()

    if search_query:
        stories_qs = fetch_story_qs(request.user).filter(title__icontains=search_query)
        suggestions = list(stories_qs.values_list('title', flat=True)[:10])  # Limit results to 10
    else:
        suggestions = []

    return JsonResponse(suggestions, safe=False)

@login_required
def search_stories(request):
    """API endpoint for live search"""
    search_query = request.GET.get('q', '').strip()
    filter_date = request.GET.get('date', '').strip()

    stories_qs = fetch_story_qs(request.user)

    if search_query:
        stories_qs = stories_qs.filter(title__icontains=search_query)

    if filter_date:
        stories_qs = stories_qs.filter(published_date=filter_date)

    results = [
        {
            "id": story.id,
            "title": story.title,
            "article_url": story.article_url,
            "published_date": story.published_date.strftime('%Y-%m-%d'),
            "body_text": story.body_text[:100] + "..." if len(story.body_text) > 100 else story.body_text,
            "tagged_companies": [company.name for company in story.tagged_companies.all()]
        }
        for story in stories_qs[:10]  # Limit results for performance
    ]

    return JsonResponse({"stories": results})
