from django.urls import path
from . import views


urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),

    path('profile/<str:pk>/', views.UpdateAuthor.as_view(), name='updateauthor'),

    path('category/', views.CategoryCreate.as_view(), name='category'),

    path('editcat/<int:pk>/', views.EditCategory.as_view(), name='editcat'),

    path('cat/delete/<int:pk>/', views.delete_category, name='deletecat'),

    path('media/', views.MediaUpload.as_view(), name='media'),

    path('editmedia/<int:pk>/', views.EditMedia.as_view(), name='editmedia'),

    path('media/delete/<int:pk>/', views.delete_media, name='deletemedia'),

    path('newpost/', views.PostCreate.as_view(), name='newpost'),

    path('allposts/', views.view_posts, name='posts'),

    path('post/delete/<int:pk>/', views.delete_posts, name='deletepost'),

    path('editpost/<int:pk>/', views.EditPost.as_view(), name='editpost'),

    path('quote/', views.QuoteCreate.as_view(), name='quote'),

    path('editquote/<int:pk>/', views.EditQuote.as_view(), name='editquote'),

    path('quote/delete/<int:pk>/', views.delete_quote, name='deletequote'),

    path('read/<slug:slug>/', views.PostDetailView.as_view(), name='read'),

    path('tag/<slug:slug>/', views.tagged, name='tag'),

    path('', views.index, name='index'),

    path('theme/<slug:slug>/',
         views.CategoryArticleView.as_view(), name='categoryarticles'),

    path('search/', views.SearchResultsView.as_view(), name='search'),

    path('comments/', views.CommentManage.as_view(), name='comments'),

    path('editcomment/<int:pk>/', views.edit_comment, name='editcomment'),

    path('comment/delete/<int:pk>/', views.delete_comment, name='deletecomment'),
]