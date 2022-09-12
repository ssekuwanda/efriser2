from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import *
import json

#Form Layout from Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

BUYER_TYPE = [
    ('0','Business'),
    ('3','Government'),
    ('1','Consumer'),
    ('2','Foreigner'),
    ]

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
        fields = ['name', 'companyLogo','tin','device_number','email','telephone_number','location','url','nature','wht_exempt','vat_wht']

class ClientForm(forms.ModelForm):
    company_type= forms.CharField(widget=forms.RadioSelect(choices=BUYER_TYPE))
    class Meta:
        model = Client
        fields = ['name', 'business_name','address', 'email_address', 'contact_number', 'company_type','tin']
    
class InvoiceProductForm(forms.ModelForm):
    class Meta:
        model = InvoiceProducts
        fields = ['product', 'tax_type', 'price']

    def __init__(self, ps, *args, **kwargs):
        super(InvoiceProductForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(id__in=ps)

class IndInvProductForm(forms.ModelForm):
    class Meta:
        model = InvoiceProducts
        fields = ['product', 'tax_type', 'price']

    def __init__(self, ps, *args, **kwargs):
        super(InvoiceProductForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(id__in=ps)

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
        model = Client
        fields = ['name','tin']

class CreditNoteForm(forms.ModelForm):
    class Meta:
        model = CreditNote
        fields = ['reason_code','reason']

class ProdMetaForm(forms.ModelForm):
    class Meta:
        model = ProductMeta
        fields = ['stock','price']


class CnCancelForm(forms.ModelForm):
    REASONS = [('101','Buyer refused to accept the invoice due to incorrect invoice/receipt'), ('102','Not delivered due to incorrect invoice/receipt'),('103','Other reasons')]

    reason= forms.CharField(widget=forms.RadioSelect(choices=REASONS))
    class Meta:
        model = CnCancel
        fields = ['reason','details',]

class BarCodeForm(forms.ModelForm):
    class Meta:
        model = BarCode
        fields = ['name']

class ProductsFormSet(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code',]