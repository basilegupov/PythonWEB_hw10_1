from django.shortcuts import render, redirect
from django.db.models import Count
from django.core.paginator import Paginator

from .utils import get_mongodb
from bson.objectid import ObjectId
from .models import Quote, Tag, Author
from .forms import QuoteForm, AuthorForm, TagForm
from django.contrib.auth.decorators import login_required


def main(request, page=1, num_tags=10):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:num_tags]
    latest_quote = Quote.objects.latest('created_at')
    tags_for_latest_quote = latest_quote.tags.all()
    author_for_latest_quote = Author.objects.get(id=latest_quote.author_id)
    return render(request, 'quotes/index.html',
                  context={"quotes": quotes_on_page,
                           'tags10': tags,
                           'latest_quote': latest_quote,
                           'author_for_latest_quote': author_for_latest_quote,
                           'tags_for_latest_quote': tags_for_latest_quote})


def author_about(request, author_id, num_tags=10):
    db = get_mongodb()
    author = db.authors.find_one({'_id': ObjectId(author_id)})
    tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:num_tags]
    return render(request, 'quotes/author.html', context={'author': author, 'tags10': tags})


def tag_page(request, tag_name, num_tags=10):
    tag = Tag.objects.get(name=tag_name)
    quotes_with_tag = Quote.objects.filter(tags=tag)
    tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:num_tags]
    return render(request, 'quotes/tag.html', {'quotes_with_tag': quotes_with_tag, 'tag': tag, 'tags10': tags})


def render_tags(request, num_tags=10, template_name='quotes/top_tags.html'):
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:num_tags]
    context = {'top_tags': top_tags}
    tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:num_tags]
    return render(request, template_name, context, {'tags10': tags})


def author_for_tag(request, author_id, num_tags=10):
    author = Author.objects.get(id=author_id)
    tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:num_tags]
    return render(request, 'quotes/author_for_tag.html', context={'author': author, 'tags10': tags})


@login_required  # Проверяет, что пользователь авторизован, прежде чем позволить доступ к представлению.
def add_author(request):  # Обработчик запроса для добавления нового автора.
    if request.method == 'POST':  # Проверка метода запроса (POST или GET).
        form = AuthorForm(request.POST)  # Создание формы на основе POST данных.
        if form.is_valid():  # Проверка валидности данных из формы.
            new_author = form.save(commit=False)  # Создание нового автора без сохранения в БД.
            new_author.user = request.user  # Установка пользователя как создателя автора.
            new_author.save()  # Сохранение автора в БД.
            return redirect(to='quotes:root')  # Перенаправление на главную страницу.
        else:
            return render(request, 'quotes/add_author.html',
                          context={'form': form})  # Отображение формы с ошибками валидации.
    return render(request, 'quotes/add_author.html',
                  context={'form': AuthorForm()})  # Отображение пустой формы для ввода.


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():

            new_quote = form.save(commit=False)
            new_quote.user = request.user
            # Получаем объект Author из формы
            author_name = form.cleaned_data["author"]
            author = Author.objects.get(fullname=author_name)
            new_quote.author = author  # Присваиваем объект Author цитате
            new_quote.save()
            form.save_m2m()  # Сохраняем ManyToManyField (теги)
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_quote.html', context={'form': form})
    return render(request, 'quotes/add_quote.html', context={'form': QuoteForm()})


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_tag.html', context={'form': form})
    return render(request, 'quotes/add_tag.html', context={'form': TagForm()})
