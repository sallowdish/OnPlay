from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.templatetags.static import static
#blog
from django.db.models import permalink

# Create your models here:


class OnPlayUser(models.Model):
	user = models.OneToOneField(User,null=1)
	profileimage=models.ImageField(upload_to='Avatar',null=1)
	nickname = models.CharField(max_length=50,null=1)
	def __unicode__(self):
		return self.user.username
	def avatar_url(self):
		if self.profileimage:
			return self.profileimage.url
		else:
			return static('notfirstapp/images/Avatar/tx_unknown.png')


class Game(models.Model):
	fk_image=models.ForeignKey('Image',null=True)
	gamename=models.CharField(max_length=100,default="Game")
	createTime=models.DateTimeField(auto_now_add=1)
	depolyed_path=models.TextField(max_length=200,null=True)
	game_description=models.TextField(max_length=500,null=True)
	game_instructions=models.TextField(max_length=500,null=True)
	slug = AutoSlugField(populate_from='gamename',unique=1,null=1)
	"""docstring for Game"""
	def __unicode__(self):
		return self.gamename
		
""" All the games that are being put in the spotlight by the admins. 
	 It is up to the Admins to not have duplicate games in this table."""
class SpotlightGame(models.Model):
	fk_game=models.ForeignKey(Game) 
	def __unicode__(self):
		return self.fk_game.gamename
	
class Figure(models.Model):
	User_id=models.ForeignKey(User)
	name=models.CharField(max_length=50,default="Player")
	tag=models.CharField(max_length=50,default="Player#0000")
	def __unicode__(self):
		return self.name+"\t tag: "+self.tag
				

class Play(models.Model):
	"""docstring for Play"""
	# User_id=models.ForeignKey(User)
	Game_id=models.ForeignKey(Game)
	Figure_id=models.ForeignKey(Figure)
	def __unicode__(self):
		return "Playing "+self.Game_id.gamename+" as "+self.Figure_id.name

class Own(models.Model):
	Game_id=models.ForeignKey(Game)
	User_id=models.ForeignKey(User)
	"""docstring for GameOwner"""
	def __unicode__(self):
		# username = Account.objects.filter(id=self.Account_id)[0].username
		# gamename = Game.objects.filter(id=self.Account_id)[0].username
		return self.User_id.username+" owns "+self.Game_id.gamename
		
class ScoreRank(models.Model):
	Figure_id=models.ForeignKey(Figure)
	Game_id=models.ForeignKey(Game)
	
	score=models.IntegerField(default=0)
	rank=models.IntegerField(default=0)
	achieveTime=models.DateTimeField(auto_now_add=1)
	"""docstring for Rank"""
	def __unicode__(self):
		return self.Figure_id.name+" got "+ str(self.score)+" at "+str(self.achieveTime)+" and ranks at "+str(self.rank if self.rank!=0 else 'N/A')

class TimeRank(models.Model):
	Figure_id=models.ForeignKey(Figure)
	Game_id=models.ForeignKey(Game)
	
	finishTime=models.TimeField(auto_now_add=0)
	rank=models.IntegerField(default=0)
	achieveTime=models.DateTimeField(auto_now_add=1)
	"""docstring for TimeRank"""
	def __unicode__(self):
		return self.Figure_id.name+" finished game in "+ str(self.finishTime)+" at "+str(self.achieveTime)+" and ranks at "+str(self.rank if self.rank!=0 else 'N/A')

class Image(models.Model):
    imagefile = models.ImageField(upload_to='Images/%Y/%m/%d')	

    def __unicode__(self):
		return self.imagefile.url

class GameArchive(models.Model):
	fk_game= models.ForeignKey('Game')
	name = models.CharField(max_length=50)
	gamefile = models.FileField(upload_to='temp/game/%Y/%m')
	upload_time=models.DateTimeField(auto_now_add=1)
	def __unicode__(self):
		return self.name

class GameComment(models.Model):
	fk_game= models.ForeignKey('Game')
	fk_comment_poster=models.ForeignKey(User)
	comment=models.CharField(max_length=250)
	comment_time=models.DateTimeField(auto_now_add=1)

class GameRate(models.Model):
	"""docstring for GameRateing"""
	fk_game= models.ForeignKey('Game')
	fk_comment_poster=models.ForeignKey(User)
	rate=models.IntegerField(default=5)
	rate_time=models.DateTimeField(auto_now_add=1)

"""Keeps track of every game page loaded """
class GameVisit(models.Model):
	"""docstring for GameRateing"""
	fk_game= models.ForeignKey('Game')
	fk_visiter=models.ForeignKey(User, null=True)
	visit_time=models.DateTimeField(auto_now_add=1)

		
#blog	
class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ForeignKey('Category')

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('game:view_blog_post', None, { 'slug': self.slug })
#blog
class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('game:view_blog_category', None, { 'slug': self.slug })