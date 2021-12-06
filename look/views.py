from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Max, Min, Sum, Subquery, OuterRef
from django.views.decorators.cache import cache_page


def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    post = Post.objects.filter(gender='male').order_by('-likes')[:10]
    pos = Post.objects.filter(gender='female').order_by('-likes')[:10]

    if request.method == 'POST':
        p_form = PostForm(request.POST, request.FILES)
        if p_form.is_valid():
            p_form.save()
            po = Post.objects.all().count()

            return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': po}))
            # return redirect('home')
    else:
        p_form = PostForm()

    context = {
        'post': post,
        'pos': pos,
        'p_form': p_form,
    }

    return render(request, 'home.html', context)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-date')

    ip = get_ip(request)
    if not Ip.objects.filter(ip=ip).exists():
        Ip.objects.create(ip=ip)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

        return JsonResponse({'msg': 'good'})
    else:
        form = CommentForm()

    is_liked = False
    if post.likes.filter(id=Ip.objects.get(ip=ip).id).exists():
        is_liked = True

    is_disliked = False
    if post.dislikes.filter(id=Ip.objects.get(ip=ip).id).exists():
        is_disliked = True

    context = {
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'is_disliked': is_disliked,
        'total_dislikes': post.total_dislikes(),
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(request, 'post_detail.html', context)


def dislike_post(request):

    ip = get_ip(request)
    if not Ip.objects.filter(ip=ip).exists():
        Ip.objects.create(ip=ip)

    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    dislike = Dislikes.objects.filter(user=Ip.objects.get(ip=ip), id=request.POST.get("post_id"))
    is_disliked = False
    if post.dislikes.filter(id=Ip.objects.get(ip=ip).id).exists():
        post.dislikes.remove(Ip.objects.get(ip=ip))
        is_disliked = False
        Dislikes.objects.filter(user=Ip.objects.get(ip=ip), post=post).delete()

    else:
        post.dislikes.add(Ip.objects.get(ip=ip))
        is_disliked = True
        Dislikes.objects.create(user=Ip.objects.get(ip=ip), post=post)

    context = {
        'is_disliked': is_disliked,
        'total_dislikes': post.total_dislikes(),
        'post': post,
    }
    return JsonResponse({'msg': 'Disliked'})
    # return HttpResponseRedirect(post.get_absolute_url())


def like_post(request):

    ip = get_ip(request)
    if not Ip.objects.filter(ip=ip).exists():
        Ip.objects.create(ip=ip)

    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    like = Likes.objects.filter(user=Ip.objects.get(ip=ip), id=request.POST.get("post_id"))
    is_liked = False
    if post.likes.filter(id=Ip.objects.get(ip=ip).id).exists():
        post.likes.remove(Ip.objects.get(ip=ip))
        is_liked = False
        Likes.objects.filter(user=Ip.objects.get(ip=ip), post=post).delete()

    else:
        post.likes.add(Ip.objects.get(ip=ip))
        is_liked = True
        Likes.objects.create(user=Ip.objects.get(ip=ip), post=post)

    context = {
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'post': post,
    }
    return JsonResponse({'msg': 'Liked'}, status=200)
    # return HttpResponseRedirect(post.get_absolute_url())
