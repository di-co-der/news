import feedparser
import time
from datetime import datetime
from bs4 import BeautifulSoup

from django.shortcuts import get_object_or_404

from news_monitoring.source.models import Source
from news_monitoring.story.models import Story


def fetch_source_qs(user):
    if user.is_staff:
        source_qs = Source.objects.all()  # Staff sees all sources
    else:
        source_qs = Source.objects.filter(company=user.company)
    return source_qs

def fetch_source_obj(user,source_id):
    if user.is_staff:
        source_obj = get_object_or_404(Source, id=source_id)
    else:
        source_obj = get_object_or_404(Source, id=source_id, company=user.company)

    tagged_companies = source_obj.tagged_companies.values_list("id", flat=True)
    return (source_obj, tagged_companies)


def update_or_create_source(source, user, name, url, company, tagged_companies):

    if source:
        source.name = name
        source.url = url
        source.company = company
        source.updated_by = user
        source.save()
    else:
        source = Source.objects.create(name=name, url=url, company=company, added_by=user)
    source.tagged_companies.set(tagged_companies)
    print(source)
    import_stories_from_feed(source, user)


def validate_form_data(user, payload, source_obj):
    name = payload.get("name")
    url = payload.get("url")
    company = user.company
    tagged_companies = list(map(int, payload.getlist("companies")))

    if name and url:
        update_or_create_source(source_obj, user, name, url, company, tagged_companies)
        return True
    else:
        return False


def import_stories_from_feed(source, user):
    """
    Parse the RSS feed from the source URL and create Story objects for each feed entry.
    Only creates stories that don't already exist based on article_url.
    """
    feed = feedparser.parse(source.url)

    for entry in feed.entries:

        if not Story.objects.filter(article_url=entry.link).exists():
            published_date = None

            if hasattr(entry, 'published_parsed'):
                published_date = datetime.fromtimestamp(time.mktime(entry.published_parsed))

            body_text = entry.get('summary', '')
            soup = BeautifulSoup(body_text, 'html.parser')
            body_text_cleaned = soup.get_text()

            story = Story.objects.create(
                title=entry.title,
                body_text=body_text_cleaned,
                article_url=entry.link,
                published_date=published_date,
                company=user.company,
                source=source,
                added_by=user
            )

            story.tagged_companies.set(source.tagged_companies.all())
