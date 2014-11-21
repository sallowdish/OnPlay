from django import forms
from .models import *
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput
from django.contrib.auth.forms import UserCreationForm

# class AccountForm(forms.ModelForm):
#     password= models.CharField(max_length=50)
#     email=models.EmailField(max_length=50)
#     # newUser=None

#     class Meta:
#         model=Account


#     def is_valid(self):
#         # import pdb; pdb.set_trace();
#         emptyError='This field is required'
#         isFilledUp=True
#         flag=super(AccountForm,self).is_valid()
#         #check all field is filled up
#         if not bool(self.data['username']):
#             self.errors['username']=emptyError
#         if not bool(self.data['password']):
#             self.errors['password']=emptyError
#         # if not bool(self.data['email']):
#         #     self.errors['email']=emptyError
#         if len(self.errors)==0:
#             #check if username is valid
#             existList=[user.username for user in User.objects.all()]
#             if self.data['username'] in existList:
#                 self.errors['Invaild Username']='Username has been used by someone else!'
#                 isFilledUp=False
#         else:#fail to find all required info
#             isFilledUp=False
#         # import pdb; pdb.set_trace()
#         return flag and isFilledUp

#     def save(self):
#         user=User.objects.create_user(
#             username=self.data['username'],
#             password=self.data['password'],
#             email=self.data['email'],
#             first_name=self.data['firstname'],
#             last_name=self.data['lastname']
#         )
#         self.newUser=user

class GameForm(forms.ModelForm):
    class Meta:
    	model= Game
        field=['gamename','fk_image']
        exclude=['depolyed_path']


class ImageForm(forms.Form):
    imagefile = forms.ImageField(
        label='Select a image',
        help_text='max. 42 megabytes'
    )

class FigureForm(forms.ModelForm):
    class Meta:
        model=Figure
        field=['name']

class PlayForm(forms.ModelForm):
    class Meta:
        model=Play

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

 
class CommentForm(forms.ModelForm):
	comment = forms.CharField(label='Comment', max_length=250, widget=forms.Textarea)
	fk_game = forms.CharField(max_length=50)
	fk_comment_poster = forms.CharField(max_length=50)	
	class Meta:
		model=GameComment       
