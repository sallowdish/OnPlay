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
	url(r'^profile/$',views.ProfileView.as_view(),name='ProfilePage'),

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
	url(r'^playgame/(?P<game_slug>\w+)',views.GamePlayView.as_view(),name='GamePlayPage'),

	#Comment Part
	url(r'comment/',views.CommentListView.as_view(),name='CommentListPage'),
<<<<<<< HEAD
=======
	url(r'comment/create',views.CommentCreateView.as_view(),name='CommentCreatePage'),
	#gameview
	url(r'^game/(?P<gameid>\d+)/$',views.GameView.as_view(),name='game'),
>>>>>>> rayworkingbranch
	

	#api part ScoreRankApiView
	url(r'^rank/(?P<pk>\d+)/$',views.ScoreRankApiView,name='ScoreRankApi'),

	# url(r'^(?P<contact_id>\d+)/edit/$', views.EditPageController, name='EditPage'),
	# url(r'^(?P<contact_id>\d+)/edit/done$', views.EditDoneController, name='EditDone'),
	# url(r'^create/$', views.CreatePageController, name='CreatePage'),
	# url(r'^create/done$', views.CreateDoneController, name='CreateDone'),
	
	#Games html files.
	url(r'^2048/$',TemplateView.as_view(template_name='notfirstapp/2048.html'),name='GameDemoPage'),
	url(r'^asteroids/$',TemplateView.as_view(template_name='notfirstapp/asteroids.html'),name='Asteroids'),
	url(r'^snake/$',TemplateView.as_view(template_name='notfirstapp/snake.html'),name='Snake'),
	url(r'^starship/$',TemplateView.as_view(template_name='notfirstapp/starship.html'),name='Starship'),
	url(r'^alien/$',TemplateView.as_view(template_name='notfirstapp/alien.html'),name='Alien'),
	url(r'^libgdx/$',TemplateView.as_view(template_name='notfirstapp/gamelibgdx.html'),name='libgdx'),
	
	
	
	
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

		
		
		
		
		
		
		
		
		
		
