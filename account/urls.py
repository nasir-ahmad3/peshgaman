from django.contrib.auth import views
from django.urls import path
from .views import( 
    Home, 
    ArticleCreate, 
    GraphCreate,
    GraphList, 
    CategoryList, 
    CategoryCreate, 
    ArticleUpdate, 
    CategoryUpdate, 
    GraphUpdate, 
    ArticleDelete, 
    GraphDelete, 
    CategoryDelete,
    Profile,
    Registeration,
    activate,
)

app_name = 'account'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('article/create/', ArticleCreate.as_view(), name='article-create'),
    path('article/delete/<int:pk>/', ArticleDelete.as_view(), name="article-delete"),
    path('article/update/<int:pk>/', ArticleUpdate.as_view(), name="article-update" ),

	path('graph/list/', GraphList.as_view(), name='graphـlist'),
    path('graph/create/', GraphCreate.as_view(), name='graph-create'),
    path('graph/update/<int:pk>/', GraphUpdate.as_view(), name='graph-update'),
    path('graph/delete/<int:pk>/', GraphDelete.as_view(), name='graph-delete'),

    path('category/list/', CategoryList.as_view(), name='category-list'),
    path('category/create/', CategoryCreate.as_view(), name="category-create"),
    path('category/update/<int:pk>/', CategoryUpdate.as_view(), name="category-update" ),
    path('category/delete/<int:pk>/', CategoryDelete.as_view(), name='category-delete'),

    path('profile/', Profile.as_view(), name="profile")

]
