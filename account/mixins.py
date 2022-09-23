from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from blog.models import Article, ArticleCategory

# my mixins 

class ArticleFieldMixin():

	def dispatch(self, request, *args, **kwargs):
		if (self.request.user.is_superuser):
			self.fields = ['title', 'user', 'slug', 'Graph', 'category',
			 'description', 'thumbnail', 'publish', 'status']
		elif (self.request.user.is_author):
			self.fields = ['title', 'slug', 'Graph', 'category',
			 'description', 'thumbnail', 'publish']
		else :
			raise Http404
		return super().dispatch(request, *args, **kwargs)


class FormValidMixins():
	def form_valid(self, form):
		if (self.request.user.is_superuser):
			form.save()
		elif(self.request.user.is_author):
			self.obj = form.save(commit=False)
			self.obj.status = 'd'
			self.obj.user = self.request.user
		return super().form_valid(form)


class CategoryFieldMixin():

	def dispatch(self, request, *args, **kwargs):
		if (self.request.user.is_superuser):
			self.fields = ['title' ,'slug' ,'position' ,'status']
		elif (self.request.user.is_author):
			self.fields = ['title' ,'slug' ,'position']
		else :
			raise Http404
		return super().dispatch(request, *args, **kwargs)


class CategoryFormValidMixins():
	def form_valid(self, form):
		if (self.request.user.is_superuser):
			form.save()
		elif(self.request.user.is_author):
			self.obj = form.save(commit=False)
			self.obj.status = False
		return super().form_valid(form)

class UserAccessMixin():
	def dispatch(self, request, pk, *args, **kwargs):
		article = get_object_or_404(Article, pk=pk)

		if (self.request.user.is_superuser or( article.user == self.request.user and article.status=='d') ):
			return super().dispatch(request, pk, *args, **kwargs)
		else :
			raise Http404



class CategoryUserAccessMixin():
	def dispatch(self, request, pk, *args, **kwargs):
		category = get_object_or_404(ArticleCategory, pk=pk)

		if (self.request.user.is_superuser or category.status == False ):
			return super().dispatch(request, pk, *args, **kwargs)
		else :
			raise Http404


class SuperSuerAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if (self.request.user.is_superuser ):
			return super().dispatch(request, *args, **kwargs)
		else :
			raise Http404


class AuthorsMixins():
	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_superuser or self.request.user.is_author:
			return super().dispatch(request, *args, **kwargs)
		else :
			return redirect('account:profile')
