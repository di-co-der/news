from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from news_monitoring.source.models import Source

from .models import Story
from ..company.models import Company


@login_required
def add_or_edit(request, story_id=None):
    companies = Company.objects.all()  # Fetch all companies for tagging
    story = None

    if story_id:
        # Fetch the existing story or return 404
        story = get_object_or_404(Story, id=story_id, added_by=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        body_text = request.POST.get("body_text")
        published_date = request.POST.get("published_date")
        article_url = request.POST.get("article_url")
        selected_companies = request.POST.getlist("tagged_companies")

        # Validate required fields
        if not title or not body_text or not article_url:
            return render(
                request,
                "story/add_story.html",
                {
                    "error": "All fields are required!",
                    "companies": companies,
                    "story": story,  # Pass story data if editing
                    "selected_tagged_companies": selected_companies
                },
            )

        if story:
            # Update existing story
            story.title = title
            story.body_text = body_text
            story.published_date = published_date
            story.article_url = article_url
            story.updated_by = request.user
            story.save()
        else:
            # Create new story
            story = Story.objects.create(
                title=title,
                body_text=body_text,
                article_url=article_url,
                published_date=published_date,
                added_by=request.user,
                company=request.user.company,  # Assuming user has a company field
            )

        # Assign tagged companies
        story.tagged_companies.set(selected_companies)

        return redirect("story:list")

    return render(
        request,
        "story/add_story.html",
        {
            "companies": companies,
            "story": story,
            "selected_tagged_companies": story.tagged_companies.values_list("id", flat=True) if story else [],
        }
    )

@login_required
def list(request):
    """List stories based on user role."""
    if request.user.is_staff:
        stories = Story.objects.all()  # Staff sees all stories
    else:
        stories = Story.objects.filter(
            added_by=request.user,
        )  # Users see only their stories

    return render(request, "story/list_stories.html", {"stories": stories})

@login_required
def delete(request, story_id):
    story = get_object_or_404(Story, id=story_id, added_by=request.user)
    story.delete()
    messages.success(request, "Story deleted successfully.")
    return redirect("story:list")
