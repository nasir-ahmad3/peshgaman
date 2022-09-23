from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse 
from account.models import User
from comment.models.comments import Comment
from django.contrib.contenttypes.fields import GenericRelation

# my Managers
class CategoryManager(models.Manager):
	def Active(self):
		return self.filter(status=True)


class ArticleManager(models.Manager):
	def published(self):
		return self.filter(status='p')

# Create your models here.
class GetIpAddress(models.Model):
	ip_address = models.GenericIPAddressField(verbose_name="آی پی ادرس")

	def __str__(self):
		return str(self.ip_address)

	class Meta:
		verbose_name="ای پی"
		verbose_name_plural="ای پی ها"

class Graph(models.Model):
	title = models.CharField(max_length=200, verbose_name="عنوان گراف")

	graph_name_1 = models.CharField(max_length=200, verbose_name='نام گراف 1')
	graph_image_1 = models.ImageField(upload_to="images", verbose_name="عکس گراف 1")
	graph_number_1 = models.IntegerField(verbose_name="مقدار گراف 1")

	graph_name_2 = models.CharField(max_length=200, verbose_name='نام گراف 2')
	graph_image_2 = models.ImageField(upload_to="images", verbose_name="عکس گراف 2")
	graph_number_2 = models.IntegerField(verbose_name="مقدار گراف 2")

	graph_name_3 = models.CharField(max_length=200, verbose_name='نام گراف 3')
	graph_image_3 = models.ImageField(upload_to="images", verbose_name="عکس گراف 3")
	graph_number_3 = models.IntegerField(verbose_name="مقدار گراف 3")

	graph_name_4 = models.CharField(max_length=200, verbose_name='نام گراف 4')
	graph_image_4 = models.ImageField(upload_to="images", verbose_name="عکس گراف 4")
	graph_number_4 = models.IntegerField(verbose_name="مقدار گراف 4")

	graph_name_5 = models.CharField(max_length=200, verbose_name='نام گراف 5')
	graph_image_5 = models.ImageField(upload_to="images", verbose_name="عکس گراف 5")
	graph_number_5 = models.IntegerField(verbose_name="مقدار گراف 5")

	graph_name_6 = models.CharField(max_length=200, verbose_name='نام گراف 6')
	graph_image_6 = models.ImageField(upload_to="images", verbose_name="عکس گراف 6")
	graph_number_6 = models.IntegerField(verbose_name="مقدار گراف 6")

	graph_name_7 = models.CharField(max_length=200, verbose_name='نام گراف 7')
	graph_image_7 = models.ImageField(upload_to="images", verbose_name="عکس گراف 7")
	graph_number_7 = models.IntegerField(verbose_name="مقدار گراف 7")

	graph_name_8 = models.CharField(max_length=200, verbose_name='نام گراف 8')
	graph_image_8 = models.ImageField(upload_to="images", verbose_name="عکس گراف 8")
	graph_number_8 = models.IntegerField(verbose_name="مقدار گراف 8")

	graph_name_9 = models.CharField(max_length=200, verbose_name='نام گراف 9')
	graph_image_9 = models.ImageField(upload_to="images", verbose_name="عکس گراف 9")
	graph_number_9 = models.IntegerField(verbose_name="مقدار گراف 9")

	graph_name_10 = models.CharField(max_length=200, verbose_name='نام گراف 0')
	graph_image_10 = models.ImageField(upload_to="images", verbose_name="عکس گراف 0")
	graph_number_10 = models.IntegerField(verbose_name="مقدار گراف 0")

	def get_absolute_url(self):
		return reverse ('account:graphـlist')
 
	def __str__(self):
		return self.title

	class Meta():
		verbose_name='گراف'
		verbose_name_plural='گراف ها'


class ArticleCategory(models.Model):
	title = models.CharField(max_length=200, verbose_name="عنوان")
	slug = models.SlugField(unique=True, verbose_name="آدرس")
	position = models.IntegerField(verbose_name="پوزیشن")
	status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse ('account:category-list')

	class Meta:
		verbose_name="دسته بندی"
		verbose_name_plural="دسته بندی ها"

	objects = CategoryManager()


class Article(models.Model):
	STATUS_CHOICES = (
		('p', 'منتشر شده'),
		('d', 'پیش نویس'),
	)
	title = models.CharField(max_length=200, verbose_name="عنوان")
	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="article", verbose_name="نویسنده")
	slug = models.SlugField(unique=True, verbose_name="آدرس")
	comments = GenericRelation(Comment)
	Graph = models.ForeignKey(Graph, null=True, blank=True, on_delete=models.SET_NULL, related_name='graph', verbose_name="گراف")
	category = models.ManyToManyField(ArticleCategory, verbose_name="دسته بندی", related_name="article")
	description = models.TextField(verbose_name="توضیحات")
	thumbnail = models.ImageField(upload_to='images', verbose_name="عکس بندانگشتی")
	publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")
	hits = models.ManyToManyField(GetIpAddress, through='articlehit', blank=True, verbose_name="بازدی ها")

	def __str__(self):
		return self.title

	def category_to_str(self):
		return ' ,'.join([ cate.title for cate in self.category.Active() ])
	category_to_str.short_description="دسته بندی ها"

	def show_thumbnail(self):
		return format_html('<img src="{}" width=200px; style="border-radius:5px;">'.format(self.thumbnail.url))
	show_thumbnail.short_description="عکس بندانگشتی"

	def get_absolute_url(self):
		return reverse ('account:home')

	class Meta():
		verbose_name="مقاله"
		verbose_name_plural="مقالات"
		ordering = ['-publish']


	objects = ArticleManager()


class ArticleHit (models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	ip_address = models.ForeignKey(GetIpAddress, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)