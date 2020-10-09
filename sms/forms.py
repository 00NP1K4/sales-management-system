from django import forms
from .models import *
import datetime



class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity',]

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')
        return category

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        for i in Stock.objects.all():
            if i.item_name == item_name:
                raise forms.ValidationError(item_name + ' is already created')
        return item_name

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['issue_quantity', 'issue_to']

class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Receive
        fields = ['receive_quantity', 'receive_from']

class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required = False)
    #start_date = forms.DateTimeField(required=False)
    #end_date = forms.DateTimeField(required=False)
    #item_name = forms.CharField(required = False)
    class Meta:
        model = Stock
        fields = ['category', 'item_name']

class IssueSearchForm(forms.ModelForm):
    start_date = forms.DateField(required=False, initial = datetime.date.today() - datetime.timedelta(days=7))
    end_date = forms.DateField(required=False, initial = datetime.date.today())
    export_to_CSV = forms.BooleanField(required = False)
    
    class Meta:
        model = Issue
        fields = [ 'stock', 'issue_to']

class ReceiveSearchForm(forms.ModelForm):
    start_date = forms.DateField(required=False, initial = datetime.date.today() - datetime.timedelta(days=7))
    end_date = forms.DateField(required=False, initial = datetime.date.today())
    export_to_CSV = forms.BooleanField(required = False)
    class Meta:
        model = Receive
        fields = [ 'stock', 'receive_from']
    