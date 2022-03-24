import requests

from datetime import datetime
from elasticsearch_dsl import Q as elastic_Q

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q as django_Q
from django.conf import settings

from .models import Post
from .documents import PostDocument


def generate_random_data():
    api_result = requests.get(f'https://my.api.mockaroo.com/elastic?key={settings.MOCKAROO_KEY}')
    count = 1
    api_response = api_result.json()
    for data in api_response:
        print(count)
        try:
            Post.objects.create(
                author=data.get('author'),
                title=data.get('title'),
                description=data.get('description'),
            )
        except Exception:
            continue
        count += 1


def index(request):
    return render(request, 'index.html')


def search_elastic(request):
    start_time = datetime.now()
    query = request.GET.get('q')
    q = elastic_Q('multi_match', query=query, fields=['title', 'author', 'description'], fuzziness='auto')
    search_res = PostDocument.search().extra(size=10000).query(q).to_queryset()
    return render(request, 'search.html', {'posts': search_res, 'time': datetime.now() - start_time})


def search_django(request):
    start_time = datetime.now()
    query = request.GET.get('q')
    search_res = Post.objects.all().filter(django_Q(title__contains=query) |
                                           django_Q(author__contains=query) |
                                           django_Q(description__contains=query))
    return render(request, 'search.html', {'posts': search_res, 'time': datetime.now() - start_time})