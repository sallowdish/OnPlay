from django.shortcuts import render,render_to_response,get_object_or_404,get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse,QueryDict,HttpResponseRedirect
from django.template import RequestContext, loader
from django.views.generic import *
from django.views import generic
from django.contrib.auth.models import User
from notfirstapp.models import *
from .forms import *
from .urls import *
from django.db.models import Avg
import json
# Create your views here.
class IndexView(ListView):
	# current_game=Game.objects.all()
	model=Game
	template_name='notfirstapp/index.html'
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
        form.save()
        
        return self.get_success_url();


    def form_invalid(self,form):
        # formWithError = AccountForm(data=form.data)

        return render(self.request,'notfirstapp/signup.html',{'form':form});

    def get_success_url(self):

        return HttpResponse(render(self.request,'notfirstapp/loginframe.html',{'alert':'SignUp Successd!'}))

    def get_fail_url(self):

        return render(self.request,'notfirstapp/signup.html',{'form':form});

class ProfileView(TemplateView):
	"""docstring for ClassName"""
	template_name='notfirstapp/profile.html'


	def get_context_data(self,**kwargs):
		context=super(ProfileView,self).get_context_data(**kwargs)
		context['user']=self.request.user
		return context
		


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

    

class GameCreateView(CreateView):
    # Handle file upload
    template_name="notfirstapp/gameform.html"
    form_class=GameForm

    def post(self, request, *args, **kwargs):
    	# data=form.data
    	# self.object = None
     #    form = self.get_form(self.form_class)
     #    targetID=request.POST['fk_image']
     #    form.instance.fk_image=Image.objects.get(id=targetID)
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
        ownership=Own(Game_id=self.object,User_id=self.request.user)
        ownership.save()
    	self.id=self.object.id
    	return HttpResponseRedirect(self.get_success_url())

    # def get_form(self, form_class):
    #     form = (super(GameCreateView, self)).get_form(form_class)
    #     current_images = Image.objects.all()
    #     form.fields['fk_image'].queryset = current_images 
    #     return form

    def get_context_data(self, **kwargs):
        context = super(GameCreateView, self).get_context_data(**kwargs)
        context['current_path'] = self.request.get_full_path()
        return context

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
        return context

 
class GameView(TemplateView):

	def get(self, request, gameid):
		model=Game
		template_name = "notfirstapp/game.html"
		context_object_name = 'game'
		queryset=Game.objects.order_by('-createTime')
		gameObj =Game.objects.get(id=gameid)
		model=GameVisit
		
		#obj = GameVisit.objects.get_or_create(fk_game=timep)
		obj = GameVisit.objects.create(fk_game=gameObj)
		
		visted = GameVisit.objects.filter(fk_game=gameObj).count()	
		
		comments = GameComment.objects.filter(fk_game=gameObj)		
		
		p = GameRate.objects.filter(fk_game=gameObj)
		rating = p.aggregate(Avg('rate')).values()[0]		
		
		
		form = CommentForm(initial={'fk_game': gameid, 'fk_comment_poster': 0})
		form.fields['fk_game'].widget = forms.HiddenInput()		
		form.fields['fk_comment_poster'].widget = forms.HiddenInput()		
		
		
		return render_to_response("notfirstapp/game.html", {'rating': rating, 'played': visted, 'form' : form, 'gameid' : gameid , 'comments' : comments}, context_instance = RequestContext(request));
		
	def post(self, request, gameid):
			
		model=Game
		template_name = "notfirstapp/game.html"
		context_object_name = 'game'
		queryset=Game.objects.order_by('-createTime')
		gameObj =Game.objects.get(id=gameid)
		model=GameVisit
		obj = GameVisit.objects.create(fk_game=gameObj)
		
		if(request.POST.get("rating", "").strip() != "-1" ):
			user =User.objects.get(id=request.user.id)
			obj = GameRate.objects.get_or_create(fk_game=gameObj, fk_comment_poster=user )
			GameRate.objects.filter(fk_game=gameObj, fk_comment_poster=user ).update(rate=request.POST.get("rating", ""))		
			#obj.rate = request.POST.get("rating", "")
		#	obj = GameRate(rate = request.POST.get("rating", ""))
			
		
		
		if(request.POST.get("comment", "").strip() != ""):
			user =User.objects.get(id=request.user.id)
			obj = GameComment.objects.create(fk_game=gameObj, fk_comment_poster=user, comment=request.POST.get("comment", "") )
		
	
		p = GameRate.objects.filter(fk_game=gameObj)
		rating = p.aggregate(Avg('rate')).values()[0]		
		
		visted = GameVisit.objects.filter(fk_game=gameObj).count()				
		
		comments = GameComment.objects.filter(fk_game=gameObj)		
			
		form = CommentForm(initial={'fk_game': gameid, 'fk_comment_poster': 0})
		form.fields['fk_game'].widget = forms.HiddenInput()		
		form.fields['fk_comment_poster'].widget = forms.HiddenInput()		
		return render_to_response("notfirstapp/game.html", {'rating': rating, 'played': visted, 'form' : form, 'gameid' : gameid, 'comments' : comments }, context_instance = RequestContext(request));
			
	
