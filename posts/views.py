from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Post, LastUpdate
import time, datetime
from .forms import PostForm
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core import mail
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from news.tasks import email_admin
# Create your views here.

@cache_page(None)
def home(request):
    """
    This is the public view that displays only published posts. 
    The view also returns a UNIX timestamp of the most recently updated post.
    This timestamp is compared with the `LastUpdate` value to determine when the page should be refreshed.
    Every 5 seconds, the `latest` timestamp is compared with the `LastUpdate` timestamp. 
    If `LastUpdate` is greater that `latest`, this implies that a Post has either been published or unpublished.
    """

    posts = Post.objects.filter(published=True)
    latest = 0
    if posts:
        latest = Post.objects.latest('updated').unix_time()

    return render(request, 'posts/home.html', {'posts':posts, 'latest':latest})

@login_required
def all(request):
    """
    This is a view for staff members that shows all posts, published or unpublished
    Each Post has a link that displays the Post and presents the option to publish or unpublish the post
    """

    posts = Post.objects.filter()

    print("made a query")
    return render(request, 'posts/all.html', {'posts':posts})

@login_required
def toggle_publish(request,id):
    """
    This view allows an authenticated staff user to publish or unpublish an article by clicking a button.
    Clicking the button toggles the current state of the selected Post's `published` field.
    It also updates the `LastUpdated` time to be the time when the Post was updated (saved), tracked by its `updated` field
    This field uses `auto_now=True`, which updates the datetime field to the time at which the record is saved.
    Finally, the button triggers the clearing of the cache.
    This removes the cached home page and forces it to be refreshed with the published (or unpublished post).
    """
    
    instance = get_object_or_404(Post, id=id)

    if request.method=="POST":
        instance.published = not instance.published
        instance.save()

        t, created = LastUpdate.objects.get_or_create(id=1)

        t.updated = instance.updated
        t.save()

        cache.clear()
        return redirect('posts:home')

    context = {'post':instance}

    return render(request, 'posts/publish.html', context)

@login_required
def new(request):
    """
    This form allows for a staff user to create a new post.
    It does not publish the post, but it redirects to a page where the post can be reviewed and published.
    """

    form = PostForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return HttpResponseRedirect(reverse('posts:toggle_publish', args=(instance.id,)))

    context = {'form':form}

    return render(request, 'posts/new.html', context)

def refresh(request):
    """
    This is the URL that is polled by the public-facing page.
    It returns a UNIX timestamp of the last time an article was published or unpublished. 
    This timestamp comes from the `LastUpdated`, a table that stores and updates only one row with one datetime column.
    Publishing and unpublishing are the only two actions that clear the cached homepage. 
    When the returned UNIX timestamp is greater than the UNIX timestamp of the most recently updated article,
    The page is refreshed with `location.reload()`.
    """
    
    t, created = LastUpdate.objects.get_or_create(id=1)
    if created:
        t.save()
        t = t.unix_time()
    else:
        t = t.unix_time()
    latest = int(t) - 2
    return JsonResponse({'latest':int(latest)})


def mail(request):
    """
    A test function for sending mail.
    """
    email_admin.delay('testinggg')
    return JsonResponse({"details":"working"})