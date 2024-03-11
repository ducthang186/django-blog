# Importing necessary libraries and modules
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CommentForm, PostForm
from django.views import generic

# View to display a list of all posts
@staff_member_required
def post_list(request):
    posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        post.published_at = timezone.now()
        post.save()
        return redirect('post_list')
    return render(request, 'post_list.html', {'posts': posts})


# View to display the details of a specific post
def post_detail(request, pk):
    # Query to get a specific post based on its primary key (pk)
    post = get_object_or_404(Post, pk=pk)
    # Query to get all comments associated with this post
    comments = post.comment_set.all()
    # Checking if the request method is POST to process the form data
    if request.method == "POST":
        form = CommentForm(request.POST)  # Creating a form instance with the submitted data
        if form.is_valid():  # Validating the form data
            comment = form.save(commit=False)  # Saving the form data as a comment object, but not saving to the database yet
            comment.post = post  # Assigning the post to the comment
            comment.author = request.user  # Assigning the logged in user as the author of the comment
            comment.save()  # Saving the comment object to the database
    else:
        form = CommentForm()  # Creating an empty form instance if the request method is not POST
    # Rendering the template post_detail.html with the post, comments, and form data
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

# View to add a comment on a specific post
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)  # Redirecting back to the post detail page
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})

# Additional views for superusers to create, edit, publish posts, and manage drafts
@staff_member_required  # Decorator to ensure only staff members (including superusers) can access this view
def create_post(request):
    # Checking if the request method is POST to process the form data
    if request.method == "POST":
        form = PostForm(request.POST)  # Creating a form instance with the submitted data
        if form.is_valid():  # Validating the form data
            post = form.save(commit=False)  # Saving the form data as a post object, but not saving to the database yet
            post.author = request.user  # Assigning the logged in user as the author of the post
            post.save()  # Saving the post object to the database
            return redirect('post_detail', pk=post.pk)  # Redirecting to the post detail page after successful post creation
    else:
        form = PostForm()  # Creating an empty form instance if the request method is not POST
    # Rendering the template create_edit_post.html with the form data
    return render(request, 'create_edit_post.html', {'form': form})

@staff_member_required  # Decorator to ensure only staff members (including superusers) can access this view
def edit_post(request, pk):
    # Query to get a specific post based on its primary key (pk)
    post = get_object_or_404(Post, pk=pk)
    # Checking if the request method is POST to process the form data
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)  # Creating a form instance with the submitted data and the post instance
        if form.is_valid():  # Validating the form data
            form.save()  # Saving the form data to the database
            return redirect('post_detail', pk=post.pk)  # Redirecting to the post detail page after successful post editing
    else:
        form = PostForm(instance=post)  # Creating a form instance with the post instance if the request method is not POST
    # Rendering the template create_edit_post.html with the form data
    return render(request, 'create_edit_post.html', {'form': form})

@staff_member_required  # Decorator to ensure only staff members (including superusers) can access this view
def publish_post(request, pk):
    # Query to get a specific post based on its primary key (pk)
    post = get_object_or_404(Post, pk=pk)
    post.publish()  # Publishing the post using the publish method defined in the Post model
    return redirect('post_list')  # Redirecting to the post detail page after successful post publishing

@staff_member_required  # Decorator to ensure only staff members (including superusers) can access this view
def draft_list(request):
    # Query to get all draft posts from the database, ordered by creation date in descending order
    drafts = Post.objects.filter(published_at__isnull=True)
    # Rendering the template draft_list.html with the drafts data
    return render(request, 'draft_list.html', {'drafts': drafts})

