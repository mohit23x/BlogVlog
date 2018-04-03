from django.shortcuts import render, reverse
from django.views.generic import TemplateView, ListView, DeleteView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blog, Comment, CommentReply
from django.urls import reverse_lazy
from .forms import CommentForm, CommentReplyForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


class Homepage(ListView):
    model = Blog
    template_name = 'homepage.html'

'''class PostDetail(DetailView):
    model = Blog
    template_name = 'postdetail.html'''

def PostDetail(request, pk):
    form1 = CommentForm
    form2 = CommentReplyForm
    data1 = Blog.objects.get(pk=pk)
    com = Comment.objects.filter(blog=data1)
    replycom = CommentReply.objects.filter(blog=data1)
  
    if request.method == 'POST':
        
        if request.POST.get('whichcomment'):
            data3 = CommentReplyForm(request.POST)

            if data3.is_valid():
                whichcomment = int(request.POST.get('whichcomment'))
                message = data3.cleaned_data['message']

                CommentReply.objects.create(
                    whichcomment = Comment.objects.get(id=whichcomment),
                    user = User.objects.get(username=request.user.username),
                    message = message,
                    blog=data1

                ).save()

                return HttpResponseRedirect(reverse('postdetail', args=(), kwargs={'pk': pk}))
                #return render(request, 'postdetail.html', {'data1': data1, 'form1':form1, 'com':com, 'form2':form2, 'replycom':replycom})
 

        else:
            data2 = CommentForm(request.POST)
    
            if data2.is_valid():
                blog = data1,
                message = data2.cleaned_data['message']
                

                Comment.objects.create(
                    blog=data1,
                    user= User.objects.get(username=request.user.username),
                    message=message
                ).save()

                return HttpResponseRedirect(reverse('postdetail', args=(), kwargs={'pk': pk}))
                
    else:
        return render(request, 'postdetail.html', {'data1': data1, 'form1':form1, 'com': com, 'form2':form2, 'replycom':replycom})
    


class BlogPostNew(CreateView):
    model = Blog
    template_name = 'poatnew.html'
    fields = '__all__'

class PostEdit(UpdateView):
    model = Blog
    template_name  = 'blogedit.html'
    fields = '__all__'


class BlogDelete(DeleteView):
    model= Blog
    template_name = 'blogdelete.html'
    success_url = reverse_lazy('homepage')

class MyPost(ListView):
    template_name = 'mypost.html'
    context_object_name = 'authorallpost'

    def get_queryset(self):
        return Blog.objects.filter(author__username=self.kwargs['author'])


class CommentReplyDelete(DeleteView):
    model = CommentReply
    template_name = 'blogdelete.html'
    success_url = reverse_lazy('homepage')


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'blogdelete.html'
    success_url = reverse_lazy('homepage')

    