from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from news_monitoring.source.models import Source

from .models import Story


@login_required
def add_story(request):
    sources = Source.objects.filter(added_by=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        source_id = request.POST.get("source")
        body_text = request.POST.get("body_text")
        article_url = request.POST.get("article_url")

        if not title or not body_text or not article_url or not source_id:
            return render(
                request,
                "story/add_story.html",
                {"error": "All fields are required!", "sources": sources},
            )

        source = Source.objects.get(id=source_id)

        Story.objects.create(
            title=title,
            source=source,
            body_text=body_text,
            article_url=article_url,
            added_by=request.user,
        )

        return redirect("story:list_stories")

    return render(request, "story/add_story.html", {"sources": sources})


@login_required
def list_stories(request):
    """List stories based on user role."""
    if request.user.is_staff:
        stories = Story.objects.all()  # Staff sees all stories
    else:
        stories = Story.objects.filter(
            added_by=request.user,
        )  # Users see only their stories

    return render(request, "story/list_stories.html", {"stories": stories})
