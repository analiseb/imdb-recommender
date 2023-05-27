from django import forms

class MovieForm(forms.Form):
    movie_ref = forms.CharField(
        label=False, 
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'What is a movie you like?',
            'class': 'form-control'
            })
        )
