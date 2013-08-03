from django import forms

class VoteForm(forms.Form):
    vote = forms.BooleanField(initial=True)
