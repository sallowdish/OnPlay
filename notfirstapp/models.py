from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField

# Create your models here.
class OnPlayUser(models.Model):
	user = models.OneToOneField(User,null=1)
	profileimage=models.ImageField(upload_to='Avatar',null=1)
	nickname = models.CharField(max_length=50,null=1)


class Game(models.Model):
	gamename=models.CharField(max_length=100,default="Game")
	createTime=models.DateTimeField(auto_now_add=1)
	fk_image=models.ForeignKey('Image',null=True)
	depolyed_path=models.TextField(max_length=200,null=1)
	slug = AutoSlugField(populate_from='title',unique=1,null=1)
	"""docstring for Game"""
	def __unicode__(self):
		return self.gamename
	
class Figure(models.Model):
	name=models.CharField(max_length=50,default="Player")
	tag=models.CharField(max_length=50,default="Player#0000")
	User_id=models.ForeignKey(User)
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
	name = models.CharField(max_length=50)
	gamefile = models.FileField(upload_to='temp/game/%Y/%m')
	fk_game= models.ForeignKey('Game')
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

class GameVisit(models.Model):
	"""docstring for GameRateing"""
	fk_game= models.ForeignKey('Game')
	fk_visiter=models.ForeignKey(User, null=True)
	visit_time=models.DateTimeField(auto_now_add=1)

		
	
