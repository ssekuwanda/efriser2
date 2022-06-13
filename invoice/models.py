import imp
from django.db import models
from django.forms import JSONField
from django.template.defaultfilters import slugify
from django.utils import timezone
from uuid import uuid4
from django.contrib.auth.models import User
from random import randint
from jsonfield import JSONField

randoms = randint(120,1000)

class Company(models.Model):

    companyTypes = [
        ('Services', 'Services'), 
        ('Products', 'Products'),
        ]
    # Basic Fields
    owner = models.OneToOneField(
        User, related_name="company1", blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField("Company Name",max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=1000, null=True, blank=True)

    companyLogo = models.ImageField(default='default_logo.jpg', upload_to='company_logos', blank=True, null=True)
    company_type = models.CharField(max_length=100, choices=companyTypes, blank=True, null=True)

    #Tax fields
    tin = models.BigIntegerField()
    device_number = models.CharField(max_length=100, null=True, blank=True)

    #Utility fields
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.device_number)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.slug is None:
            rad = randoms
            self.slug = slugify('{} {}'.format(
                self.name, rad))

        self.slug = slugify('{} {}'.format(self.name, self.id))
        self.last_updated = timezone.localtime(timezone.now())

        super(Company, self).save(*args, **kwargs)

class Client(models.Model):

    #Basic Fields. wwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, null=True, blank=True)
    business_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=10000, null=True, blank=True)
    email_address = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)
    nin_brn = models.CharField("nin/Brn", max_length=100, null=True, blank=True)
    tin = models.BigIntegerField(null=True, blank=True, unique=True)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return '{}'.format(self.name)


    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.name, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.name, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Client, self).save(*args, **kwargs)



class Invoice(models.Model):
    CURRENCY = [
        ('UGX', 'UGX'),
        ('USD', 'USD'),
        ('GBP', 'GBP'),
    ]
    # Basic Fields
    number = models.CharField(null=True, blank=True, max_length=100)
    finalized = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True) 
    currency = models.CharField("CURRENCY",choices= CURRENCY,null=True, blank=True, max_length=100)
    tax = models.CharField(null=True, blank=True, max_length=100)
    payment_method = models.CharField(null=True, blank=True, max_length=100)


    # EFRIS fields
    fdn = models.CharField(null=True, blank=True, max_length=100)
    number = models.CharField(null=True, blank=True, max_length=100)
    # anti_fake_code = models.CharField(null=True, blank=True, max_length=10000)
    # qrcode = models.CharField(null=True, blank=True, max_length=10000)
    json_response = JSONField(blank=True)

    #RELATED fields
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.SET_NULL)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return '{} {}'.format(self.number, self.uniqueId)


    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.number, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.number, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Invoice, self).save(*args, **kwargs)

class CreditNote(models.Model):
    REASONS = [
        ('101', 'Return of products due to expiry or damage, etc.'),
        ('102', 'Cancellation of the purchase'),
        ('103', 'Invoice amount wrongly stated due to miscalculation of price, tax or discounts, etc.'),
        ('104', 'Partial or complete waive off of the service sale after the invoice is generated and sent to the customer'),
        ('105', 'Others (Please specify'),
    ]
    invoice = models.ForeignKey(Invoice, blank=True, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    reason_code = models.CharField(max_length=10000, choices=REASONS, null=False, blank=False)
    reason = models.TextField(null=True, blank=True)

    def __str__(self): 
        return str(self.invoice)


class Unit_Measurement(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=3, null=True, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    CURRENCY = [
        ('UGX', 'UGX'),
        ('USD', 'USD'),
        ('GBP', 'GBP'),
    ]

    YES_OR_NO =[
        ('Yes','Yes'),
        ('No','No'),
    ]

    TAX_RATES = [('18%', '18%'),('0%','0%'),]

    # EFRIS Calibration
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(null=False, blank=False, max_length=100)
    code = models.CharField(null=False, blank=False, max_length=4)
    unit_measure = models.ForeignKey(
        Unit_Measurement, on_delete=models.SET_NULL, null=True, blank=True)
    unit_price = models.FloatField(null=False, blank=False)
    currency = models.CharField(choices=CURRENCY, max_length=3)
    tax_rate = models.CharField(choices=TAX_RATES, null=False, blank=False, max_length=3, default='18%')
    commodity_id = models.CharField(null=False, blank=False, max_length=18)
    has_excise_duty = models.CharField(
        choices=YES_OR_NO, max_length=3, null=True, blank=True)
    description = models.CharField(null=False, blank=False, max_length=1024)
    stock_warning = models.CharField(null=False, blank=False, max_length=24)
    # piece_measure_unit = models.CharField(null=True, blank=True, max_length=3)

    #Related Fields
    # invoice = models.ForeignKey(Invoice, blank=True, null=True, on_delete=models.CASCADE)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return '{}'.format(self.name)


    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.name, self.uniqueId))
        self.slug = slugify('{} {}'.format(self.name, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        self.unit_price = round(self.unit_price, 2)
        super(Product, self).save(*args, **kwargs)

class InvoiceProducts(models.Model):
    # Basic fields
    invoice = models.ForeignKey(
        Invoice, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    notes = models.TextField(null=True, blank=True)
    quantity = models.FloatField()
    price = models.FloatField("Unit Price")

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return '{}--{}'.format(str(self.invoice), self.id)

    def total(self):
        return float(self.price*self.quantity)
    
    def prod_tax(self):
        tax = 1
        if self.product.tax_rate == "18%":
            tax = 0.18
        else:
            tax = 1
        return float(self.total()*tax)   

    def tax(self):
        tax = 1
        if self.product.tax_rate == "18%":
            tax = 0.18
        else:
            tax = 1
        return float((self.total()*tax)/1.18)

    def net_amount(self):
        return float((self.total())-self.tax())
    
    # def net_price(self):
    #     return self.price*self.quantity

    # def total(self):
    #     tax = 1
    #     if self.product.tax_rate == "18%":
    #         tax = 0.18
    #     else:
    #         tax = 1
    #     return self.price*self.quantity

    # def tax_total(self):
    #     tax = 1
    #     if self.product.tax_rate == "18%":
    #         tax =0.18
    #     else:
    #         tax =1
    #     return int(self.total())*tax

    # def unit_tax(self):
    #     tax = 1
    #     if self.product.tax_rate == "18%":
    #         tax =0.18
    #     else:
    #         tax =1
    #     return (((self.price*self.quantity)*tax))/1.18
    
    # def net_product_px(self):
    #     tax = 1
    #     if self.product.tax_rate == "18%":
    #         tax =0.18
    #     else:
    #         tax =1
    #     return ((self.price*self.quantity)-int(self.unit_tax()))  



    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.product, self.uniqueId))
        self.slug = slugify('{} {}'.format(self.invoice, self.uniqueId))
        self.price = round(self.price, 2)
        super(InvoiceProducts, self).save(*args, **kwargs)


class Settings(models.Model):
    #Basic Fields
    clientName = models.CharField(null=True, blank=True, max_length=200)
    clientLogo = models.ImageField(default='default_logo.jpg', upload_to='company_logos')
    addressLine1 = models.CharField(null=True, blank=True, max_length=200)
    postalCode = models.CharField(null=True, blank=True, max_length=10)
    phoneNumber = models.CharField(null=True, blank=True, max_length=100)
    emailAddress = models.CharField(null=True, blank=True, max_length=100)
    taxNumber = models.CharField(null=True, blank=True, max_length=100)


    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return '{} {}'.format(self.clientName, self.uniqueId)


    def get_absolute_url(self):
        return reverse('settings-detail', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.clientName, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.clientName, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Settings, self).save(*args, **kwargs)
