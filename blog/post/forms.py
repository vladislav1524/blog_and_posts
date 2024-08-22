from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=False, label='Фото профиля')
    date_of_birth = forms.DateField(required=True, label='Укажите вашу дату рождения')
    username = forms.CharField(max_length=20, label='Имя пользователя')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Логин или Email', max_length=254)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class CommentForm(forms.ModelForm):
        
    class Meta:
        model = Comment
        fields = ('body',) 


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'tags', 'image', 'video'] 

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(PostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        post = super(PostForm, self).save(commit=False)
        image = self.cleaned_data.get('image')
        video = self.cleaned_data.get('video')
        if image:
            post.image = image
        if video:
            post.video = video
        if not self.instance.pk:  
            post.author = self.author
        if commit:
            post.save()
        return post
    

class ImageEditForm(forms.Form):
    image = forms.ImageField(required=False, label='Фото')
    delete_image = forms.BooleanField(required=False, label='Удалить фото')
