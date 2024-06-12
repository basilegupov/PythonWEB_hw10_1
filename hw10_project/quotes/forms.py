from django.forms import ModelForm, CharField, TextInput, ModelMultipleChoiceField, SelectMultiple, Select, Textarea, \
    ChoiceField, ModelChoiceField

from .models import Tag, Author, Quote


class AuthorForm(ModelForm):
    fullname = CharField(max_length=100, required=True, widget=TextInput(attrs={"class": "form-control"}))
    born_date = CharField(max_length=50, required=True, widget=TextInput(attrs={"class": "form-control"}))
    born_location = CharField(max_length=100, required=True, widget=TextInput(attrs={"class": "form-control"}))
    description = CharField(required=True, widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=50, required=True, widget=TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Tag
        fields = ['name']
        exclude = ['tags']


class QuoteForm(ModelForm):
    quote = CharField(required=True, widget=TextInput(attrs={"class": "form-control"}))
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all().order_by('name'),
                                    widget=SelectMultiple(attrs={"class": "form-select", "size": "7"}))
    author = ModelChoiceField(queryset=Author.objects.all().order_by('fullname'))

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']
