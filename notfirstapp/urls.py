from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from notfirstapp import views

urlpatterns = patterns('',
	
	#login
	url(r'^login/',views.login_user, name="LoginPage"),
	url(r'^logout/$','django.contrib.auth.views.logout', {'next_page':'game:indexPage'},name="LogoutPage"),
	#signup
	url(r'^signup/',views.SignUpView.as_view(),name='SignUpPage'),

	#User
	url(r'^profile/(?P<pk>\d+)/$',views.ProfileView.as_view(),name='ProfilePage'),
	url(r'^profile/(?P<pk>\d+)/update/$',views.ProfileUpdateView.as_view(),name='ProfileUpdatePage'),

	#index page
	url(r'^$', views.IndexView.as_view(), name="indexPage"),
	# url(r'^(?P<game_id>\d+)/$', views.DetailPageController, name='DetailPage'),
	
	
	#manager part
	url(r'^manager/upload/$',login_required(views.GameCreateView.as_view()),name='GameFormPage'),
	url(r'^manager/gamearchive/upload/$',login_required(views.GameUploadView.as_view()),name='GameArchiveUploadPage'),
	url(r'^manager/(?P<pk>\d+)/$',login_required(views.GameDetailView.as_view()),name='GameDetailPage'),
	url(r'^manager/$',login_required(views.GameListView.as_view()),name='GameManagePage'),
	url(r'^manager/(?P<pk>\d+)/rank/$',login_required(views.ScoreRankView.as_view()),name='ScoreRankPage'),
	url(r'^manager/simplelist/$',TemplateView.as_view(template_name='game.html'),name='SimpleGameListPage'),
	
	
	#image part
	url(r'^image/upload/$',login_required(views.ImageView.as_view()),name='ImageFormPage'),
	url(r'^image/(?P<pk>\d+)/$',views.ImageDetailView.as_view(),name='ImageDetailPage'),
	url(r'^image/$',views.ImageListView.as_view(),name='ImageListPage'),

	#Gallery part
	url(r'^gallery/$',views.GameGalleryView.as_view(),name='GameGalleryPage'),

	#PlayGame part
	url(r'^favorite/', views.favorite),
	url(r'^unfavorite/', views.unfavorite),	
	url(r'^playgame/(?P<game_slug>[a-zA-Z0-9_.-]+)$',views.GamePlayView.as_view(),name='GamePlayPage'),


	#Comment Part
	url(r'^comment/(?P<game_slug>[a-zA-Z0-9_.-]+)$',views.CommentListView.as_view(),name='CommentListPage'),
	url(r'^comment/create/$',views.CommentCreateView.as_view(),name='CommentCreatePage'),

	#api part ScoreRankApiView
	url(r'^rank/(?P<pk>\d+)/$',views.ScoreRankApiView,name='ScoreRankApi'),
	
	#Games html files.
	url(r'^2048/$',TemplateView.as_view(template_name='notfirstapp/2048.html'),name='GameDemoPage'),
	url(r'^asteroids/$',TemplateView.as_view(template_name='notfirstapp/asteroids.html'),name='Asteroids'),
	url(r'^snake/$',TemplateView.as_view(template_name='notfirstapp/snake.html'),name='Snake'),
	url(r'^starship/$',TemplateView.as_view(template_name='notfirstapp/starship.html'),name='Starship'),
	url(r'^alien/$',TemplateView.as_view(template_name='notfirstapp/alien.html'),name='Alien'),
    url(r'^filler/$',TemplateView.as_view(template_name='notfirstapp/fillerGame.html'),name='Filler Game'),
	url(r'^libgdx/$',TemplateView.as_view(template_name='notfirstapp/gamelibgdx.html'),name='libgdx'),
	
	#blog
	url(r'^blog/', 'notfirstapp.views.blogIndex', name='blog'),
	url(
    r'^blog/view/(?P<slug>[^\.]+).html', 
	'notfirstapp.views.view_post', 
    name='view_blog_post'),
	url(
    r'^blog/category/(?P<slug>[^\.]+).html', 
    'notfirstapp.views.view_category', 
    name='view_blog_category'),
	
	
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT}))

		
		
		
		
		
		
		
		
		
		
