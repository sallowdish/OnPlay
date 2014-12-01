from django.shortcuts import render,render_to_response,get_object_or_404,get_list_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import *
from django.template import RequestContext, loader
from django.views.generic import *
from django.views import generic
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from notfirstapp.models import *
from .forms import *
from .urls import *
from django.db.models import Avg
from django.db.models import Count
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import pdb
# Create your views here.
class IndexView(ListView):
	# current_game=Game.objects.all()
	model=Game
	template_name='notfirstapp/index2.html'
	context_object_name='game_list'

	def get_context_data(self, **kwargs):
		context=super(IndexView,self).get_context_data(**kwargs)
		game_list=Game.objects.order_by('-createTime')[:4]
		context['game_list']=game_list
		context['user']=self.request.user
		return context
	# return HttpResponse(template.render(context))

class SignUpView(FormView):
    # form_class=UserCreationForm
    form_class=UserCreateForm
    template_name='notfirstapp/signup.html'

    def form_valid(self,form):
        user=form.save()
        # import pdb
        # pdb.set_trace()
        OnPlayUser(user=user).save()
        return self.get_success_url();


    def form_invalid(self,form):
        # formWithError = AccountForm(data=form.data)

        return render(self.request,'notfirstapp/signup.html',{'form':form});

    def get_success_url(self):

        return HttpResponse(render(self.request,'notfirstapp/loginframe.html',{'alert':'SignUp Successd!'}))

    def get_fail_url(self):

        return render(self.request,'notfirstapp/signup.html',{'form':form});

class ProfileView(View):
    model=OnPlayUser
    template_name='notfirstapp/profile.html'


    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied("You have to login to see others' profile")
        user=OnPlayUser.objects.get(user__id=self.kwargs.get('pk'))
    	game=GameVisit.objects.filter(fk_visiter=self.kwargs.get('pk'))

    	game_list=Favorite.objects.filter(fk_visiter=self.kwargs.get('pk'))

    	gameplayed=game.count()

    	lastplayed= "none"
    	if gameplayed > 0:
    		lastplayed=game.latest('visit_time')


    	visit=GameVisit.objects.filter(fk_visiter=self.kwargs.get('pk')).extra({'visit_time' : "date(visit_time)"}).values('visit_time').annotate(play_count=Count('visit_time'))

        context={'player':user,  'last': lastplayed, 'gameplayed': gameplayed, 'visit': visit, 'favorite': game_list}
        if 'is_updated' in self.request.GET and self.request.GET.get('is_updated')==u'1':
            context['is_updated']='1'

        return render_to_response('notfirstapp/profile.html',context,context_instance=RequestContext(request))

    # def get(self, request, *args, **kwargs):
    #     raise PermissionDenied()

class ProfileUpdateView(UpdateView):
    model=OnPlayUser
    template_name="notfirstapp/profileupdate.html"
    form_class=OnPlayUserForm
    
    def get_success_url(self):
        return reverse('game:ProfilePage',kwargs={'pk':self.object.user.id})+"?is_updated=1"
        


class FigureFormView(CreateView):
	"""docstring for FigureFormView"""
	context_object_name='figureform.html'
	form_class=FigureForm

	def post(self, request, *args, **kwargs):
		form=self.form_class(request.POST)

                if form.is_valid():
                # newGame=Game(gamename=form.data[''])
                    return self.form_valid(form)
                else:
                    return self.form_invalid(form)

        def form_valid(self,form):
                self.object = form.save()
                # self.object=obj
                # self.object.save()
                self.id=self.object.id
                return HttpResponseRedirect(self.get_success_url())
	
    # def get_form(self, form_class):
    #     form = (super(GameCreateView, self)).get_form(form_class)
    #     current_account = Account.objects.all()
    #     form.fields['fk'].queryset = current_images 
    #     return form

        def get_success_url(self):
                return reverse('game:FigureDetailPage',kwargs={'pk': self.id})

class ScoreRankView(ListView):
    template_name='notfirstapp/ranklist.html'
    model=ScoreRank

    context_object_name='rank_list'

    # def post(self, request, *args, **kwargs):
    #     postdata=self.request.POST

    #     jsondata=json.load(postdata)
    #     data['Game_id']=get_object_or_404(Game,id=self.kwargs['pk'])
    #     data['Figure_id']=Figure_id(name=jsondata['figure'],User_id=get_object_or_404(User,username=jsondata['username']))
    #     date['score']=jsondata['score']
    #     form=ScoreRankForm(data)

    #     if form.is_valid():
    #     # newGame=Game(gamename=form.data[''])
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)


    def form_valid(self,form):
        form.save();

    def get_context_data(self, **kwargs):
        gameid=self.kwargs['pk']
        game=get_object_or_404(Game,pk=gameid)

        context=super(ScoreRankView,self).get_context_data(**kwargs)
        rank_list=ScoreRank.objects.filter(Game_id=gameid).order_by('-score')
        context['rank_list']=rank_list
        context['game']=game
        # context['user']=self.request.user
        return context

class GameGalleryView(ListView):
    # form_class=GameForm
    template_name = "notfirstapp/gamegallery.html"
    context_object_name = 'game_list'
    queryset=Game.objects.order_by('-createTime')

class GameListView(ListView):
	# form_class=GameForm
	template_name = "notfirstapp/gamelist.html"
	context_object_name = 'game_list'

	def get_queryset(self):
        	return Game.objects.filter(own__User_id=self.request.user).order_by('-createTime')

    

class GameCreateView(FormView):
    # Handle file upload
    template_name="notfirstapp/gameform.html"
    form_class=GameCreateForm

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST,request.FILES)
        if form.is_valid():
        	# newGame=Game(gamename=form.data[''])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        img=Image(imagefile=form.cleaned_data['image'])
        img.save()
        game=Game(gamename=form.cleaned_data['gamename'],fk_image=img)
        game.save()
        ownership=Own(Game_id=game,User_id=self.request.user)
        ownership.save()
    	self.id=game.id
    	return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
    	return reverse('game:GameDetailPage',kwargs={'pk': self.id})

class GameDetailView(DetailView):
    model = Game
    template_name = 'notfirstapp/gamedetail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GameDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        game=context['game']
        context['appname'] = 'notfirstapp'
        context['back_url']=reverse('game:GameManagePage')
        context['available_archives']=GameArchive.objects.filter(fk_game=game)
        context['form']=GameArchiveUploadForm(initial={'name':game.gamename,'fk_game':game})
        return context


class ImageView(FormView):
    # Handle file upload
    template_name="notfirstapp/imageform.html"
    form_class=ImageForm

    def get_context_data(self, **kwargs):
    	context = super(ImageView, self).get_context_data(**kwargs)
    	context['uploaded']=Image.objects.all();
    	return context;

    def form_valid(self,form):
    	newImage=Image(
    		imagefile=self.get_form_kwargs().get('files')['imagefile'])	
    	newImage.save();
    	self.id=newImage.id

    	return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
    	return reverse('game:ImageFormPage')

class ImageDetailView(DetailView):
    model = Image
    template_name = 'notfirstapp/imagedetial.html'
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ImageDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['appname'] = 'notfirstapp'
        return context


class ImageListView(ListView):
    model = Image
    template_name = 'notfirstapp/imagelist.html'
    context_object_name = 'imagelist'
    queryset = Image.objects.all()

@csrf_exempt
def ScoreRankApiView(request,pk):
    if request.method=='POST':
        postdata=request.body
        jsondata=json.loads(postdata)
        data={}
        data['Game_id']=get_object_or_404(Game,id=pk).id
        user=get_object_or_404(User,username=jsondata['username'])
        figure=Figure(name=jsondata['figure'],User_id=user)
        figure.save();
        figure=figure.id;
        data['Figure_id']=figure
        data['score']=jsondata['score']
        form=ScoreRankForm(data)


        if form.is_valid():
        # newGame=Game(gamename=form.data[''])
            newRank=form.save();
            lst=ScoreRank.objects.filter(Game_id=data['Game_id']).order_by('-score')
            for index,item in enumerate(lst):
                item.rank=index+1
                item.save();
            # position=toplist.index(newRank)
            lst=ScoreRank.objects.filter(Game_id=data['Game_id']).order_by('-score')
            newRank=get_object_or_404(ScoreRank,id=newRank.id)
            if len(lst)>5:
                lst=lst[:5]
            toplist=[]
            for rank in lst:
                dic={}
                dic['figure']=rank.Figure_id.name;
                dic['score']=rank.score;
                dic['time']=rank.achieveTime.strftime("%Y-%m-%d %H:%M:%S");
                dic['rank']=rank.rank
                toplist.append(dic)
            reval={}
            reval['position']=newRank.rank
            reval['rank']=toplist
            jsondata=json.dumps(reval)
            return HttpResponse(jsondata, status=201)
        else:
            return HttpResponse('Bad Request', status=400)
    else:
        return HttpResponse('Forbiden.',status=403)

def login_user(request):
    if request.method=='POST':
        logout(request)
        template_name='notfirstapp/loginframe.html'
        username = password = ''
        context_dict={}
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    nextURL=reverse('game:indexPage')
                    if request.POST['next'] != '':
                        nextURL=request.POST['next']
                        # print 'fail to get next'
                    return HttpResponseRedirect(nextURL)

                else:
                    context_dict['error']='account: '+username+" is not active."
            else:
                context_dict['error']='Invalid username or password' 
        return render_to_response('notfirstapp/loginframe.html', context_dict,context_instance=RequestContext(request))
    elif request.method=='GET':
        dic={}
        try:
            dic['next']=request.GET['next']
        except Exception, e:
            dic={}
        return render_to_response('notfirstapp/loginframe.html',dic,context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('game:LoginPage'))

class GameUploadView(FormView):
    """docstring for GameUploadView"""
    """ the view handle the upload file"""
    template_name='notfirstapp/gamedetail.html'
    form_class = GameArchiveUploadForm
    
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('game:GameDetailPage', kwargs={'pk': self.request.POST['fk_game']})

class GamePlayView(TemplateView):
	template_name='notfirstapp/gameplay.html'

	def get_context_data(self,**kwargs):
		context=super(GamePlayView,self).get_context_data(**kwargs);
		game=Game.objects.get(slug=context['game_slug'])
		context['game']=game
		# context['object_list']=GameComment.objects.filter(fk_game=game)
		
		
		ratings = GameRate.objects.filter(fk_game=game)
		context['rating'] = ratings.aggregate(Avg('rate')).values()[0]
        	context['ratings'] = ratings.count()
         
		
		if self.request.user.is_authenticated():

			if Favorite.objects.filter(fk_game=game, fk_visiter=self.request.user ).count()	 > 0: 
				context['favorite'] = 1

			GameVisit.objects.create(fk_game=game, fk_visiter=self.request.user)
		else:
			GameVisit.objects.create(fk_game=game)

		context['played']=GameVisit.objects.filter(fk_game=game).count()
		context['visit']=GameVisit.objects.filter(fk_game=game).extra({'visit_time' : "date(visit_time)"}).values('visit_time').annotate(play_count=Count('visit_time'))
	
	
		form = CommentForm(initial={'fk_game': game, 'fk_comment_poster': self.request.user.id})
		form.fields['fk_game'].widget = forms.HiddenInput()		
		form.fields['fk_comment_poster'].widget = forms.HiddenInput()			
		context['form'] = form
        	context['request']=self.request
		
		return context

    #should seprate
	def post(self, request, **kwargs):
		context=super(GamePlayView,self).get_context_data(**kwargs);
		game=Game.objects.get(slug=context['game_slug'])
		context['game']=game	

		
		model=OnPlayUser
		if request.user.is_authenticated():
			if Favorite.objects.filter(fk_game=game, fk_visiter=self.request.user ).count()	 > 0: 
				context['favorite'] = 1	
				
			if request.POST['action'] == 'Rate':
				user =User.objects.get(id=request.user.id)
				obj = GameRate.objects.get_or_create(fk_game=game, fk_comment_poster=user )
				GameRate.objects.filter(fk_game=game, fk_comment_poster=user ).update(rate=request.POST.get("rating", ""))
				
			if request.POST['action'] == 'Comment':
				user = User.objects.get(id=request.user.id)
				obj = GameComment.objects.create(fk_game=game, fk_comment_poster=user, comment=request.POST.get("comment", "") )	
		
		else:
			if request.POST['action'] == 'Rate':
				context['rate_warning'] = 'warning'
			
			if request.POST['action'] == 'Comment':
				context['comment_warning'] = 'warning'
	
		ratings = GameRate.objects.filter(fk_game=game)
		context['ratings'] = ratings.count()
		context['rating'] = ratings.aggregate(Avg('rate')).values()[0]	  	
		
		context['played']=GameVisit.objects.filter(fk_game=game).count()
		context['visit']=GameVisit.objects.filter(fk_game=game).extra({'visit_time' : "date(visit_time)"}).values('visit_time').annotate(play_count=Count('visit_time'))
	
		context['comment_list']=GameComment.objects.filter(fk_game=game)
		
		form = CommentForm(initial={'fk_game': game, 'fk_comment_poster': 0})
		form.fields['fk_game'].widget = forms.HiddenInput()		
		form.fields['fk_comment_poster'].widget = forms.HiddenInput()			
		context['form'] = form		
		
		return render_to_response("notfirstapp/gameplay.html", context, context_instance = RequestContext(request));
			
			
def favorite(request):
	if (request.POST.get("user", "") != "None"):
		user =User.objects.get(id=request.POST.get("user", ""))
		game=Game.objects.get(slug=request.POST.get("game", ""))

		obj = Favorite.objects.get_or_create(fk_game=game, fk_visiter=user )

		return HttpResponse('Success')
	else:
	    return HttpResponse('Login')

 
def unfavorite(request):
	if (request.POST.get("user", "") != "None"):
		user =User.objects.get(id=request.POST.get("user", ""))
		game=Game.objects.get(slug=request.POST.get("game", ""))

		Favorite.objects.filter(fk_game=game, fk_visiter=user ).delete()

		return HttpResponse('Success')
	else:
	    return HttpResponse('Login')






class CommentListView(ListView):
    model=GameComment
    template_name='notfirstapp/commentlist.html'
    paginate_by = 5

    def get_context_data(self,**kwargs):
        # import pdb
        context=super(CommentListView,self).get_context_data(**kwargs);
        # pdb.set_trace()
        if 'game_slug' in self.kwargs.keys() and self.request.user.is_authenticated():
            # context['comment_list']=GameComment.objects.filter(fk_game__slug=self.kwargs.get('game_slug'));
            context['form']=CommentForm(initial={'fk_game': Game.objects.get(slug=self.kwargs.get('game_slug')), 'fk_comment_poster': self.request.user.id})
        else:
            pass
            # context['comment_list']=GameComment.objects.all();
        # pdb.set_trace()
        return context


class CommentCreateView(FormView):
    """docstring for Comment"""
    form_class=CommentForm
    new_comment=""

    
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        raise PermissionDenied("You shouldn't be here.")

    def form_valid(self,form):
        self.new_comment=form.save();
        return HttpResponseRedirect(reverse('game:CommentListPage',kwargs={'game_slug': self.new_comment.fk_game.slug}))

    #TODO:1
    def form_invalid(self,form):
        raise ValidationError



#blog
def blogIndex(request):
	entries = Blog.objects.filter().order_by('-id')
	
	paginator = Paginator(entries,5 )
	
	page_num = request.GET.get('page', 1)
	
	try:
		page = paginator.page(page_num)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		page = paginator.page(1)
		
	ctx = {
		'page': page
	}
	return render_to_response('notfirstapp/blog_index.html', ctx, context_instance=RequestContext(request))

def view_post(request, slug):   
    return render_to_response('notfirstapp/view_post.html', {
        'post': get_object_or_404(Blog, slug=slug)
    })

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    blog = Blog.objects.filter(category=category)
    if len(blog)>5:
        blog=blog[:5]
    return render_to_response('notfirstapp/view_category.html', {
        'category': category,
        'posts': blog,
    })


