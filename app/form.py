from django import forms

class sentence_form(forms.Form):
    sentence = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type': 'text', 'placeholder' : 'Enter Sentence / Paragraph'}), required=True)

class language_select_form(forms.Form):
    my_choices = (
        ('mr' , 'Marathi'),
        ('hi' , 'Hindi')
    )
    language = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)