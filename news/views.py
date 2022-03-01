from urllib import request
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.http import Http404,HttpResponse, HttpResponseRedirect
import datetime as dt
from django.shortcuts import render,redirect
from .models import Article, NewsLetterRecipients
from .forms import NewsLetterForm, NewsArticleForm
from .email import send_welcome_email
# from  django.contrib.auth import login,authenticate
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required


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

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = NewsLetterRecipients(name = name, email = email)
            recipient.save()
            send_welcome_email(name,email)
            HttpResponseRedirect('news_today')
    else:
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
    return render(request, 'all-news.article.html', {"article":article})

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