from django.urls import path
from . import views

urlpatterns = [
path('login',views.login, name='login'),
path('logout',views.logout, name='logout'),
path('dashboard',views.dashboard, name='dashboard'),
path('products', views.products, name='products'), 
path('clients',views.clients, name='clients'),
path('invoices/<slug:slug>', views.invoices, name='invoices'),
path('client_home/<slug:slug>', views.client_home, name='client_home'),

path('credit_notes', views.creditNoteHome, name='creditnotes'),



#Create URL Paths
path('invoices/create/<slug:slug>',views.createInvoice, name='create-invoice'),
path('invoices/create-build/<slug:slug>',views.createBuildInvoice, name='create-build-invoice'),
path('creditnote/create/<slug:slug>',views.createCreditNote, name='create-creditnote'),

#Delete an invoice
    # path('invoices/delete/<slug:client_slug>/<slug:invoice_slug>',views.deleteInvoice, name='delete-invoice'),

#PDF and EMAIL Paths
# path('invoices/view-pdf/<slug:slug>',views.viewPDFInvoice, name='view-pdf-invoice'),
# path('invoices/view-document/<slug:slug>',views.viewDocumentInvoice, name='view-document-invoice'),
# path('invoices/email-document/<slug:slug>',views.emailDocumentInvoice, name='email-document-invoice'),

#Company Settings Page
# path('company/create', views.createCompany, name='company-settings'),
# path('company/settings',views.companySettings, name='company-settings'),
]
