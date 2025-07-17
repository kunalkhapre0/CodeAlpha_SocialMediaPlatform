from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileUpdateForm, PostCreateForm, CommentForm
from .models import Profile, Post, Comment, Follow
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome.')
            return redirect('home') # Or 'profile_edit' to fill profile
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at') # Assuming you want posts here

    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        # Check if the logged-in user is following the profile_user
        if Follow.objects.filter(follower=request.user, following=profile_user).exists():
            is_following = True

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following, # Add this to the context
    }
    return render(request, 'social/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        # User form can be added if you want to edit User model fields like first_name, last_name, email
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }
    return render(request, 'social/profile_edit.html', context)

@login_required
def home_view(request):
    # For now, show all posts. Later, this could be posts from followed users.
    posts = Post.objects.all().order_by('-created_at')
    comment_form = CommentForm() # For adding comments directly on the feed
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'social/home.html', context)

@login_required
def placeholder_post_create_view(request):
    return HttpResponse("Post creation page - Coming in Phase 2!")

@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostCreateForm()
    return render(request, 'social/post_form.html', {'form': form, 'type': 'Create'})


@login_required # Or allow public view
def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('created_at') # Or '-created_at'
    comment_form = CommentForm()

    if request.method == 'POST': # Handling comment submission
        # Ensure it's for the comment form and not another form if you add more
        # For simplicity, assuming any POST here is a comment
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            comment = c_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('post_detail', pk=post.pk) # Redirect to refresh and show new comment
    else: # GET request
        c_form = CommentForm()


    context = {
        'post': post,
        'comments': comments,
        'comment_form': c_form, # Pass the form instance
    }
    return render(request, 'social/post_detail.html', context)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreateForm # Can use the same form
    template_name = 'social/post_form.html'
    # success_url = reverse_lazy('home') # Or redirect to post_detail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
@login_required
def add_comment_to_post(request, pk): # pk is post's pk
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            # Redirect to the post detail or the part of the page with the post
            # If using AJAX, return JsonResponse
            return redirect(request.META.get('HTTP_REFERER', 'home')) # Redirect to previous page
    else:
        # This view is primarily for POST, but redirect if GET
        return redirect('post_detail', pk=pk)
    
@login_required
def like_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'like':
            post.likes.add(request.user)
            messages.success(request, f'You liked the post "{post.content[:30]}..."')
        elif action == 'unlike':
            post.likes.remove(request.user)
            messages.success(request, f'You unliked the post "{post.content[:30]}..."')
    # Redirect to the previous page or a specific page
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def toggle_follow_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow == request.user:
        messages.warning(request, "You cannot follow yourself.")
        return redirect('profile', username=username)

    follow_instance, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )

    if created:
        messages.success(request, f'You are now following {username}.')
    else:
        follow_instance.delete()
        messages.success(request, f'You have unfollowed {username}.')

    return redirect('profile', username=username)

@login_required
def home_view(request):
    followed_users = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    # Include user's own posts in the feed as well
    users_for_feed = list(followed_users) + [request.user.id]

    posts = Post.objects.filter(author__id__in=users_for_feed).order_by('-created_at')
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'social/home.html', context)


def search_users_view(request):
    query = request.GET.get('q')
    raw_results = []
    users_with_follow_status = [] # New list to hold users and their follow status

    if query:
        raw_results = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).distinct()

        if request.user.is_authenticated:
            # Exclude the current user from results
            raw_results = raw_results.exclude(pk=request.user.pk)

            # Get IDs of users that the current user is following
            following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
            for user_obj in raw_results:
                users_with_follow_status.append({
                    'user': user_obj,
                    'is_followed_by_current_user': user_obj.pk in following_ids
                })
        else: # For anonymous users
            for user_obj in raw_results:
                users_with_follow_status.append({
                    'user': user_obj,
                    'is_followed_by_current_user': False # Anonymous users can't follow
                })
    else: # No query
        # To prevent 'users_with_follow_status' from being undefined if query is None
        users_with_follow_status = []


    context = {
        'query': query,
        'results': users_with_follow_status, # Pass the new list to the template
    }
    return render(request, 'social/search_results.html', context)