from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from posts.models import Video
from posts.forms import VideoForm


def login_user(request):
    user = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            ''

        if user:
            user = authenticate(username=email, password=password)
            login(request, user)
            return redirect('index')

    return render(request, 'login.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):

    if not request.user.is_authenticated:
        return redirect('login')

    videos = Video.objects.all()

    return render(request, 'index.html', {
        'videos': videos
    })


@login_required(login_url='login')
def create_post(request):
    form = VideoForm()
    if request.method == 'POST':
        title = request.POST['title']

        form = VideoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.slug = title
            form.author = request.user
            form.save()
            return redirect('index')
        print(request.POST)
    return render(request, 'add-post.html', {
        'form': form
    })


@login_required(login_url='login')
def user_profile(request, user_id):
    user = User.objects.get(id=id)
    video_posts = Video.objects.filter(author=user)
    return render(request, 'profile.html', {
        'user': user,
        'videos': video_posts
    })


@login_required(login_url='login')
def like_dislike_post(request, video_id):
    video = Video.objects.get(id=video_id)
    liked_by_users = video.likes.all()

    is_like = False
    for user in liked_by_users:
        if user == request.user:
            is_like = True

    if is_like:
        video.likes.remove(request.user)

    if not is_like:
        video.likes.add(request.user)

    return redirect(request.META['HTTP_REFERER'])
