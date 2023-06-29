"""
-> BookRegisterForm: Formulário responsável por ativar o usuário a partir da chave enviada para ele por email.
"""
from django import forms
from .models import BookRegisterModel


class BookRegisterForm(forms.ModelForm):
    # Forms fields.
    title = forms.CharField(label="Título", max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Qual o nome do livro'}))
    edition = forms.CharField(label="Edição", max_length=50, required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Qual a edição do livro?'}))
    npages = forms.IntegerField(label="Número de páginas", required=False,
                                widget=forms.NumberInput(attrs={'placeholder': 'Quantas páginas tem o livro?'}))
    begin = forms.DateField(label="Início", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    finish = forms.DateField(label="Término", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    concluded = forms.BooleanField(label="Não terminou? Só cliclar na caixinha ao lado", required=False)
    wish = forms.BooleanField(label="É para lista de desejos?", required=False)

    def clean_concluded(self):
        if self.cleaned_data['concluded']:
            self.cleaned_data['concluded'] = False
        else:
            self.cleaned_data['concluded'] = True

        return self.cleaned_data['concluded']

    def clean_wish(self):
        if self.cleaned_data['wish']:
            self.cleaned_data['concluded'] = False

        return self.cleaned_data['wish']

    # Class to add additional metadata inside the form.
    class Meta:
        model = BookRegisterModel  # Template that will be used for the form.
        fields = ['title', 'edition', 'npages', 'concluded', 'begin', 'finish', 'wish']  # Forms view fields.
        ordering = ['id']
