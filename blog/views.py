from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from blog.forms import CommentForm
from blog.models import Post


@cache_page(300)
@vary_on_headers("Cookie")
def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now())
    print(posts)
    return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    ctx = {
        "post": post,
        "comment_form": comment_form,
        }
    return render(request, "blog/post-detail.html", ctx)