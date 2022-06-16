from urllib import response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from invoice.utils.api import *
from invoice.utils.invoice_cleaner import *
from .forms import *
from .models import *
from .functions import *
from .utils.goods_dict import *

from django.contrib.auth.models import User, auth
from random import randint
from uuid import uuid4

from django.http import HttpResponse
from django.template.loader import get_template
import os
from django.db.models import Sum


#Anonymous required
def anonymous_required(function=None, redirect_url=None):

   if not redirect_url:
       redirect_url = 'dashboard'

   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous,
       login_url=redirect_url
   )

   if function:
       return actual_decorator(function)
   return actual_decorator


def index(request):
    context = {}
    return render(request, 'invoice/index.html', context)


@anonymous_required
def login(request):
    context = {}
    if request.method == 'GET':
        form = UserLoginForm()
        context['form'] = form
        return render(request, 'invoice/login.html', context)

    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)

            return redirect('dashboard')
        else:
            context['form'] = form
            messages.error(request, 'Invalid Credentials')
            return redirect('login')


    return render(request, 'invoice/login.html', context)


@login_required
def dashboard(request):
    clients = Client.objects.all().count()
    invoices = Invoice.objects.all().count()
    # paidInvoices = Invoice.objects.filter(status='PAID').count()
    context = {}

    if request.method == 'GET':
        form = CompanyForm()
        context['form'] = form
        return render(request, 'invoice/dashboard.html', context)


    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        context['form'] = form
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()

            messages.success(request, 'New Company Added')
            return redirect('dashboard')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('dashboard')

    context['clients'] = clients
    context['invoices'] = invoices
    return render(request, 'invoice/dashboard.html', context)


@login_required
def invoices(request, slug):
    context = {}
    invoices = Invoice.objects.all()
    # cleint = Client.objects.get(slug=slug)
    context['invoices'] = invoices
    context['cleint'] = "cleint"

    return render(request, 'invoice/invoices.html', context)


@login_required
def products(request):
    context = {}
    products = Product.objects.all()
    context['products'] = products

    issuer = request.user.company1

    if request.method == 'GET':
        form = ProductForm()
        context['form'] = form
        return render(request, 'invoice/products.html', context)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form = form.save(commit=False)
            
            form.company = issuer
            message = {"havePieceUnit": "102"}

            message['goodsName'] = form.name
            message['goodsCode'] = form.code
            message['measureUnit'] = str(form.unit_measure.code)
            message['unitPrice'] = form.unit_price
            message['currency'] = "101" if form.currency=="USD" else "102"
            message['commodityCategoryId'] = form.commodity_id
            message['haveExciseTax'] = "101" if form.has_excise_duty=="Yes" else "102"
            message['description'] = form.description
            message['stockPrewarning'] = form.stock_warning
            
            response = goodsUpload(issuer.tin, issuer.device_number, message)

            if response['returnStateInfo']['returnMessage'] != 'SUCCESS':
                messages.error(request, f"{response['returnStateInfo']['returnMessage']} Please check that all details are correct")
                return redirect('products')
            else:
                form.save()
                messages.success(request,response['returnStateInfo']['returnMessage'])
                return redirect('products')     
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('products')
    return render(request, 'invoice/products.html', context)


@login_required
def productsMaintance(request, slug):
    prod = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        form = ProdMetaForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = prod
            form.save()
            return redirect('products')
    else:
        form = ProdMetaForm()
    context = {'form': form,'product':prod}
    return render(request, 'product/product_update.html', context)   


@login_required
def clients(request):
    owned = request.user.company1
    context = {}
    clients = Client.objects.filter(company=owned)
    context['clients'] = clients

    if request.method == 'GET':
        form = ClientForm()
        context['form'] = form
        return render(request, 'invoice/clients.html', context)

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)

        if form.is_valid():
            form_tin = form.cleaned_data['tin']
            form = form.save(commit=False)
            response = None
            if form.tin:
                response = getClientDetails(owned.tin, form_tin, owned.device_number)
                print(response)

            if response:
                if 'address' in json.loads(response)['taxpayer']:
                    address = json.loads(response)['taxpayer']['address']
                else:
                    address = ""
                if 'contactEmail' in json.loads(response)['taxpayer']:
                    email = json.loads(response)['taxpayer']['contactEmail']
                else:
                    email = ""
                if 'contactNumber' in json.loads(response)['taxpayer']:
                    number = json.loads(response)['taxpayer']['contactNumber']
                else:
                    number = ""
                if 'legalName' in json.loads(response)['taxpayer']:
                    legal_name = json.loads(response)['taxpayer']['legalName']
                else:
                    legal_name = ""
                if 'ninBrn' in json.loads(response)['taxpayer']:
                    nin = json.loads(response)['taxpayer']['ninBrn']
                else:
                    nin =""
                form.business_name = legal_name
                form.email_address = email
                form.contact_number = number
                form.nin_brn = nin
                form.address = address
            form.company = owned
            form.save()
            messages.success(request, 'New Client Added')
            return redirect('clients')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('clients')
    return render(request, 'invoice/clients.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

###--------------------------- Create Invoice Views Start here --------------------------------------------- ###

@login_required
def createInvoice(request, slug):
    number = 'INV-'+str(uuid4()).split('-')[1]
    client = Client.objects.get(slug=slug)
    newInvoice = Invoice.objects.create(number=number, client=client)
    newInvoice.save()

    inv = Invoice.objects.get(number=number)
    return redirect('create-build-invoice', slug=inv.slug)


@login_required
def createBuildInvoice(request, slug):
    try:
        invoice = Invoice.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')
    products = InvoiceProducts.objects.filter(invoice=invoice)

    context = {}
    goods_context = []
    tax_context = []
    
    net_amount = 0
    tax_amount = 0
    gross_amount = 0
    order_number = 0
    context.update(inv_context(invoice.json_response))

    for prod in products:
        good = goods_details(prod,order_number)
        tax = tax_details(prod)
        order_number+=1
        
        net_amount += prod.net_amount()
        tax_amount += prod.tax()
        gross_amount += prod.total()

        # Add populated good to goods_details list
        goods_context.append(good)
        tax_context.append(tax)
    
    context['invoice'] = invoice
    context['products'] = products
    context['net'] = net_amount
    context['tax'] = tax_amount
    context['gross'] = gross_amount
    context['operator'] = request.user.username
    context['buyerTin'] = invoice.client.tin
    context['itemCount'] = order_number
    context['remarks'] = ""
    
    goods_summary = summary(context)


    goodsDetails = goods_context
    taxDetails = tax_context
    summary_json = goods_summary

    if request.method == 'GET':
        prod_form = InvoiceProductForm()
        inv_form = InvoiceForm(instance=invoice)
        context['prod_form'] = prod_form
        context['inv_form'] = inv_form
        return render(request, 'invoice/create-invoice.html', context)

    if request.method == 'POST':
        prod_form = InvoiceProductForm(request.POST)
        inv_form = InvoiceForm(request.POST, instance=invoice)
        client_form = ClientSelectForm(request.POST, instance=invoice)

        if prod_form.is_valid():
            obj = prod_form.save(commit=False)
            obj.invoice = invoice
            obj.save()
            messages.success(request, "Invoice product added succesfully")
            return redirect('create-build-invoice', slug=slug)
        elif inv_form.is_valid and request.POST:
            invoice_update = inv_form.save(commit=False)
            
            issuer = request.user.company1
            context['currency'] = inv_form['currency'].value()
            context['remarks'] = inv_form['remarks'].value()

            inv = uploadInvoice(issuer, context, goodsDetails, taxDetails,summary_json)
            invoice_update.json_response = inv["content"]

            if inv["returnMessage"] == "SUCCESS":
                invoice_update.finalized = True
                invoice_update.save()
                messages.success(request, "Invoice Issued succesfully")
            else:
                messages.warning(request, inv["returnMessage"])
            
            return redirect('create-build-invoice', slug=slug)
        # to be deleted 
        elif client_form.is_valid() and 'client' in request.POST:

            client_form.save()
            messages.success(request, "Client added to invoice succesfully")
            return redirect('create-build-invoice', slug=slug)
        else:
            context['prod_form'] = prod_form
            context['inv_form'] = inv_form
            context['client_form'] = client_form
            messages.error(request,"Problem processing your request")
            return render(request, 'invoice/create-invoice.html', context)
    return render(request, 'invoice/create-invoice.html', context)


def client_home(request, slug):
    client = Client.objects.get(slug=slug)
    invoices = Invoice.objects.filter(client=client)
    context ={}
    context['client'] = client
    context['invoices'] = invoices
    return render(request, 'invoice/client-home.html', context)


def createCreditNote(request, slug):
    invoice = Invoice.objects.get(slug=slug)
    if request.method == 'POST':
        form = CreditNoteForm(request.POST or None)
        if request.method =="POST" and form.is_valid():
            creditnote_load = json.dumps(credit_note(invoice, form))
            encodedCreditNote = encode(creditnote_load).decode()
            received_message = creditNoteUpload(encodedCreditNote,request)

            if received_message['returnStateInfo']["returnMessage"] == "SUCCESS":
                form = form.save(commit=False)
                form.json_response = received_message
                form.reference = received_message['data']['content']
                form.invoice = invoice
                form.save()
                messages.success(request, "Credit note Issued Succesfully")
                return redirect('create-build-invoice', slug=slug)
            else:
                messages.warning(request, received_message['returnStateInfo']["returnMessage"])
    else:
        form = CreditNoteForm()
    return render(request, 'invoice/create-creditnote.html', {'form':form})

def creditNoteHome(request):
    credits = CreditNote.objects.all()

    context = {'credits':credits}
    return render(request, 'invoice/all_creditnotes.html', context)

@login_required
def pdfInvoice(request, slug):
    company = request.user.company1
    client = Client.objects.filter(company=company)
    invoice = Invoice.objects.get(slug= slug)
    
    context = {}

    context['company'] = company
    context['client'] = client

    html_string = render_to_string('documents/invoicepdf.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(presentational_hints=True)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=test.pdf'

    return response

@login_required
def prod_delete(request, slug):
    instance = get_object_or_404(InvoiceProducts, slug=slug)
    instance.delete()
    messages.success(
        request, f"{instance.product.name} was successfully deleted")
    return redirect('create-build-invoice', slug=instance.invoice.slug)