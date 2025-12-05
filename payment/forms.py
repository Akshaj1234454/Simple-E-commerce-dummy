from django import forms

class CheckoutForm(forms.Form):
	address = forms.CharField(
		label='Address',
		required=True,
		widget=forms.TextInput(attrs={
			'class': 'checkout-input',
			'placeholder': 'Enter your address',
		})
	)
	pinCode = forms.CharField(
		label='Pincode',
		required=True,
		max_length=6,
		min_length=6,
		widget=forms.TextInput(attrs={
			'class': 'checkout-input',
			'placeholder': 'Enter your pincode',
			'pattern': '\\d{6}',
		})
	)
	mobileNumber = forms.CharField(
		label='Mobile Number',
		required=True,
		max_length=10,
		min_length=10,
		widget=forms.TextInput(attrs={
			'class': 'checkout-input',
			'placeholder': 'Enter your mobile number',
			'pattern': '\\d{10}',
		})
	)

