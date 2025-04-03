from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from news_monitoring.company.models import Company
from news_monitoring.story.models import Story


def fetch_story_obj(user, story_id):
    # Optimize Query: Select related company only for non-staff users
    story_qs = Story.objects.prefetch_related("tagged_companies")

    if not user.is_staff:
        story_qs = story_qs.select_related("company")

    # Get the story object with pre-fetched tagged companies
    story_obj = get_object_or_404(story_qs, id=story_id)

    # Extract company IDs efficiently
    tagged_companies = list(story_obj.tagged_companies.values_list("id", flat=True))

    return story_obj, tagged_companies


def fetch_story_qs(user):
    """Fetches stories efficiently based on user role."""
    stories_qs = Story.objects.select_related("company").prefetch_related("tagged_companies")

    return stories_qs if user.is_staff else stories_qs.filter(company=user.company)


def validate_form_data(user, payload, story_id):
    story_data_tuple = (None, None)
    print(payload)
    title = payload.get("title")
    body_text = payload.get("body_text")
    published_date = payload.get("published_date")
    article_url = payload.get("article_url")
    tagged_companies = payload.getlist("tagged_companies")
    is_validated = False

    if title and article_url:
        is_validated = True
        if story_id:
            story_data_tuple = fetch_story_obj(user, story_id)
        update_or_create_story(story_data_tuple[0], user, title, body_text, published_date, article_url,
                               tagged_companies)
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
        story = Story.objects.create(
            title=title,
            body_text=body_text,
            article_url=article_url,
            published_date=published_date,
            added_by=user,
            company=user.company,
        )

    story.tagged_companies.set(tagged_companies)


def get_stories(user, query_dict):
    search_query = query_dict.get('q', '').strip()
    filter_date = query_dict.get('date', '').strip()

    stories_qs = fetch_story_qs(user)

    if search_query:
        stories_qs = stories_qs.filter(title__icontains=search_query)

    if filter_date:
        stories_qs = stories_qs.filter(published_date=filter_date)

    return [
        {
            "id": story.id,
            "title": story.title,
            "article_url": story.article_url,
            "published_date": story.published_date.strftime('%Y-%m-%d'),
            "body_text": story.body_text[:100] + "..." if len(story.body_text) > 100 else story.body_text,
            "tagged_companies": []  # [company.name for company in css.tagged_companies.all()]
        }
        for story in stories_qs[:10]  # Limit results for performance
    ]


def get_filtered_stories(user, search_query, filter_date):
    """Fetch and filter stories based on search query and date."""
    stories_qs = Story.objects.all() if user.is_staff else Story.objects.filter(company=user.company)

    if search_query:
        stories_qs = stories_qs.filter(title__icontains=search_query)
    if filter_date:
        stories_qs = stories_qs.filter(published_date=filter_date)

    stories_qs = stories_qs.select_related("company").prefetch_related(
        Prefetch("tagged_companies", queryset=Company.objects.only("id", "name"))
    ).only("id", "title", "article_url", "published_date", "body_text", "company_id")

    return stories_qs.prefetch_related("tagged_companies")


def get_stories_json(stories_qs, page_number):
    """Paginate and return JSON response for AJAX requests."""
    paginator = Paginator(stories_qs, 10)
    page_obj = paginator.get_page(page_number)

    return JsonResponse({
        "stories": [
            {
                "id": story.id,
                "title": story.title,
                "article_url": story.article_url,
                "published_date": story.published_date.strftime('%Y-%m-%d'),
                "body_text": story.body_text[:100] + "..." if len(story.body_text) > 100 else story.body_text,
                "tagged_companies": [company.name for company in story.tagged_companies.all()]
            }
            for story in page_obj
        ]
    })
