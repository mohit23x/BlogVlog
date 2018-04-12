from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView, ListView, DeleteView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Blog, Comment, CommentReply, Document, UserImage, UserInfo, Hashtag
from django.urls import reverse_lazy
from .forms import CommentForm, CommentReplyForm, DocumentForm, BlogForm, UserImageForm, UserInfoForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms import formset_factory, modelformset_factory
from PIL import Image
from django import forms
from simple_search import search_filter
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




class Homepage(ListView):
    model = Blog
    template_name = 'homepage.html'
    paginate_by = 10

    context_object_name = 'object_list'
    model = Blog

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        context.update({
            'hashtag': Hashtag.objects.order_by('name'),
        })
        return context

    def get_queryset(self):
        return Blog.objects.all().order_by('-date')






class AboutUs(TemplateView):
    template_name = 'aboutus.html'


def newpost(request):
    hashtag = Hashtag.objects.all().order_by('name')
    
    DocumentFormSet = modelformset_factory(Document, form=DocumentForm, extra=5)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        formset = DocumentFormSet(request.POST, request.FILES, queryset=Document.objects.none())

        if form.is_valid() and formset.is_valid:
            neww_post = form.save()
            neww_post.author = User.objects.get(username=request.user.username)
            neww_post.save()
            try:
                for f in formset.cleaned_data:
                    image = f['image']
                    photo = Document(blog=neww_post, image=image)
                    photo.save()
            except:
                pass
            return redirect('homepage')
    else:
        form = BlogForm
        formset = DocumentFormSet(queryset=Document.objects.none())
        return render(request, 'postnew.html', {'form':form, 'formset':formset, 'hashtag':hashtag})



def user_image_func(request):
    hashtag = Hashtag.objects.all().order_by('name')
    
    user = User.objects.get(username=request.user.username)
    try:
        imgdata = UserImage.objects.get(author=user)
    except:
        imgdata = None

    if request.method == 'POST':    

        try:
            form = UserImageForm(request.POST, request.FILES)
            
            if form.is_valid():
                don = form.save()
                user = User.objects.get(username=request.user.username)
                don.author = user
                don.save()
                return redirect('homepage')

        except:
            form = UserImageForm(request.POST)

            if form.is_valid():
                imgdata.description = form.changed_data['description']
                imgdata.designation = form.cleaned_data['designation']
                imgdata.displayname = form.cleaned_data['displayname']
                imgdata.save()
                return redirect('homepage')
    else:
        if imgdata:
            form = UserImageForm(initial={'displayname': imgdata.displayname, 'description':imgdata.description, 'designation':imgdata.designation })
            return render(request, 'userimage.html', {'form': form, 'hashtag':hashtag})
        else:
            form = UserImageForm()
            return render(request, 'userimage.html', {'form': form, 'hashtag':hashtag})



def PostDetail(request, pk):
    hashtag = Hashtag.objects.all().order_by('name')
    form1 = CommentForm
    form2 = CommentReplyForm
    data1 = Blog.objects.get(pk=pk)
    com = Comment.objects.filter(blog=data1)
    replycom = CommentReply.objects.filter(blog=data1)
    documents = Document.objects.filter(blog=data1)
    authorinfo = UserImage.objects.get(author=data1.author)
    userinfo_object = UserInfo.objects.get(author=data1.author)
  
    if request.method == 'POST':
        
        if request.POST.get('whichcomment'):
            data3 = CommentReplyForm(request.POST)

            if data3.is_valid():
                whichcomment = int(request.POST.get('whichcomment'))
                message = data3.cleaned_data['message']
#                user = User.objects.get(username=request.user.username)
#                usrimg = UserImage.objects.get(author=user)

                don = data3.save(commit=False)
                don.blog=data1
                don.user=User.objects.get(username=request.user.username)
                don.message = message
                don.whichcomment = Comment.objects.get(id=whichcomment)
                don.usrimg = UserImage.objects.get(author=don.user)
                don.save()

                return HttpResponseRedirect(reverse('postdetail', args=(), kwargs={'pk': pk}))

        else:
            data2 = CommentForm(request.POST)

            if data2.is_valid():
                blog = data1
                message = data2.cleaned_data['message']
#                usr = User.objects.get(user=request.user.username),
#                usrimg = UserImage.objects.get(author=usr)

                don = data2.save(commit=False)
                don.blog=data1
                don.user=User.objects.get(username=request.user.username)
                don.message = message
                don.usrimg = UserImage.objects.get(author=don.user)
                don.save()

                '''Comment.objects.create(
                    blog=data1,
                    user= User.objects.get(username=request.user.username),
                    message=message,
                    usrimg=UserImage.objects.get(author=user)

                ).save()'''

                return HttpResponseRedirect(reverse('postdetail', args=(), kwargs={'pk': pk}))
                
    else:
        return render(request, 'details mockup.html', {'data1': data1, 'form1':form1, 'com': com, 'form2':form2, 'replycom':replycom, 'documents':documents, 'authorinfo':authorinfo, 'userinfo_object':userinfo_object, 'hashtag':hashtag})
    


class PostEdit(UpdateView):
    model = Blog
    template_name  = 'blogedit.html'
    fields = '__all__'


class BlogPostNew(CreateView):
    model = Blog
    template_name = 'poatnew.html'
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

    

def profile(request, nam):
    hashtag = Hashtag.objects.all().order_by('name')
    mainuser = User.objects.get(username = nam)
    blogs = Blog.objects.filter(author = mainuser)
    form = UserImageForm()

    try:
        data = UserImage.objects.get(author = mainuser)
    except:
        #user visiting his profile for first time so creating UserImage instance for him
        d = UserImage.objects.create(
            author = mainuser
        ).save()
    
        data = UserImage.objects.get(author = mainuser)

    try:
        userinfo = UserInfo.objects.get(author = mainuser)
    except:
        #visit to profile for first time so creating Userinfo model instance for him
        e = UserInfo.objects.create(
            author = mainuser
        ).save()
    
        userinfo = UserInfo.objects.get(author = mainuser)

    # user profile view count condiiton
    if str(request.user) == (nam):
        pass
    else:
        userinfo.views = userinfo.views + 1
        userinfo.save()


    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            don = form.save()
            user = User.objects.get(username=request.user.username)
            don.author = user
            don.save()
            return render(request, 'profile.html', {'data':data, 'mainuser':mainuser, 'blogs':blogs, 'form':form, 'userinfo':userinfo, 'hashtag':hashtag})

    else:
        return render(request, 'profile.html', {'data':data, 'mainuser':mainuser, 'blogs':blogs, 'form':form, 'userinfo':userinfo, 'hashtag':hashtag})



def userInfoFormView(request, pk):
    hashtag = Hashtag.objects.all().order_by('name')

    mainuser = User.objects.get(pk = pk)
    userinfo_object = UserInfo.objects.get(author = mainuser)

    form = UserInfoForm(initial={'displayname':userinfo_object.displayname, 'designation':userinfo_object.designation, 'description':userinfo_object.description, 'birthdate':userinfo_object.birthdate, 'email':mainuser.email})


    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            userinfo_object.displayname = form.cleaned_data["displayname"]
            userinfo_object.designation = form.cleaned_data["designation"]
            userinfo_object.description = form.cleaned_data["description"]
            userinfo_object.birthdate = form.cleaned_data["birthdate"]
            userinfo_object.views = int(userinfo_object.views) + 1
            userinfo_object.save()

            mainuser.first_name = userinfo_object.displayname
            mainuser.email = form.cleaned_data["email"]
            mainuser.save()
            return redirect('profile', mainuser)

    return render(request, 'editinfo.html', {'form':form, 'hashtag':hashtag})





def search(request):
    hashtag = Hashtag.objects.all().order_by('name')
    referer = request.META.get('HTTP_REFERER')

    try:
        query = request.GET["q"]
    except:
        query = ''

    err = ''
    checklist = ['<', 'br', '>', '<br>', '<strong>', '<hr>', 'hr', 'strong', 'p', '<p>', '<ul>', 'ul', '<li>', 'li', '<s', '<str', '<Stron', '<h', 'g>', 'on>', 'ron>', 'tron>', 'strong>', '<l', 'i>', 'li>', '<u', 'l>']

    if str(query) in checklist:
        err = 'Type something else'
        query = ''

    search_fields = ['title', 'text']
    f = search_filter(search_fields, query)
    filtered1 = Blog.objects.filter(f)

    search_field2 = ['displayname']
    ff = search_filter(search_field2, query)
    filtered2 = UserInfo.objects.filter(ff)
        
    return render(request, 'search.html', {'results1':filtered1, 'results2': filtered2, 'ref': referer, 'err':err, 'hashtag':hashtag})




def categoryview(request, hashtags):
    hash = Hashtag.objects.get(name=hashtags)
    hashtag = Hashtag.objects.all().order_by('name')
    try:
        object_list = Blog.objects.filter(category=hash)
    except:
        object_list = ''
        err = 'No post in this category'
        return render(request, 'categoryview.html', {'object_list':object_list, 'err':err, 'hashtag':hashtag})

    return render(request, 'categoryview.html', {'object_list':object_list, 'hashtag':hashtag})



    
    '''
    
    <link rel="stylesheet" href="https://cdn.metroui.org.ua/v4/css/metro.min.css">
    <link rel="stylesheet" href="https://cdn.metroui.org.ua/v4/css/metro-colors.min.css">
    <link rel="stylesheet" href="https://cdn.metroui.org.ua/v4/css/metro-rtl.min.css">
    <link rel="stylesheet" href="https://cdn.metroui.org.ua/v4/css/metro-icons.min.css">
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script src="https://cdn.metroui.org.ua/v4/js/metro.min.js"></script>

    '''