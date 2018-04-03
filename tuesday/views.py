from django.shortcuts import render, reverse
from .models import Comment, CommentForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.


def tuesday(request):
    data = Comment.objects.filter(parent__isnull=True)
    form = CommentForm

    if request.method == 'POST':
        entry = CommentForm(request.POST)
        parent_obj = None

        if entry.is_valid():
            message = entry.cleaned_data['message']

            try:
                parent_id = int(request.POST.get('parent'))
            except:
                parent_id = None
            
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)

                if parent_obj:
                    reply_comment = entry.save(commit=False)

                    reply_comment.message = message
                    reply_comment.parent = parent_obj
                    reply_comment.author = User.objects.get(username=request.user.username)
                    reply_comment.save()
    
                    return HttpResponseRedirect(reverse('tuesday'))
    
            new_comment =  entry.save(commit=False)
            new_comment.message = message
            new_comment.author = User.objects.get(username=request.user.username)
            new_comment.save()

            return HttpResponseRedirect(reverse('tuesday'))
    
    else:
        return render(request, 'tuesday/tuesday.html', {'data': data, 'form': form})