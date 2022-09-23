from django import template
from ..models import ArticleCategory, Article
from django.db.models import Count, Q
from datetime import datetime, timedelta

register = template.Library()

@register.inclusion_tag('parsials/last_month.html')
def last_month_view(request):
	last_month = datetime.today() - timedelta(days=30)
	return{
		'request': request,
		'last_month_view' : Article.objects.published().annotate(count=Count('hits', filter = Q(articlehit__created__gt=last_month))).order_by('-count', '-publish')[:5],
		'hot_Article' : Article.objects.published().annotate(count=Count('comments', filter = Q(comments__posted__gt=last_month) and Q(comments__content_type_id=7))).order_by('-count', '-publish')[:5],
	}


@register.inclusion_tag('parsials/category.html')
def category_navbar():
	return {
		'category' : ArticleCategory.objects.filter(status=True)
	}

