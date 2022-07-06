from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from weasyprint import HTML
from invoice.utils.api import *
from invoice.utils.invoice_cleaner import *
from .forms import *
from .models import *
from .functions import *
from .utils.goods_dict import *
from django.contrib.auth.models import auth
from uuid import uuid4
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Sum
from django.db.models import Q

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
        return render(request, 'accounts/login.html', context)

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


    return render(request, 'accounts/login.html', context)

@login_required
def dashboard(request):
    clients = Client.objects.all().count()
    invoices = Invoice.objects.all().count()
    credits = CreditNote.objects.all().count()

    context = {}
    context['clients'] = clients
    context['invoices'] = invoices
    context['credits'] = credits

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


    return render(request, 'invoice/dashboard.html', context)


@login_required
def invoices(request):
    context = {}
    company = request.user.company1
    invoices = Invoice.objects.filter(company=company)

    context['invoices'] = invoices
    context['cleaned_inv']=[]
    for inv in invoices:
        if inv.json_response:
            context['cleaned_inv'].append(inv_context(inv.json_response))
            context['cleaned_inv'].append({'slug':inv.slug})

    context['cleint'] = "cleint"
    return render(request, 'invoice/all_invoices.html', context)

@login_required
def online_invoices(request):
    context = {}
    company = request.user.company1
    invoices = Invoice.objects.filter(company=company)
    for inv in invoices:
        cleaned_data = inv_context(inv.json_response)
    context['invoices'] = invoices
    context['cleint'] = "cleint"
    return render(request, 'invoice/invoices.html', context)

@login_required
def products(request):
    issuer = request.user.company1
    context = {}
    products = Product.objects.filter(company=issuer)
    context['products'] = products

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
    comp = request.user.company1

    if request.method == "POST":
        form = ProdMetaForm(request.POST)
        if form.is_valid():
            goods_update_details = {}
            goods_update_details["quantity"] = form["stock"].value()
            goods_update_details["unitPrice"] = form["price"].value()
            goods_update_details["commodityGoodsId"] = prod.commodity_id
            goods_update_details["code"] = prod.code

            stock_dict = stockGoods(goods_update_details)
            stock_json = json.dumps(stock_dict)
            encrpt = encode(stock_json).decode("utf-8")

            payload_data = payload_info(comp.tin, comp.device_number, "T131", encrpt)
            output = post_message(payload_data)

            form = form.save(commit=False)
            form.company = comp
            form.product = prod
            prod.stock_warning = int(prod.stock_warning)+int(goods_update_details['quantity'])
            
            if output =="[]":
                prod.save()
                form.save()
                messages.success(request, "GOODS RESTOCKED SUCCESSFULLY")
                return redirect('products')
            else:
                messages.error(request,"Please check that all details are correct/ Services can't be restocked")
                return redirect('products')
            return redirect('products')  
    else:
        form = ProdMetaForm()
    context = {'form': form,'product':prod}
    return render(request, 'product/product_update.html', context)   


@login_required
def clients(request):
    owned = request.user.company1
    queryset = Client.objects.filter(name__icontains='Boston')
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
            # response = None
            if form.tin:
                response = getClientDetails(owned.tin, form_tin, owned.device_number)

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
    today = datetime.now()
    company = request.user.company1
     
    for inv in Invoice.objects.filter(company=company):
        if inv.inv_prod.all == None:
            inv.delete()

    list_num = []
    for numb in Invoice.objects.filter(company=company, last_updated__year=today.year):
        list_num.append(numb.number)

    max_numb = max(list_num)
    new_numb = int(max_numb)+1

    client = Client.objects.get(slug=slug)
    newInvoice = Invoice.objects.create(number=new_numb, client=client, company=company)
    newInvoice.save()

    inv = Invoice.objects.get(slug=newInvoice.slug)
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

    if invoice.json_response != "":
        context.update(inv_context(invoice.json_response))
    
    for prod in products:
        good = goods_details(prod, order_number, invoice)
        tax = tax_details(prod, invoice)
        order_number+=1
        
        net_amount += prod.net_amount()
        tax_amount += prod.tax()
        gross_amount += prod.total()
        goods_context.append(good)
        tax_context.append(tax)
    
    context['invoice'] = invoice
    context['products'] = products
    context['net'] = net_amount
    context['tax'] = tax_amount
    context['gross'] = gross_amount
    context['operator'] = request.user.username
    if invoice.client.tin:
        context['buyerTin'] = invoice.client.tin
    else:
        context['buyerTin'] = ""
    context['itemCount'] = order_number
    context['remarks'] = ""
    context['payWay'] = invoice.payment_method,
    context['buyerLegalName'] = invoice.client.name,
    context['buyerEmail'] = invoice.client.email_address,

    context['buyerAddress'] = invoice.client.address
    if invoice.client.company_type != '3':
        context['buyerType'] = invoice.client.company_type
    else:
        context['buyerType'] = str(0)

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
            if obj.price == '':
                obj.price = 1
            obj.save()
            messages.success(request, "Product added succesfully")
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
    company = request.user.company1

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

                reference = received_message['data']['content']
                decrpt = decode(reference).decode()
                form.json_response = decrpt
                form.reference = json.loads(decrpt)['referenceNo']
                form.invoice = invoice
                form.company = company
            
                form.save()
                messages.success(request, "Credit note Issued Succesfully")
                return redirect('create-build-invoice', slug=slug)
            else:
                messages.warning(request, received_message['returnStateInfo']["returnMessage"])
    else:
        form = CreditNoteForm()
    return render(request, 'invoice/create-creditnote.html', {'form':form})

def creditNoteHome(request):
    company = request.user.company1
    credits = CreditNote.objects.all()

    context = {'credits':credits}
    return render(request, 'invoice/all_creditnotes.html', context)

@login_required
def pdfInvoice(request, slug):
    company = request.user.company1
    client = Client.objects.filter(company=company)

    context = {}
    invoice = Invoice.objects.get(slug= slug)
    context['invDetails'] = invoice
    invoice_pdts = InvoiceProducts.objects.filter(invoice=invoice)

    context['company'] = company
    context['client'] = client
    context['invoice'] = []
    context['taxes'] = []
    context['clean_data'] = inv_context(invoice.json_response)
    context['products'] = invoice_pdts
    
    tax_total = 0

    for prod in invoice_pdts:      
        tax = tax_details(prod, invoice)
        tax_total +=float(tax['taxAmount'])

    context['tax'] = tax_total
    fdn = inv_context(invoice.json_response)['fdn']

    for good in inv_context(invoice.json_response)['items']:
        context['invoice'].append(good)

    for tx in inv_context(invoice.json_response)['taxDetails']:
        context['taxes'].append(tx)
    # +context.update(inv_context(invoice.json_response))
 
    bank = request.user.company1.bank_details.filter(currency=invoice.currency)
    context['bank'] = bank

    html_string = render_to_string('documents/invoicepdf.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(presentational_hints=True)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename={fdn}.pdf'
    return response

@login_required
def prod_delete(request, slug):
    instance = get_object_or_404(InvoiceProducts, slug=slug)
    instance.delete()
    messages.success(
        request, f"{instance.product.name} was successfully deleted")
    return redirect('create-build-invoice', slug=instance.invoice.slug)


def refresh_cn_status(request, id):
    cn = CreditNote.objects.get(id=id)
    comp = request.user.company1
    encrpted = encode(json.dumps({"id": cn.reference})).decode()
    resp = refreshCnStatus(comp.tin, comp.device_number, encrpted)
    
    return redirect('create-build-invoice', slug=cn.invoice.slug)


def cn_list(request):
    context = {}
    context['details']=[]
    if request.method == "POST":
        start_date = str(request.POST['start_date'])
        end_date = str(request.POST['end_date'])
        query = str(request.POST['query'])

        cn_dict = cnQueryList(start_date, end_date, query)
        cn_json = json.dumps(cn_dict)
        encrpt = encode(cn_json).decode("utf-8")
        uploadList = cnListUpload(encrpt, request)
        json_dump = json.loads(uploadList)

        for rec in json_dump['records']:
            context['details'].append(rec)
    return render(request, 'credit_note/cn_list.html', context)
    

def inv_list(request):
    context = {}
    context['details']=[]
    if request.method == "POST":
        start_date = str(request.POST['start_date'])
        end_date = str(request.POST['end_date'])

        return_msg = invListUpload(start_date, end_date, request)
        for rec in return_msg['records']:
            context['details'].append(rec)
    return render(request, 'invoice/inv_list.html', context)

def inv_details(request):
    context = {}
    context['details']=[]
    if request.method == "POST":
        fdn = str(request.POST['fdn'])

        return_msg = msg_middleware(request, fdn)
        if return_msg:
            context['antifake']=return_msg['basicInformation']['antifakeCode']
            context['date']=return_msg['basicInformation']['issuedDate']
            context['fdn']=return_msg['basicInformation']['invoiceNo']
            context['currency']=return_msg['basicInformation']['currency']

            context['buyer']=return_msg['buyerDetails']['buyerLegalName']
            context['tin']=return_msg['buyerDetails']['buyerTin']

            context['gross']=return_msg['summary']['grossAmount']
            context['net']=return_msg['summary']['netAmount']
            context['tax']=return_msg['summary']['taxAmount']
            messages.success(request, "Valid Invoice")
        else:
            messages.warning(request, "Invalid Invoice")
    return render(request, 'invoice/inv_details.html', context)


def cancel_cn(request, id):
    cn = CreditNote.objects.get(id = id)
    invoice = cn.invoice
    msg = {}
    msg['inv_id'] =  inv_context(cn.invoice.json_response)['invoiceId']
    msg['cn_ref'] = cn.reference

    # cn_dict = cancel_cn_helper()
    
    form = CnCancelForm()
    msg['form']= form
    if request.method == 'POST':
        form = CnCancelForm(request.POST)

        if form.is_valid():
            msg['reason'] = form.cleaned_data['reason']
            form = form.save(commit=False)
            form.cn = cn
            form.save()
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('create-build-invoice','invoice.slug')
    return render(request, 'credit_note/cancel_cn.html',msg)
    
def approve_cn(self):
    pass