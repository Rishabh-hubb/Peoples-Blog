from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic.detail import SingleObjectMixin 
from django.urls import reverse_lazy, reverse 
from blog.forms import CommentForm, BlogCreateForm, ContactForm
from django_blog import settings
from .models import Post, Comment, Category
from django.contrib import messages
from django.db.models import Count

class BlogListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3


class CommentGet(DetailView):  # new
    model = Post
    template_name = "blog/post_detail.html"
    ordering = ['-date_added']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin,FormView):  # new
    model = Post
    form_class = CommentForm
    ordering = ['-date_added']
    template_name = "blog/post_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user

        comment = form.save(commit=False)
        comment.post = self.object

        comment.save()
        messages.info(self.request,"Comment added Successfully")
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()

        return reverse("blog-detail", kwargs={"pk": article.pk})


class UserPostListView(ListView):
    model = Post
    
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class BlogDetailView(DetailView):
    model = Post

        
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)
 

class BlogPostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog-home')


    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request,'Blog created successfully')
        return super().form_valid(form)

class CategoryCreateView(LoginRequiredMixin,CreateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('blog-home')

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class BlogPostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    form_class = BlogCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class BlogDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#def home(request):
#    context = {
#        'posts': Post.objects.all()
#    }
#   return render(request,'blog/home.html',context)



class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'
    success_url = '/'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        messages.success(self.request, f"The comment has been deleted successfully")
        return reverse_lazy('blog-detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user


class SearchView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'posts'


    def queryset(self):
        query = self.request.GET.get('search')
        if query and len(query) < 25:
            object_list_content = self.model.objects.filter(content__icontains=query)

            object_list_category = self.model.objects.filter(category__name__icontains=query)
            print(object_list_category)

            object_list_title = self.model.objects.filter(title__icontains=query)
            object_list = object_list_title.union(object_list_content,object_list_category)
            print(object_list)
        else:
            object_list = self.model.objects.none()

        return object_list

class ContactView(FormView):
    form_class = ContactForm
    template_name = 'blog/about.html'
    success_url = reverse_lazy('blog-about')


    def form_valid(self, form):
        message = "{name} / {email} said: ".format(
            name=form.cleaned_data.get('name'),
            email=form.cleaned_data.get('email'))
        message += "\n\n{0}".format(form.cleaned_data.get('message'))
        send_mail(
            subject=form.cleaned_data.get('subject').strip(),
            message=message,
            from_email='contact-form@myapp.com',
            recipient_list=[settings.EMAIL_HOST_USER],
        )
        messages.success(self.request,f"Thank You! We Will get back to You Very soon")

        return super(ContactView, self).form_valid(form)






    





