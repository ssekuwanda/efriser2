from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from weasyprint import HTML
from invoice.request_msg import goods_inquiry_req
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
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def dashboard(request):
    context = {}
    if hasattr(request.user,'company1'):
        clients = Client.objects.filter(company=request.user.company1).count()
        invoices = Invoice.objects.filter(company=request.user.company1).count()
        credits = CreditNote.objects.filter(company=request.user.company1).count()

        invoice2 = Invoice.objects.filter(company=request.user.company1,json_response="")
        for inv in invoice2:
            inv.delete()

    
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
    invoice2 = Invoice.objects.filter(company=company, json_response="")
    for inv in invoice2:
        inv.delete()

    context['invoices'] = invoices
    context['cleaned_inv'] = []
    for inv in invoices:
        if inv.json_response:
            context['cleaned_inv'].append(inv_cleaner(inv.json_response, inv.slug))
            # context['cleaned_inv'].append({'slug':inv.slug})
    context['client'] = "client"
    return render(request, 'invoice/all_invoices.html', context)

@login_required
def online_invoices(request):
    context = {}
    company = request.user.company1
    invoices = Invoice.objects.filter(company=company)

    invoice2 = Invoice.objects.filter(company=company,json_response="")
    for inv in invoice2:
        inv.delete()

    for inv in invoices:
        cleaned_data = inv_context(inv.json_response)
    context['invoices'] = invoices
    context['cleint'] = "cleint"
    return render(request, 'invoice/invoices.html', context)

@login_required
def products(request):
    issuer = request.user.company1
    context = {}    

    query = request.GET.get('q')

    if query:
        paginator = Paginator(Product.objects.filter(company=issuer).filter(Q(name__icontains = query)), 10)
    else:
        paginator = Paginator(Product.objects.filter(company=issuer), 10)

    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

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
            
            response = goodsUpload(request, message)

            if response['returnStateInfo']['returnMessage'] != 'SUCCESS':
                messages.error(request, f"{response['returnStateInfo']['returnMessage']} Please check that all details are correct & that the code is unique")
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

            payload_data = payload_info(request, "T131", encrpt)
            output = post_message(request, payload_data)

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
    else:
        form = ProdMetaForm()
    context = {'form': form,'product':prod}
    return render(request, 'product/product_update.html', context)   

@login_required
def goods_inquiry(request, slug):
    prod = get_object_or_404(Product, slug=slug)
    req = goods_inquiry_req(prod)
    result = json.loads(goodsInquire(request, req))
    return render(request, 'product/product_inquiry.html', result) 

@login_required
def dictonary(request):
    if request.method == 'POST':
        query = request.POST.get('q', False)
        pickled = json.loads(systemDict(request))
        return render(request, 'product/dictionary.html', {'context':pickled})
    return render(request, 'product/dictionary.html')

@login_required
def clients(request):
    owned = request.user.company1
    context = {}
    query = request.GET.get('q')

    if query:
        clients = Client.objects.filter(company=owned).filter(Q(name__icontains=query))
    else:
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
                response = getClientDetails(request, form_tin)
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
def createInvoice(request, slug):
    company = request.user.company1
     
    for inv in Invoice.objects.filter(company=company):
        if inv.inv_prod.all == None:
            inv.delete()

    list_num = [0]
    today = datetime.now()
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
    ps = []
    for product in Product.objects.filter(company=request.user.company1):
        ps.append(product.id)
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
    tax_amount_summary = 0
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

        # check if the customer is VAT exempt if yes tax = 0 in the summary section
        if prod.tax_type.code == "04":
            tax_amount_summary = 0
        else:
            tax_amount_summary += prod.tax()
    
    context['invoice'] = invoice
    context['products'] = products
    context['net'] = net_amount
    context['tax'] = tax_amount
    context['tax_summary'] = tax_amount_summary
    context['gross'] = gross_amount
    context['operator'] = request.user.username
    if invoice.client.tin:
        context['buyerTin'] = invoice.client.tin
    else:
        context['buyerTin'] = ""
    context['itemCount'] = order_number
    context['payWay'] = invoice.payment_method,
    context['buyerLegalName'] = invoice.client.name,
    context['buyerEmail'] = invoice.client.email_address,

    context['buyerAddress'] = invoice.client.address
    if invoice.client.company_type == "2":
        context['industryCode'] = "102",
    else:
        context['industryCode'] = "101",
  
    if invoice.client.company_type != '3':
        context['buyerType'] = invoice.client.company_type
    else:
        context['buyerType'] = str(0)

    goodsDetails = goods_context
    taxDetails = tax_context

    if request.method == 'GET':
        prod_form = InvoiceProductForm(ps)
        inv_form = InvoiceForm(instance=invoice)
        context['prod_form'] = prod_form
        context['inv_form'] = inv_form
        return render(request, 'invoice/create-invoice.html', context)

    if request.method == 'POST':
        prod_form = InvoiceProductForm(ps,request.POST)
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
            
            context['currency'] = inv_form['currency'].value()
            context['remarks'] = inv_form['remarks'].value()
            context['payment_method'] = inv_form['payment_method'].value()
            payment_details = pay_way(context)
            goods_summary = summary(context)

            inv = uploadInvoice(request, context, goodsDetails, taxDetails, goods_summary, payment_details)  
            invoice_update.json_response = inv["content"]

            if inv["returnMessage"] == "SUCCESS":
                invoice_update.finalized = True
                invoice_update.save()
                for prod in products:
                    init_product = Product.objects.get(id=prod.product.id)
                    prod_total = int(init_product.stock_warning)
                    reduction = prod_total - int(prod.quantity)
                    init_product.stock_warning = str(reduction)
                    init_product.save()
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

@login_required
def client_home(request, slug):
    client = Client.objects.get(slug=slug)
    invoices = Invoice.objects.filter(client=client) 
    context ={}
    context['client'] = client
    context['invoices'] = invoices
    return render(request, 'invoice/client-home.html', context)

@login_required
def createCreditNote(request, slug):
    list_num = [0]
    for numb in CreditNote.objects.filter(company=request.user.company1, last_updated__year=datetime.now().year):
        list_num.append(numb.number)

    max_numb = max(list_num)
    new_numb = int(max_numb)+1
    cn_number = str(request.user.company1.short_name+'/'+str(new_numb)+'/'+str(datetime.now().year))+'-CN'

    invoice = Invoice.objects.get(slug=slug)
    if request.method == 'POST':
        form = CreditNoteForm(request.POST or None)
        if request.method =="POST" and form.is_valid():
            creditnote_load = json.dumps(credit_note(invoice, form, cn_number))
            encodedCreditNote = encode(creditnote_load).decode()
            received_message = creditNoteUpload(encodedCreditNote,request)

            if received_message['returnStateInfo']["returnMessage"] == "SUCCESS":
                form = form.save(commit=False)
                form.json_response = received_message

                reference = received_message['data']['content']
                decrpt = decode(reference).decode()
                form.json_response = decrpt
                form.number = new_numb
                form.reference = json.loads(decrpt)['referenceNo']
                form.invoice = invoice
                form.company = request.user.company1
            
                form.save()
                messages.success(request, "Credit note Issued Succesfully")
                return redirect('create-build-invoice', slug=slug)
            else:
                messages.warning(request, received_message['returnStateInfo']["returnMessage"])
    else:
        form = CreditNoteForm()
    return render(request, 'invoice/create-creditnote.html', {'form':form})

@login_required
def creditNoteHome(request):
    company = request.user.company1
    credits = CreditNote.objects.filter(company=company)#.order_by('-status')
    context = {'credits':credits}
    return render(request, 'credit_note/all_creditnotes.html', context)

@login_required
def pdfInvoice(request, slug):
    company = request.user.company1
    client = Client.objects.filter(company=company)

    context = {}
    if Invoice.objects.get(slug= slug) != None:
        invoice = Invoice.objects.get(slug= slug)
    else:
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
def creditnote_pdf(request, fdn):
    company = request.user.company1
    client = Client.objects.filter(company=company)

    context = {}
    cnote = CreditNote.objects.get(fdn=fdn)
    
    anti_fake = ""
    if cnote.anti_fake == None:
        vc = msg_middleware(request, fdn)
        anti_fake = vc['basicInformation']['antifakeCode']
        CreditNote.objects.filter(fdn=fdn).update(anti_fake=anti_fake)

    note = CreditNote.objects.get(fdn=fdn)
    invoice = note.invoice
    context['cn'] = note
    context['invDetails'] = invoice
    invoice_pdts = InvoiceProducts.objects.filter(invoice=invoice)

    context['company'] = company
    context['anti_fake'] = anti_fake

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
    context['tax'] = tax_total
    
    fdn = inv_context(invoice.json_response)['fdn']

    for good in inv_context(invoice.json_response)['items']:
        context['invoice'].append(good)

    for tx in inv_context(invoice.json_response)['taxDetails']:
        context['taxes'].append(tx)

    # context.update(inv_context(invoice.json_response))
 
    bank = request.user.company1.bank_details.filter(currency=invoice.currency)
    context['bank'] = bank

    html_string = render_to_string('documents/creditnotepdf.html', context)
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

@login_required
def refresh_cn_status(request, id):
    cn = CreditNote.objects.get(id=id)
    encrpted = encode(json.dumps({"id": cn.reference})).decode()
    resp = refreshCnStatus(request, encrpted)    
    return redirect('create-build-invoice', slug=cn.invoice.slug)

@login_required
def cn_list(request):
    all_cns = CreditNote.objects.filter(company=request.user.company1, status=False)
    context = {}
    context['details']=[]
    if request.method == "POST":
        start_date = str(request.POST['start_date'])
        end_date = str(request.POST['end_date'])
        query = str(request.POST['query'])

        cn_dict = cnQueryList(start_date, end_date, query)
        cn_json = json.dumps(cn_dict)
        encoded_string = encode(cn_json)
        encrpt = encoded_string.decode('utf-8')
        uploadList = cnListUpload(encrpt, request)
        json_dump = json.loads(uploadList)
        for cns in all_cns:
            for js in json_dump['records']:
                if js['referenceNo']==cns.reference:
                    try:
                        cns.fdn = js['invoiceNo']
                        cns.status = True
                    except KeyError:
                        pass
                    if js['approveStatus'] == "101":
                        cns.approval = "Approved"
                    elif js['approveStatus'] == "102":
                        cns.approval = "Submitted"
                    elif js['approveStatus'] == "103":
                        cns.approval = "Rejected"
                    elif js['approveStatus'] == "104":
                        cns.approval = "Voided"
                    cns.save()                    

        for rec in json_dump['records']:
            context['details'].append(rec)
    return render(request, 'credit_note/cn_list.html', context)

@login_required  
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

@login_required
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

@login_required
def cancel_cn(request, inv, cn ):
    cn = CreditNote.objects.get(id = id)
    msg = {}
    msg['inv_id'] =  inv_context(cn.invoice.json_response)['invoiceId']
    msg['cn_ref'] = cn.reference
    
    form = CnCancelForm()
    msg['form']= form
    if request.method == 'POST':
        form = CnCancelForm(request.POST)

        if form.is_valid():
            msg['reason'] = form.cleaned_data['reason']
            cn_dict = cancel_cn_helper(request, msg)
            form = form.save(commit=False)
            form.cn = cn
            form.save()
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('create-build-invoice','invoice.slug')
    return render(request, 'credit_note/cancel_cn.html',msg)

# this cancels a CN that is not yet approved
@login_required
def cancel_cn_application(request, id, ref):
    details = {
        "businessKey": id,
        "referenceNo": ref
        }
    message = encode(str(details)).decode()
    payload_data = payload_info(request,"T120",message)
    request_json = post_message(request, payload_data)
    if request_json == "":
        messages.error(request, 'Check that the credit note is not approved/Rejected, It must have a status of submitted!!')
    else:
        messages.success(request, 'Invoice Cancelled successfully')
    return redirect('cn_list')

@login_required
def cancel_approved_cn(request, fdn, cn, ref):
    note = CreditNote.objects.get(reference = ref)
    msg = {}
    msg['oriInvoiceId']=fdn
    msg['invoiceNo']=cn
    msg['invoiceApplyCategoryCode']="104"

    form = CnCancelForm()
    if request.method == 'POST':
        form = CnCancelForm(request.POST)
        if form.is_valid():
            msg['reasonCode'] = form.cleaned_data['reason']
            msg['reason'] = form.cleaned_data['details']
            form = form.save(commit=False)
            form.cn = note
            message = encode(str(msg)).decode()
            payload_data = payload_info(request,"T114",message)
            request_json = post_message(payload_data)
            form.save()
            messages.success(request, 'Credit note issued successfully')
            return redirect('cn_list')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('cancel_approved_cn', fdn, cn, ref)
    return render(request, 'credit_note/cancel_cn.html',{'form':form})


def barcode_generator(request):
    if request.method == "POST":
        form = BarCodeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Barcode Generated successfuly")
        else:
            messages.error(request,"Error Generating code")
    else:
        form = BarCodeForm()
    context = {'form': form, 'barcodes':BarCode.objects.all().order_by('-date_created')}
    return render(request, 'barcode/barcode.html', context)