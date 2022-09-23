from django.urls import path
from .views import ArticleList, ArticleDetail, Category, Author, ArticlePreview, Search

app_name = 'blog'
urlpatterns = [
	path('', ArticleList.as_view(), name='home'),
	path('page/<int:page>/', ArticleList.as_view(), name='home'),
	path('detail/<slug:slug>/', ArticleDetail.as_view(), name='detail'),
	path('preview/<int:pk>/', ArticlePreview.as_view(), name='preview'),
	path('category/<slug:slug>/', Category.as_view(), name='category'),
	path('category/<slug:slug>/page/<int:page>/', Category.as_view(), name='category'),
	path('author/<slug:username>/', Author.as_view(), name='author'),
	path('author/<slug:username>/page/<int:page>/', Author.as_view(), name='author'),
	path('search/', Search.as_view(), name='search'),
	path('search/page/<int:page>/', Search.as_view(), name='search'),
]
