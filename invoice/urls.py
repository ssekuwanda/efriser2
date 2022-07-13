from django.urls import path
from . import views

urlpatterns = [
path('login',views.login, name='login'),
path('logout',views.logout, name='logout'),
path('dashboard',views.dashboard, name='dashboard'),
path('products', views.products, name='products'), 

# -------------Clients--------------
path('clients',views.clients, name='clients'),
path('client_home/<slug:slug>', views.client_home, name='client_home'),

# ----------- Invoice---------------
path('invoices/', views.invoices, name='all_invoices'),
path('invoices/create/<slug:slug>',views.createInvoice, name='create-invoice'),
path('invoices/create-build/<slug:slug>',views.createBuildInvoice, name='create-build-invoice'),
path('invoice-pdf/<slug:slug>', views.pdfInvoice, name='invoices-doc'),
path('inv_list/', views.inv_list, name='inv_list'),
path('inv_details/', views.inv_details, name='inv_details'),

# ---------------Product----------------
path('prod_delete/<slug:slug>',views.prod_delete, name='prod_delete'),
path('prod_update/<slug:slug>',views.productsMaintance, name='prod_update'),
path('prod-inquire/<slug:slug>',views.goods_inquiry, name='goods_inquiry'),
path('dictionary>',views.dictonary, name='dictonary'),


# --------------Credit notes---------
path('credit_notes', views.creditNoteHome, name='creditnotes'),
path('credit_notes_list', views.cn_list, name='cn_list'),
path('creditnote/create/<slug:slug>',views.createCreditNote, name='create-creditnote'),
path('creditnote/refresh_cn_status/<int:id>',views.refresh_cn_status, name='cn_refresh'),
path('creditnote/cancel-cn/<int:id>',views.cancel_cn, name='cancel_cn'),
path('creditnote/cancel-fresh/<str:id>/<str:ref>',views.cancel_cn_application, name='cancel_fresh_cn'),
path('creditnote/cancel-approved/<str:fdn>/<str:cn>/<str:ref>',views.cancel_approved_cn, name='cancel_approved_cn'),



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
