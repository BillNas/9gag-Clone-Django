from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from posts.views import PostCreateView,index,category,deletePost, updatePost,random_post, post, like, dislike, like_comment, dislike_comment
from users.views import register, profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('random/', random_post, name='random'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', register, name='signup'),
    path('upload/', PostCreateView.as_view(template_name='upload.html'), name='upload'),
    path('update/<str:post_id>/', updatePost, name='update'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
     path('u/<str:username>/', profile, name='profile'),
    path('gag/<str:post_id>/', post, name='post'),
    path('gag/<str:post_id>/like/', like, name='like'),
    path('gag/<str:post_id>/dislike/', dislike, name='dislike'),
    path('gag/<str:post_id>/like/<int:comment_id>/', like_comment, name='like_comment'),
    path('gag/<str:post_id>/dislike/<int:comment_id>/',
         dislike_comment, name='dislike_comment'),
    path('<str:categories>/', category, name='category'),
    path('delete/<str:post_id>',deletePost,name='delete')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
