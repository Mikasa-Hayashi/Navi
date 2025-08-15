from django import forms
from .models import Companion


class CompanionCreationForm():
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Navi',
        }),
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            },
        ),
    )
    gender = forms.ChoiceField(
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
    )
    eye_color = forms.ChoiceField(
        choices=[
            ('blue', 'Blue'),
            ('green', 'Green'),
            ('brown', 'Brown'),
            ('gray', 'Gray'),
            ('amber', 'Amber'),
        ],
    )
    hair_color = forms.ChoiceField(
        choices=[
            ('blonde', 'Blonde'),
            ('brown', 'Brown'),
            ('black', 'Black'),
            ('grey', 'Grey'),
            ('white', 'White'),
            ('red', 'Red'),
        ],
    )
    create_dialog = forms.BooleanField(
        required=False, 
        label='Create conversation',
    )

    class Meta:
        model = Companion
        fields = ['name', 'birth_date', 'gender', 'eye_color', 'hair_color', 'create_dialog']