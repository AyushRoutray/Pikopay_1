from django import forms
from core.models import CreditCard, KYC
from django.forms import ImageField, FileInput, DateInput
from django.contrib.auth.forms import UserCreationForm
from core.models import User

class CreditCardForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Card Holder Name"}))
    number = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"Card Number"}))
    month = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"Expiry Month"}))
    year = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"Expiry Month"}))
    cvv = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"CVV"}))

    class Meta:
        model = CreditCard
        fields = ['name', 'number', 'month', 'year', 'cvv', 'card_type']

class AmountForm(forms.ModelForm):
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"$30"}))
    
    class Meta:
        model = CreditCard
        fields = ['amount']
        
class DateInput(forms.DateInput):
    input_type = 'date'

class KYCForm(forms.ModelForm):
    identity_image = ImageField(widget=FileInput)
    image = ImageField(widget=FileInput)
    signature = ImageField(widget=FileInput)

    class Meta:
        model = KYC
        fields = [ 'full_name', 'image', 'marrital_status', 'gender', 'identity_type', 'identity_image', 'date_of_birth', 'signature', 'country', 'state', 'city', 'mobile', 'fax']
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder":"Full Name"}),
            "mobile": forms.TextInput(attrs={"placeholder":"Mobile Number"}),
            "fax": forms.TextInput(attrs={"placeholder":"Fax Number"}),
            "country": forms.TextInput(attrs={"placeholder":"Country"}),
            "state": forms.TextInput(attrs={"placeholder":"State"}),
            "city": forms.TextInput(attrs={"placeholder":"City"}),
            'date_of_birth':DateInput
        }
        
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
