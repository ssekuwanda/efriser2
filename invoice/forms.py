from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import *
import json

#Form Layout from Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class DateInput(forms.DateInput):
    input_type = 'date'


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(
                            widget=forms.TextInput(attrs={'id': 'floatingInput', 'class': 'form-control mb-3'}),
                            required=True)
    password = forms.CharField(
                            widget=forms.PasswordInput(attrs={'id': 'floatingPassword', 'class': 'form-control mb-3'}),
                            required=True)

    class Meta:
        model=User
        fields=['username','password']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'companyLogo', 'company_type','tin','device_number']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'business_name',
                  'address', 'email_address', 'contact_number', 'nin_brn','tin']

class InvoiceProductForm(forms.ModelForm):
    class Meta:
        model = InvoiceProducts
        fields = ['product', 'quantity', 'price']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'unit_measure',
                  'unit_price', 'currency', 'commodity_id', 
                  'has_excise_duty', 'description', 'stock_warning', 
                  ]


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['remarks', 'currency', 'payment_method']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows':2})
        }


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['clientName', 'clientLogo', 'addressLine1', 'postalCode', 'phoneNumber', 'emailAddress', 'taxNumber']


class ClientSelectForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client']

class CreditNoteForm(forms.ModelForm):
    class Meta:
        model = CreditNote
        fields = ['reason_code','reason']

class ProdMetaForm(forms.ModelForm):
    class Meta:
        model = ProductMeta
        fields = ['stock','price']