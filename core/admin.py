from django.contrib import admin
from core.models import Transaction, CreditCard, Notification
from core.models import Account, KYC
from core.models import User
from import_export.admin import ImportExportModelAdmin

class TransactionAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'status', 'transaction_type']
    list_display = ['user', 'amount', 'status', 'transaction_type', 'reciever', 'sender']


class CreditCardAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'card_type']
    list_display = ['user', 'amount', 'card_type']
    

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'amount' ,'date']

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Notification, NotificationAdmin)

class AccountAdminModel(ImportExportModelAdmin):
    list_editable = ['account_status', 'account_balance', 'kyc_submitted', 'kyc_confirmed'] 
    list_display = ['user', 'account_number' ,'account_status', 'account_balance', 'kyc_submitted', 'kyc_confirmed'] 
    list_filter = ['account_status']

class KYCAdmin(ImportExportModelAdmin):
    search_fields = ["full_name"]
    list_display = ['user', 'full_name', 'gender', 'identity_type', 'date_of_birth'] 


admin.site.register(Account, AccountAdminModel)
admin.site.register(KYC, KYCAdmin)

admin.site.register(User)


