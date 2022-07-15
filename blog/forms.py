from django import forms
from .models import Comment, Post, Category
from django import forms
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple


class BlogCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','category']

    def __init__(self, *args, **kwargs):
        super(BlogCreateForm, self).__init__(*args, **kwargs)

        self.fields["category"].widget = CheckboxSelectMultiple()
        self.fields["category"].queryset = Category.objects.all()




class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            'body': Textarea(attrs={'cols':20,'rows':2}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))




