from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from .models import Post,AboutUs
from django.http import Http404
from django.core.paginator import Paginator
from .forms import ContactForm


# Create your views here.

#   posts=[
#       {'id':1,'title':'POST1','content':'Content of post 1'},
#       {'id':2,'title':'POST2','content':'Content of post 2'},
#       {'id':3,'title':'POST3','content':'Content of post 3'},
#       {'id':4,'title':'POST4','content':'Content of post 4'}
#        ]

def index(request):

    # GETTING POST DATA BY ID 
    all_posts = Post.objects.all()

    # PAGINATOR

    paginator = Paginator(all_posts,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request,'blog/index.html',{'page_obj':page_obj})

def detail(request,slug):
   # STATIC DATA
   #  post=next((item for item in posts if item['id'] == int(post_id)),None)
   
    # GETTING DATA FROM MODEL BY POST ID 
    try:
        # post= Post.objects.get(pk=post_id)
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category = post.category).exclude(pk = post.id)

    except Post.DoesNotExist:
        raise Http404("Page does not exist")
    
    return render(request,'blog/detail.html',{'post':post,'related_posts':related_posts})

def old_url_redirect(request):
    return redirect(reverse('blog:new_page_url'))

def new_url_view(request):
    return HttpResponse("This is the new url")

def contact_view(request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')

            logger = logging.getLogger("TESTING")
            
            if form.is_valid():
              logger.debug('POST Data is valid')
              #send email or save in database
              success_message = 'Your Email has been sent!'
              return render(request,'blog/contact.html', {'form':form,'success_message':success_message})
            else:
             logger.debug('Form validation failure')
             return render(request,'blog/contact.html', {'form':form, 'name': name, 'email':email, 'message': message})
        return render(request,'blog/contact.html')

def about_view(request):
    about_content = AboutUs.objects.first().content
    return render(request,'blog/about.html')