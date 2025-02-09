from django.urls import path, include

from . import views

app_name = 'blog'

post_urls = [
    path('<int:post_id>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('create/', views.CreatePostView.as_view(), name='create_post'),
    path('<int:post_id>/edit/', views.EditPostView.as_view(),
         name='edit_post'),
    path('<int:post_id>/delete/', views.DeletePostView.as_view(),
         name='delete_post'),
    path('<post_id>/comment/', views.CreateCommentView.as_view(),
         name='add_comment'),
    path('<post_id>/edit_comment/<int:comment_id>/',
         views.EditCommentView.as_view(), name='edit_comment'),
    path('<post_id>/delete_comment/<int:comment_id>/',
         views.DeleteCommentView.as_view(), name='delete_comment'),
]

urlpatterns = [
    path('posts/', include(post_urls)),
    path('', views.IndexView.as_view(), name='index'),
    path('category/<slug:slug>/',
         views.CategoryDetailView.as_view(), name='category_posts'),
    path('profile/<str:username>/',
         views.UserProfileView.as_view(), name='profile'
         ),
    path('profile_edit/',
         views.EditUserProfileView.as_view(), name='edit_profile'
         ),
]
