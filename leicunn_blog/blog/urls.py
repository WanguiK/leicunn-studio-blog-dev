from django.urls import path
from . import views


urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),

    path('updateprofile/<str:pk>/', views.UpdateAuthor.as_view(), name='updateauthor'),

    path('category/', views.CategoryCreate.as_view(), name='category'),

    # path('newpost/', views.PostCreate, name='newpost'),

    path('newpost/', views.PostCreate.as_view(), name='newpost'),
    
    path('allposts/', views.view_posts, name='posts'),

    # path('', views.index, name='index'),

    # path('editpost/<int:pk>/', views.EditPost.as_view(), name='editpost'),

    # path('read/<slug:slug>/', views.PostDetailView.as_view(), name='read'),

    # path('profile/<str:pk>/', views.ViewEditor.as_view(), name='vieweditor'),

    # path('category/<slug:slug>/',
    #      views.CategoryArticleView.as_view(), name='categoryarticles')
]