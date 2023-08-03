from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import ArticleForm
from .models import Article, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request, "articles.html", {"articles": articles})

    articles = Article.objects.all()

    return render(request, "articles.html", {"articles": articles})

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

@login_required(login_url = "user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)

    return render(request, "dashboard.html", {"articles": articles})

@login_required(login_url = "user:login")
def create(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit =False)
        article.author = request.user
        article.save()

        messages.success(request, "Makale başarıyla oluşturuldu.")
        return redirect("article:dashboard")
    
    return render(request, "create.html", {"form": form})

def detail(request, id):
    # article = Article.objects.filter(id = id).first()

    article = get_object_or_404(Article, id = id)
    comments = Comment.objects.filter(article = article)

    return render(request, "detail.html", {"article": article, "comments": comments})

@login_required(login_url = "user:login")
def edit(request, id):
    article = get_object_or_404(Article, id = id)

    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)

    if form.is_valid():
        article = form.save(commit =False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale başarıyla düzenlendi.")
        return redirect("article:dashboard")

    return render(request, "edit.html", {"form": form})

@login_required(login_url = "user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id = id)

    article.delete()

    messages.success(request, "Makale başarıyla silindi.")

    return redirect("article:dashboard")

@login_required(login_url = "user:login")
def addComment(request, id):
    article = get_object_or_404(Article, id = id)

    if request.method == "POST":
        comment_author = request.user
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article

        newComment.save()

    return redirect(reverse("article:detail", kwargs={"id": id}))