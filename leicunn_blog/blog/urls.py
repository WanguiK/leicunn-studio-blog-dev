from django.urls import path
from django.conf.urls import handler404, handler500
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

    path('add_comment/<int:pk>/', views.add_comment, name='add_comment'),

    path('author/<slug:slug>/', views.AuthorDetailView.as_view(), name='author'),

    path('add_opinion/<str:pk>/', views.create_opinion, name='create_opinion'),

    path('tag/<slug:slug>/', views.tagged, name='tag'),

    path('', views.index, name='index'),

    path('theme/<slug:slug>/',
         views.CategoryArticleView.as_view(), name='categoryarticles'),

    path('search/', views.SearchResultsView.as_view(), name='search'),

    path('comments/', views.CommentManage.as_view(), name='comments'),

    path('getcomment/<int:pk>/', views.get_comment, name='getcomments'),

    path('reply/<int:pk>/', views.reply, name='reply_comment'),

    path('geteditcomment/<int:pk>/', views.get_edit_comment, name='geteditcomment'),

    path('editcomment/<int:pk>/', views.edit_comment, name='editcomment'),

    path('comment/delete/<int:pk>/', views.delete_comment, name='deletecomment'),

    path('opinions/', views.OpinionManage.as_view(), name='opinions'),

    path('getopinion/<int:pk>/', views.get_opinion, name='getopinions'),

    path('opinion/delete/<int:pk>/', views.delete_opinion, name='deleteopinion'),

    path('replyopinion/<int:pk>/', views.reply_opinion, name='reply_opinion'),

    path('geteditopinion/<int:pk>/', views.get_edit_opinion, name='geteditopinion'),

    path('editopinion/<int:pk>/', views.edit_opinion, name='editopinion'),

    path('deletenotif/', views.delete_notification, name='deletenotif'),

    path('notifstatus/', views.read_status_notif, name='notifstatus'),

    path('register/', views.Register.as_view(), name='register'),

    path('author/delete/<slug:slug>/', views.delete_author, name='deleteauthor'),

    path('getpost/<int:pk>/', views.get_post, name='getpost'),

    path('authoraddcomment/<int:pk>/', views.author_add_comment, name='author_addcomment'),

    path('authoraddopinion/', views.author_add_opinion, name='author_addopinion'),
]

handler500 = views.error500
handler404 = views.error404