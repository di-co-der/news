from django.shortcuts import get_object_or_404
from news_monitoring.story.models import Story


def fetch_story_obj(user,story_id):
    if user.is_staff:
        story_obj = get_object_or_404(Story, id=story_id)
    else:
        story_obj = get_object_or_404(Story, id=story_id, company=user.company)

    tagged_companies = story_obj.tagged_companies.values_list("id", flat=True)
    return (story_obj, tagged_companies)

def fetch_story_qs(user):
    if user.is_staff:
        stories_qs = Story.objects.all()
    else:
        stories_qs = Story.objects.filter(company=user.company)
    return stories_qs

def validate_form_data(user, payload, story):
    print(story)
    title = payload.get("title")
    body_text = payload.get("body_text")
    published_date = payload.get("published_date")
    article_url = payload.get("article_url")
    tagged_companies = payload.getlist("tagged_companies")
    is_validated = False
    if title and article_url:
        is_validated = True
        update_or_create_story(story, user, title, body_text, published_date, article_url, tagged_companies)
    return is_validated

def update_or_create_story(story, user, title, body_text, published_date, article_url, tagged_companies):
    if story:
        story.title = title
        story.body_text = body_text
        story.published_date = published_date
        story.article_url = article_url
        story.updated_by = user
        story.save()
    else:
        # Create new story
        story = Story.objects.create(
            title=title,
            body_text=body_text,
            article_url=article_url,
            published_date=published_date,
            added_by=user,
            company=user.company,
        )

    # Assign tagged companies
    story.tagged_companies.set(tagged_companies)
    pass
