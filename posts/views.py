from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.urls import reverse
import random
from next_prev import next_in_order
import string
from .forms import CommentForm, PostForm
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Post, Comment, Category


def generate_id():
    id = ''.join(random.choice(string.ascii_uppercase +
                               string.ascii_lowercase + string.digits) for _ in range(7))
    return str(id)


# get all posts


def index(request):
    posts = Post.objects.all()
    context = {
        "posts": posts,

    }
    print(posts)
    return render(request, 'index.html', context)


# get all posts by category
def category(request, categories):
    cat = get_object_or_404(Category, title=str(categories))
    posts = get_list_or_404(Post, categories=cat)
    print(category)
    print(posts)
    context = {
        "posts": posts,
        "cat": cat,
    }
    print(posts)
    return render(request, 'posts.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'categories', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = generate_id()
        return super().form_valid(form)


def post(request, post_id):
    post = get_object_or_404(Post, post_id=str(post_id))
    next_post = next_in_order(post)
    print(next_post)
    comments = post.get_comments
    form = CommentForm(request.POST, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None

            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    # create replay comment object
                    reply_comment = form.save(commit=False)
                    # assign parent_obj to replay comment
                    reply_comment.parent = parent_obj
            form.instance.post = post
            form.instance.user = request.user
            form.save()
            return redirect(reverse("post", kwargs={
                'post_id': post.post_id,
            }))
    context = {
        'post': post,
        'next_post': next_post,
        'form': form,
        'comments': comments,

    }
    return render(request, 'post.html', context)


@login_required
def like(request, post_id):
    post = get_object_or_404(Post, post_id=str(post_id))
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    elif user in post.dislikes.all():
        post.dislikes.remove(user)
        post.likes.add(user)
    else:
        post.likes.add(user)

    return redirect(reverse("post", kwargs={
        'post_id': post.post_id,
    }))


@login_required
def dislike(request, post_id):
    post = get_object_or_404(Post, post_id=str(post_id))
    user = request.user

    if user in post.dislikes.all():
        post.dislikes.remove(user)

    elif user in post.likes.all():
        post.likes.remove(user)
        post.dislikes.add(user)
    else:
        post.dislikes.add(user)

    return redirect(reverse("post", kwargs={
        'post_id': post.post_id,
    }))


@login_required
def like_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, post_id=str(post_id))
    comment = get_object_or_404(Comment, id=int(comment_id))
    user = request.user
    if user in comment.likes.all():
        comment.likes.remove(user)
    elif user in comment.dislikes.all():
        comment.dislikes.remove(user)
        comment.likes.add(user)
    else:
        comment.likes.add(user)

    return redirect(reverse("post", kwargs={
        'post_id': post.post_id,
    }))


@login_required
def dislike_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, post_id=str(post_id))
    comment = get_object_or_404(Comment, id=int(comment_id))
    user = request.user

    if user in comment.dislikes.all():
        comment.dislikes.remove(user)

    elif user in comment.likes.all():
        comment.likes.remove(user)
        comment.dislikes.add(user)
    else:
        comment.dislikes.add(user)

    return redirect(reverse("post", kwargs={
        'post_id': post.post_id,
    }))


def random_post(request):
    posts = Post.objects.all()
    rand_post = random.choice(posts)
    print(random_post)
    return redirect(reverse("post", kwargs={
        'post_id': rand_post.post_id
    }))


@login_required
def deletePost(request, post_id):
    post = Post.objects.filter(post_id=post_id).delete()
    return redirect('index')


@login_required
def updatePost(request, post_id):
    post = get_object_or_404(Post, post_id=str(post_id))
    form = PostForm(request.POST or None, instance=post)
    context = {'form': form}
    if form.is_valid():
        post = form.save(commit=False)

        post.save()

        context = {'form': form,
                   }

        return redirect(reverse("post", kwargs={
            'post_id': post.post_id
        }))

    else:
        context = {'form': form,

                   'error': 'The form was not updated successfully. Please enter in a title and content'}
        return render(request, 'upload.html', context)
