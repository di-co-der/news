import time
from datetime import datetime

import feedparser
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from news_monitoring.source.models import Source
from news_monitoring.story.models import Story


def fetch_source_qs(user):
    try:
        if user.is_staff:
            return Source.objects.all()  # Staff sees all sources
        return Source.objects.filter(company=user.company)
    except Exception as e:
        print(f"Error fetching sources: {e}")
        return Source.objects.none()


def fetch_source_obj(user, source_id):
    try:
        if user.is_staff:
            source_obj = get_object_or_404(Source, id=source_id)
        else:
            source_obj = get_object_or_404(Source, id=source_id, company=user.company)
        tagged_companies = source_obj.tagged_companies.values_list("id", flat=True)
        return (source_obj, tagged_companies)
    except ObjectDoesNotExist:
        print("Error: Source not found.")
        return (None, [])
    except Exception as e:
        print(f"Unexpected error fetching source object: {e}")
        return (None, [])


def update_or_create_source(user, name, url, company, tagged_companies, source=None):
    try:
        if source:
            source.name = name
            source.url = url
            source.company = company
            source.updated_by = user
            source.save()
        else:
            source = Source.objects.create(name=name, url=url, company=company, added_by=user)
        source.tagged_companies.set(tagged_companies)
        # import_stories_from_feed(source, user)
        return True
    except IntegrityError as e:
        print(f"Database error while updating/creating source: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error updating/creating source: {e}")
        return False


def validate_form_data(user, payload, source_id):
    try:
        source_data_tuple = (None, None)
        name = payload.get("name")
        url = payload.get("url")
        company = user.company
        tagged_companies = payload.getlist("tagged_companies")

        if name and url:
            if source_id:
                source_data_tuple = fetch_source_obj(user, source_id)
            update_or_create_source(user, name, url, company, tagged_companies, source_data_tuple[0])
            return True, "Success"
        return False, "Name and URL are required Fields."
    except Exception as e:
        print(f"Error validating form data: {e}")
        return False, "Error Occured"


def import_stories_from_feed(source, user):
    try:
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
    except feedparser.CharacterEncodingOverride as e:
        print(f"Error parsing feed: {e}")
    except Exception as e:
        print(f"Unexpected error importing stories: {e}")
