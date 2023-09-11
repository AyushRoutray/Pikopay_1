"""
URL configuration for Pikopay_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views, transfer, transaction, payment_request, credit_card
from django.conf.urls import include

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),

    # Transfers
    path("search-account/", transfer.search_users_account_number, name="search-account"),
    path("amount-transfer/<account_number>/", transfer.AmountTransfer, name="amount-transfer"),
    path("amount-transfer-process/<account_number>/", transfer.AmountTransferProcess, name="amount-transfer-process"),
    path("transfer-confirmation/<account_number>/<transaction_id>/", transfer.TransferConfirmation, name="transfer-confirmation"),
    path("transfer-process/<account_number>/<transaction_id>/", transfer.TransferProcess, name="transfer-process"),
    path("transfer-completed/<account_number>/<transaction_id>/", transfer.TransferCompleted, name="transfer-completed"),


    # transactions
    path("transactions/", transaction.transaction_lists, name="transactions"),
    path("transaction-detail/<transaction_id>/", transaction.transaction_detail, name="transaction-detail"),

    # Payment Request
    path("request-search-account/", payment_request.SearchUsersRequest, name="request-search-account"),
    path("amount-request/<account_number>/", payment_request.AmountRequest, name="amount-request"),
    path("amount-request-process/<account_number>/", payment_request.AmountRequestProcess, name="amount-request-process"),
    path("amount-request-confirmation/<account_number>/<transaction_id>/", payment_request.AmountRequestConfirmation, name="amount-request-confirmation"),
    path("amount-request-final-process/<account_number>/<transaction_id>/", payment_request.AmountRequestFinalProcess, name="amount-request-final-process"),
    path("amount-request-completed/<account_number>/<transaction_id>/", payment_request.RequestCompleted, name="amount-request-completed"),


    # Request Settlement
    path("settlement-confirmation/<account_number>/<transaction_id>/", payment_request.settlement_confirmation, name="settlement-confirmation"),
    path("settlement-processing/<account_number>/<transaction_id>/", payment_request.settlement_processing, name="settlement-processing"),
    path("settlement-completed/<account_number>/<transaction_id>/", payment_request.SettlementCompleted, name="settlement-completed"),
    path("delete-request/<account_number>/<transaction_id>/", payment_request.deletepaymentrequest, name="delete-request"),



    # Credit Card URLS
    path("card/<card_id>/", credit_card.card_detail, name="card-detail"),
    path("fund-credit-card/<card_id>/", credit_card.fund_credit_card, name="fund-credit-card"),
    path("withdraw_fund/<card_id>/", credit_card.withdraw_fund, name="withdraw_fund"),
    path("delete_card/<card_id>/", credit_card.delete_card, name="delete_card"),
    
    path("dashboard/", views.dashboard, name="dashboard"),
    path("account", views.account, name="account"),
    path("kyc-reg/", views.kyc_registration, name="kyc-reg"),
    
    path("sign-up/", views.RegisterView, name="sign-up"),
    path("sign-in/", views.LoginView, name="sign-in"),
    path("sign-out/", views.logoutView, name="sign-out"),
    path("guestsign-in/", views.GuestLoginView, name="guestsign-in"),
    path("convert/", include("guest_user.urls")),
]
