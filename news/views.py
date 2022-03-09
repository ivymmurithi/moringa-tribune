from re import M
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
import datetime as dt
from django.shortcuts import render,redirect
from .models import Article, NewsLetterRecipients,MoringaMerch
from .forms import NewsLetterForm, NewsArticleForm
from .email import send_welcome_email
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializer import MerchSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly

from news import serializer

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('news/')
    else:
        form = RegisterForm
    return render(request, 'registration/registration_form.html', {'form':form})

@login_required
def past_days_news(request,year,month,day):

    try:
        date = dt.datetime.strptime(f"{year}-{month}-{day}",'%Y-%m-%d').date()

    except ValidationError:
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)

    news = Article.days_news(date)
    
    return render(request, 'all-news/past-news.html',{"date":date, "news":news})

@login_required
def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    form = NewsLetterForm()
    return render(request, 'all-news/today-news.html', {"date":date,"news":news, "letterForm":form})

@login_required
def search_results(request):
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message, "articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})

@login_required
def article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
    except:
        raise Http404()
    return render(request, 'all-news/article.html', {"article":article})

@login_required
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect('newstoday')
    else:
        form = NewsArticleForm()
    return render(request, 'new_article.html', {'form':form})

@login_required
def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)

"""
In Class-based views, you have to call as_view() function 
so as to return a callable view that takes a request and
returns a response. Its the main entry-point in 
request-response cycle in case of generic views.
"""
class MerchList(APIView):
      # get method that will:
    def get(self, request, format=None):
        # query the database to get all the MoringaMerchobjects
        all_merch = MoringaMerch.objects.all() 
        # serialize the Django model objects and return the serialized data as a response
        serializers = MerchSerializer(all_merch, many=True)
        return Response(serializers.data)

    """
    request.data attribute, which is similar to request.POST, but more useful for working with Web APIs.

    request.POST # Only handles form data. Only works for 'POST' method.

    request.data # Handles arbitrary data. Works for 'POST', 'PUT' and 'PATCH' methods.
    """

    # request. data to access JSON data for 'POST', 'PUT' and 'PATCH' requests
    def post(self, request, format=None):
        serializers = MerchSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors)

class MerchDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get_merch(self, pk):
        try:
            return MoringaMerch.objects.get(pk=pk)
        except MoringaMerch.DoesNotExist:
            return Http404
            
    def get(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        merch = self.get_merch(pk)
        merch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)