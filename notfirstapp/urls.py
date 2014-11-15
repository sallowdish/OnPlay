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
	url(r'^logout/$','django.contrib.auth.views.logout', {'template_name': 'notfirstapp/logout.html'},name="LogoutPage"),
	#signup
	url(r'^signup/$',views.SignUpView.as_view(),name='SignUpPage'),
	url(r'^profile/$',views.ProfileView.as_view(),name='ProfilePage'),
	#index page
	url(r'^$', views.IndexView.as_view(), name="indexPage"),
	# url(r'^(?P<game_id>\d+)/$', views.DetailPageController, name='DetailPage'),
	#gallery part
	url(r'^gallery/upload/$',login_required(views.GameCreateView.as_view()),name='GameFormPage'),
	url(r'^gallery/gamearchive/upload/$',login_required(views.GameUploadView.as_view()),name='GameArchiveUploadPage'),
	url(r'^gallery/(?P<pk>\d+)/$',login_required(views.GameDetailView.as_view()),name='GameDetailPage'),
	url(r'^gallery/$',login_required(views.GameListView.as_view()),name='GameListPage'),
	url(r'^gallery/(?P<pk>\d+)/rank/$',login_required(views.ScoreRankView.as_view()),name='ScoreRankPage'),
	url(r'^gallery/simplelist/$',TemplateView.as_view(template_name='game.html'),name='SimpleGameListPage'),
	#image part
	url(r'^image/upload/$',login_required(views.ImageView.as_view()),name='ImageFormPage'),
	url(r'^image/(?P<pk>\d+)/$',views.ImageDetailView.as_view(),name='ImageDetailPage'),
	url(r'^image/$',views.ImageListView.as_view(),name='ImageListPage'),

	#api part ScoreRankApiView
	url(r'^rank/(?P<pk>\d+)/$',views.ScoreRankApiView,name='ScoreRankApi'),

	#2048 game demo
	url(r'^2048/$',TemplateView.as_view(template_name='notfirstapp/2048.html'),name='GameDemoPage'),
	# url(r'^(?P<contact_id>\d+)/edit/$', views.EditPageController, name='EditPage'),
	# url(r'^(?P<contact_id>\d+)/edit/done$', views.EditDoneController, name='EditDone'),
	# url(r'^create/$', views.CreatePageController, name='CreatePage'),
	# url(r'^create/done$', views.CreateDoneController, name='CreateDone'),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))