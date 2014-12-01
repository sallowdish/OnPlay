from django import forms
from .models import *
from django.contrib.auth.models import User
from django.forms.widgets import *
from django.contrib.auth.forms import UserCreationForm

class GameForm(forms.ModelForm):
    class Meta:
    	model= Game
        exclude=['depolyed_path']

class GameCreateForm(forms.Form):
    gamename = forms.CharField(required=0)
    image = forms.ImageField(label='Select a image',
        help_text='max. 42 megabytes')

class ImageForm(forms.Form):
    imagefile = forms.ImageField(
        label='Select a image',
        help_text='max. 42 megabytes'
    )

class FigureForm(forms.ModelForm):
    class Meta:
        model=Figure
        fields=['name']

class PlayForm(forms.ModelForm):
    class Meta:
        model=Play
        exclude=[]

class ScoreRankForm(forms.ModelForm):
    # username=models.CharField(max_length=50)
    # playername=models.CharField(max_length=50)
    # gamename=models.CharField(max_length=50)
    class Meta:
        model=ScoreRank
        exclude=['rank']

class GameArchiveUploadForm(forms.ModelForm):

    class Meta:
        model=GameArchive
        widgets={
            'name': HiddenInput(),
            'fk_game': HiddenInput(),
        }
        exclude=[]
    # name = forms.CharField(max_length=50)
    # game = forms.FileField(label='Select a .zip file containing your game')

class UserCreateForm(UserCreationForm):
    """docstring for UserCreateForm"""
    firstname=forms.CharField(max_length=30,required=0)
    lastname=forms.CharField(max_length=30,required=0)
    email=forms.EmailField(max_length=50)

    def save(self, commit=True):
        # import pdb
        # pdb.set_trace()
        user=super(UserCreationForm,self).save(commit=True);
        user.set_password(self.cleaned_data["password1"])
        user.email=self.cleaned_data["email"]
        user.first_name=self.cleaned_data["firstname"]
        user.last_name=self.cleaned_data["lastname"]

        if commit:
            user.save()
        return user

class OnPlayUserForm(forms.ModelForm):
     """docstring for OnPlayUserForm"""
     class Meta:
        model=OnPlayUser
        # exclude=['user']
        widgets={
            'user':HiddenInput(),
        }
         

class CommentForm(forms.ModelForm):
    class Meta:
        model=GameComment
        exclude=[]
        widgets={
            'fk_game' : HiddenInput(),
            'fk_comment_poster': HiddenInput(),
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 240}),
        }

