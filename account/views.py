from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from blog.models import Article, Graph, ArticleCategory
from .models import User
from .forms import UserForms
from django.views.generic import (
	ListView, 
	CreateView, 
	UpdateView, 
	DeleteView
)
from .mixins import (
	ArticleFieldMixin, 
	FormValidMixins, 
	CategoryFieldMixin, 
	CategoryFormValidMixins, 
	UserAccessMixin, 
	CategoryUserAccessMixin, 
	SuperSuerAccessMixin,
	AuthorsMixins
)
from django.shortcuts import render, redirect
from blog.models import Article
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_str


# Create your views here.
class Home(LoginRequiredMixin, AuthorsMixins, ListView):

	template_name ="registration/home.html"
	def get_queryset(self):
		if (self.request.user.is_superuser):
			return Article.objects.all()
		else:
			return Article.objects.filter(user=self.request.user)


class ArticleCreate(LoginRequiredMixin, AuthorsMixins, FormValidMixins, ArticleFieldMixin ,CreateView):
	model = Article
	template_name = "registration/article-create-update.html"


class ArticleUpdate(UserAccessMixin, AuthorsMixins, FormValidMixins, ArticleFieldMixin, UpdateView):
	model = Article
	template_name = "registration/article-create-update.html"


class ArticleDelete(SuperSuerAccessMixin, AuthorsMixins, DeleteView):
	model = Article
	success_url = reverse_lazy('account:home')
	template_name = "registration/article_confirm_delete.html"



class GraphList(LoginRequiredMixin, AuthorsMixins, ListView):
	queryset = Graph.objects.all()
	template_name ="registration/graph_list.html"


class GraphCreate(LoginRequiredMixin, AuthorsMixins, CreateView):
	model = Graph
	template_name = 'registration/graph-create-update.html'
	fields = ['title', 'graph_name_1', 'graph_image_1', 'graph_number_1', 'graph_name_2', 'graph_image_2', 'graph_number_2', 'graph_name_3', 'graph_image_3', 'graph_number_3', 'graph_name_4', 'graph_image_4', 'graph_number_4', 'graph_name_5', 'graph_image_5', 'graph_number_5', 'graph_name_6', 'graph_image_6', 'graph_number_6', 'graph_name_7', 'graph_image_7', 'graph_number_7', 'graph_name_8', 'graph_image_8', 'graph_number_8', 'graph_name_9', 'graph_image_9', 'graph_number_9', 'graph_name_10', 'graph_image_10', 'graph_number_10']


class GraphUpdate(LoginRequiredMixin, AuthorsMixins, SuperSuerAccessMixin, UpdateView):
	model = Graph
	template_name = 'registration/graph-create-update.html'
	fields = ['title', 'graph_name_1', 'graph_image_1', 'graph_number_1', 'graph_name_2', 'graph_image_2', 'graph_number_2', 'graph_name_3', 'graph_image_3', 'graph_number_3', 'graph_name_4', 'graph_image_4', 'graph_number_4', 'graph_name_5', 'graph_image_5', 'graph_number_5', 'graph_name_6', 'graph_image_6', 'graph_number_6', 'graph_name_7', 'graph_image_7', 'graph_number_7', 'graph_name_8', 'graph_image_8', 'graph_number_8', 'graph_name_9', 'graph_image_9', 'graph_number_9', 'graph_name_10', 'graph_image_10', 'graph_number_10']


class GraphDelete(SuperSuerAccessMixin, AuthorsMixins, DeleteView):
	model = Graph
	success_url = reverse_lazy('account:graphـlist')
	template_name = "registration/graph_confirm_delete.html"




class CategoryList(LoginRequiredMixin, AuthorsMixins, ListView):
	queryset = ArticleCategory.objects.all() 
	template_name ="registration/category_list.html"


class CategoryCreate(LoginRequiredMixin, AuthorsMixins, CategoryFieldMixin, CategoryFormValidMixins, CreateView):
	model = ArticleCategory
	template_name = 'registration/create-update-category.html'


class CategoryUpdate(CategoryUserAccessMixin, AuthorsMixins, CategoryFieldMixin, CategoryFormValidMixins, UpdateView):
	model = ArticleCategory
	template_name = 'registration/create-update-category.html'


class CategoryDelete(SuperSuerAccessMixin, AuthorsMixins, DeleteView):
	model = ArticleCategory
	success_url = reverse_lazy('account:category-list')
	template_name = "registration/category_confirm_delete.html"


class Profile(LoginRequiredMixin, UpdateView):
	model = User 
	success_url = reverse_lazy('account:profile')
	template_name = 'registration/profile.html'
	form_class = UserForms

	def get_object(self):
		return User.objects.get(pk=self.request.user.pk)
	
	def get_form_kwargs(self):
		kwargs = super(Profile, self).get_form_kwargs()
		kwargs.update({
			'user' : self.request.user
		})
		return kwargs


class Login(LoginView):
	def get_success_url(self):
		if self.request.user.is_superuser or self.request.user.is_author:
			return reverse_lazy('account:home')	
		else:
			return reverse_lazy('account:profile')	

from .forms import RegistationForm


class Registeration(CreateView):
	form_class = RegistationForm
	template_name = 'registration/register.html'

	def form_valid(self, form):
		user = form.save(commit=False)
		user.is_active = False
		user.save()
		current_site = get_current_site(self.request)
		mail_subject = 'فعال سازس اکونت شما'
		message = render_to_string('registration/acc_active_email.html', {
			'user': user,
			'domain': current_site.domain,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			'token':account_activation_token.make_token(user),
		})
		to_email = form.cleaned_data.get('email')
		email = EmailMessage(
					mail_subject, message, to=[to_email]
		)
		email.send()
		return HttpResponse('برای ادامه ثبت نام لطفا ایمیل خود را تایید کنید')



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
