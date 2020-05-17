from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .models import *
# Create your views here.
def landing(request):
    return render(request,"landing.html")

def signup(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        email=request.POST["email"]
        user=User.objects.create_user(username=username,password=password,email=email)
        login(request,user)

        #subject = "Welcome to BlogPost!!!"
        #message = f"Hi {user.username}, use this application for reading and posting the blogs."
        #email_from = settings.EMAIL_HOST_USER
        #recipient_list = [user.email,]
        #send_mail(subject,message,email_from,recipient_list)
        
        return redirect("/home/")
    return render(request,"signup.html")


def signin(request):
    context = {}
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(username=username,password=password)
        if user :
            login(request,user)
            return redirect("/home/")
        else:
            context['error']="Provide valid credentials!!"
            return render(request,'login.html',context)
    return render(request,"login.html",context)

def signout(request):
    logout(request)
    return redirect("/login/")

def home(request):
    all_posts = BlogPost.objects.all()
    return render(request,"home.html",{"all":all_posts})

def post_page(request,post_id):

    post = BlogPost.objects.get(pk=post_id)
    comment=Comment.objects.filter(blog=post)
    print(request.user,post.author)

    return render(request,"post_page.html",{"post":post,"comment":comment})


def create_post(request):
    if request.method=="POST":
        title=request.POST["title"]
        content=request.POST["content"]
        author=request.user
        
        new_post=BlogPost.objects.create(title=title,content=content,author=author,cover=request.FILES["cover"])
        return redirect("/home/")
    return render(request,"create.html")

def delete(request,post_id):
    post=BlogPost.objects.get(pk=post_id)
    user = request.user

    if user.username == post.author:
        post.delete()
        return redirect("/home/")
    else:
        return redirect(f'/post/{post_id}/')

def edit_post(request,post_id):
    user = request.user
    post=BlogPost.objects.get(pk=post_id)

    if user.username == post.author:
        if request.method=="POST":
            title=request.POST["title"]
            content=request.POST["content"]
            
            post.title=title
            post.content=content
            if request.FILES:
                post.cover=request.FILES["cover"]
            post.save()
            return redirect(f"/post/{post.id}/")
    else:
        return redirect(f'/post/{post_id}/')
    return render(request,"edit_post.html",{"post":post})

def comment(request,post_id):
    user=request.user
    context={}
    blog_instance=BlogPost.objects.get(pk=post_id)
    comment=Comment.objects.filter(blog=blog_instance)
    if request.method=="POST":
        if user.is_authenticated:
            comment=request.POST["comment"]
            reader=request.user
            blog=blog_instance
            comment_instance=Comment.objects.create(
                comment=comment,
                reader=reader,
                blog=blog,
                )
            return redirect(f"/post/{blog.id}/")
        else:
            context["error"]="Please login!!!"
            return render(request,"login.html",context)
    return render(request,"post_page.html",{"blog":blog_instance,"comment":comment})


def like(request,post_id):
    context={}
    user=request.user
    if  user.is_authenticated:
        blog=BlogPost.objects.get(pk=post_id)
        like=Like.objects.filter(reader=request.user,blog=blog)
        if like :
            return redirect(f"/post/{post_id}/")
        blog.likes +=1
        blog.save()
        like=Like.objects.create(reader=request.user,blog=blog)
        return redirect(f"/post/{blog.id}/")
    else:
        context["error"]="Please login!!!"
        return render(request,"login.html",context)

def delete_comment(request,comment_id,post_id):
    comment_instance=Comment.objects.get(pk=comment_id)
    comment_instance.delete()
    return redirect(f'/post/{post_id}/')