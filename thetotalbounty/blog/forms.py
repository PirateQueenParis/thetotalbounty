from django import forms

class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea({"class": "form-control", "placeholder": "Leave a comment!"}), min_length=1, max_length=1000)

class DisplayNameForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput({"class": "form-control", "placeholder": ""}), min_length=1, max_length=100)