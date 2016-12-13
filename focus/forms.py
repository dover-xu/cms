from django import forms


class SetInfoForm(forms.Form):
    username = forms.CharField()


class CommentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': '60', 'rows': '6'}))


class SearchForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput)
