from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('register/',views.register,name='register'),
    path('', include('django.contrib.auth.urls')),
    path('',views.news_today,name='newsToday'),
    path('archives/<int:year>/<int:month>/<int:day>/',views.past_days_news,name='pastNews'),
    path('search/',views.search_results,name='search_results'),
    path('article/<int:article_id>/',views.article,name='article'),
    path('new/article/', views.new_article, name='new-article'),
    path('ajax/newsletter/',views.newsletter,name='newsletter'),
    path('api/merch/',views.MerchList.as_view()),
    path('api/merch/<int:pk>/',views.MerchDescription.as_view()),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)