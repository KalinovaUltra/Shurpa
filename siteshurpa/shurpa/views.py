from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import  render_to_string

from shurpa.forms import AddPostForm, UploadFileForm
from shurpa.models import Shurpa, Category, TagPost, UploadFiles
from django.http import JsonResponse

from shurpa.templatetags.yandex_gpt import ask_yandex_gpt


def chat_with_gpt(request):
    response = None
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        response = ask_yandex_gpt(user_message)
    return render(request, 'shurpa/chat.html', {'response': response})

menu = ["О Сайте","Отзывы"]
data_db=[
    {'id': 1, 'title': 'Кыстыбый', 'content': 'Цена', 'is_published': True},
    {'id': 2, 'title': 'Токмач', 'content': 'Цена', 'is_published': False},
    {'id': 3, 'title': 'Элеш', 'content': 'Цена', 'is_published': True},
]

def test(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
    }
    return render(request, 'shurpa/test.html', context= data)


def index(request):
    #t=render_to_string('shurpa/index.html')
    #return HttpResponse(t)
    posts= Shurpa.published.all()


    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
        'cats': Category.objects.all(),
    }
    return render(request,'shurpa/index.html',context= data)

def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required
def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'shurpa/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})


def otziv(request):
    return render(request, 'shurpa/otziv.html', {'title': 'Отзывы'})

def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")

def categories_by_slug(request, cat_slug):
    print(request.POST)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")

def archive(request, year):
    if year > 2023:
        uri = reverse('cat', args=('sport', ))
        return HttpResponsePermanentRedirect(uri)
    return HttpResponse(f"<h1>Архив по годам</h1><p> {year}</p>")

def show_post(request, post_slug):
    post = get_object_or_404(Shurpa, slug=post_slug)

    data= {
        'title': post.title,
        'content': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'shurpa/post.html', data)

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Shurpa.published.filter(cat_id=category.pk)
    data = {
        'title': f'Меню: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
        'cats': Category.objects.all(),
}
    return render(request, 'shurpa/index.html',context=data)

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Shurpa.Status.PUBLISHED)

    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
        'cats': Category.objects.all(),
    }
    return render(request, 'shurpa/index.html', context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def contacts_view(request):
    context = {
        'company_address': "ул. Ленина, 10, Москва, Россия",  # Замените на ваш адрес
    }
    return render(request, 'contacts.html', context)

@login_required
@permission_required('shurpa.add_shurpa', raise_exception=True)
def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # Присваиваем текущего пользователя как автора
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = AddPostForm()

    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }
    return render(request, 'shurpa/addpage.html', data)
