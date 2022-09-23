from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import Article, ArticleCategory
from account.models import User
from account.mixins import UserAccessMixin
from django.db.models import Q

# Create your views here.
class ArticleList(ListView):
	queryset = Article.objects.published()
	paginate_by = 6


class ArticleDetail(DetailView):

	def get_object(self):
		slug = self.kwargs.get('slug')
		article = get_object_or_404(Article.objects.published(), slug=slug)
			
		ip_address = self.request.user.ip_address
		if ip_address not in article.hits.all():
			article.hits.add(ip_address)

		return article


class ArticlePreview(UserAccessMixin, DetailView):

	def get_object(self):
		pk = self.kwargs.get('pk')
		article = get_object_or_404(Article, pk=pk)
		return article


class Category(ListView):
	paginate_by = 6
	template_name = 'blog/category_list.html'

	def get_queryset(self):
		global category
		slug = self.kwargs.get('slug')
		category = get_object_or_404(ArticleCategory.objects.Active(), slug=slug)
		return category.article.published()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['category'] =  category
		return context


class Author(ListView):
	paginate_by = 6
	template_name = 'blog/author_list.html'

	def get_queryset(self):
		global user
		username = self.kwargs.get('username')
		user = get_object_or_404(User, username=username)
		return user.article.published()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user'] =  user
		return context

class Search(ListView):
	paginate_by = 6
	template_name = 'blog/search_list.html'

	def get_queryset(self):
		global search
		search = self.request.GET.get('q')
		articles = Article.objects.filter(Q(description__icontains=search) | Q(title__icontains=search))
		return articles

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search'] =  search
		return context
