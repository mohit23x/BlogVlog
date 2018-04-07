from django.shortcuts import render, reverse
from django.views.generic import TemplateView, ListView, DeleteView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Blog, Comment, CommentReply, Document
from django.urls import reverse_lazy
from .forms import CommentForm, CommentReplyForm, DocumentForm, BlogForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms import formset_factory, modelformset_factory


def mockup(request):
    return render(request, 'details mockup.html')

class Homepage(ListView):
    model = Blog
    template_name = 'homepage.html'
    paginate_by = 5
    queryset = Blog.objects.all()

class AboutUs(TemplateView):
    template_name = 'aboutus.html'

'''class PostDetail(DetailView):
    model = Blog
    template_name = 'postdetail.html'''



def newpost(request):
    
    DocumentFormSet = modelformset_factory(Document, form=DocumentForm, extra=3)

    if request.method == 'POST':
        form = BlogForm(request.POST)
        formset = DocumentFormSet(request.POST, request.FILES, queryset=Document.objects.none())

        if form.is_valid() and formset.is_valid:
            neww_post = form.save(commit=False)
            neww_post.author = User.objects.get(username=request.user.username)
            neww_post.save()
            try:
                for f in formset.cleaned_data:
                    image = f['image']
                    photo = Document(blog=neww_post, image=image)
                    photo.save()
            except:
                pass
            return render(request, 'homepage.html')
    else:
        form = BlogForm        
        formset = DocumentFormSet(queryset=Document.objects.none())
        return render(request, 'postnew.html', {'form':form, 'formset':formset})



def PostDetail(request, pk):
    form1 = CommentForm
    form2 = CommentReplyForm
    data1 = Blog.objects.get(pk=pk)
    com = Comment.objects.filter(blog=data1)
    replycom = CommentReply.objects.filter(blog=data1)
    documents = Document.objects.filter(blog=data1)
  
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
        return render(request, 'details mockup.html', {'data1': data1, 'form1':form1, 'com': com, 'form2':form2, 'replycom':replycom, 'documents':documents})
    


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

    



    '''
    
    <link rel="stylesheet" href="https://cdn.metroui.org.ua/v4/css/metro.min.css">
    <link rel="stylesheet" href="https://cdn.metroui.org.ua/v4/css/metro-colors.min.css">
    <link rel="stylesheet" href="https://cdn.metroui.org.ua/v4/css/metro-rtl.min.css">
    <link rel="stylesheet" href="https://cdn.metroui.org.ua/v4/css/metro-icons.min.css">
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script src="https://cdn.metroui.org.ua/v4/js/metro.min.js"></script>

    '''