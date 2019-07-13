from .models import Product
from django import forms

class NewForm(forms.ModelForm):
    class Meta :
        model = Product
        fields =[
            'Prod_title',
            'Prod_pmail',
            'Prod_model_no',
            'Prod_manufacture',
            'Prod_weight',
            'Prod_no_of_items',
            'Prod_price',
            'Prod_description',
            'Prod_year',
            'Prod_image',
            'Prod_genre',
            'Prod_rating',
        ]