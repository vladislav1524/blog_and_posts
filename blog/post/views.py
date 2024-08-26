from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, UserProfile, Like
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, CommentForm, LoginForm, PostForm, ImageEditForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.core.paginator import Paginator


# ПОСТ LIST + CRUD
def post_list(request, username=None):
    if username:
        profile = get_object_or_404(UserProfile, user__username=username)
        posts = Post.objects.filter(author=profile)
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post/list.html', {'page_obj': page_obj,
                                                   'username': username,})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    similar_posts = Post.objects.filter(tags__in=post.tags.all())\
      .exclude(id=post.id)\
      .annotate(common_tags_count=Count('tags', filter=Q(tags__in=post.tags.all())))\
      .order_by('-common_tags_count')\
      .distinct()[:3]
    comments = Comment.objects.filter(post=post)
    user_liked = post.likes.filter(user=request.user).exists()
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'similar_posts': similar_posts,
                                                     'comments': comments,
                                                     'user_liked': user_liked})


@login_required
def post_add(request):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user=request.user)
        form = PostForm(request.POST, request.FILES, author=profile)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.save()
            form.save_m2m()
            return redirect(new_post)
    else:
        form = PostForm()
    return render(request, 'blog/post/create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post:detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post/edit.html', {'form': form,
                                                   'post': post})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('post:post_list')
    return render(request, 'blog/post/delete.html', {'post': post})


# лайки
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete() 
        like_count = post.total_likes() 
        return JsonResponse({'like_count': like_count, 'message': 'Unliked'})
    
    like_count = post.total_likes()  # Получаем новое количество лайков
    return JsonResponse({'like_count': like_count, 'message': 'Liked'})


# КОММЕНТАРИЙ CRUD
@login_required
def comment_add(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data  
            profile = get_object_or_404(UserProfile, user=request.user)  
            Comment.objects.create(post=post, author=profile, body=cd['body'], original_body=cd['body']) 
            return redirect('post:detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/comment/comment_form.html', {'form': form,
                                                              'post': post})


@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    profile = get_object_or_404(UserProfile, user=request.user)  
    
    if profile != comment.author:
        return redirect('post:detail', post_id=comment.post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            new_body = form.cleaned_data['body']        
            comment.body = new_body
            comment.save() 
            return redirect('post:detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/comment/comment_edit.html', {
        'form': form,
        'post': comment.post,
        'comment': comment
    })


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    if request.method == "POST":
        comment.delete()
        return redirect(post.get_absolute_url())
    return render(request, 'blog/comment/confirm_delete.html', {'comment': comment})


# профиль
@login_required
def profile_info(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)
    count_posts = Post.objects.filter(author=profile).count()
    count_comments = Comment.objects.filter(author=profile).count()
    if request.method == 'POST':
        form = ImageEditForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data 
            if cd['delete_image']:
                if profile.image:
                    profile.image.delete(save=False)
                profile.image = None 
            elif cd['image']:
                profile.image = cd['image']
            profile.save()
    else:
        form = ImageEditForm(initial={'image': profile.image})
    return render(request, 'blog/profile/profile_info.html', {'profile': profile,
                                                              'count_posts': count_posts,
                                                              'count_comments': count_comments,
                                                              'form': form})


# AUTH
class RegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('post:post_list')

    def get_success_url(self):
        url = reverse_lazy('post:post_list')
        if not url:
            raise ValueError("The success URL could not be resolved.")
        return url

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Пользователь с таким адресом электронной почты уже существует.')
            return self.form_invalid(form)
        
        user = form.save()
                    
        UserProfile.objects.create(user=user,
                                 image=form.cleaned_data['image'],
                                 date_of_birth=form.cleaned_data['date_of_birth'])
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        return HttpResponseRedirect(self.get_success_url())
    

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username_or_email, password=password)

            if user is None:
                users = User.objects.filter(email=username_or_email)

                if users.exists():
                    if users.count() > 1:
                        form.add_error('username_or_email', 'Найдено несколько аккаунтов с этой почтой. Если вы зарегистрированы через VK или Google, войдите через соответствующие кнопки ниже.')
                        return render(request, 'registration/login.html', {'form': form}) 
                    user = users.first()  # Берем первого пользователя из списка
                else:
                    user = None
            
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('post:post_list')
            else:
                form.add_error(None, 'Неверные логин/почта или пароль')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})
