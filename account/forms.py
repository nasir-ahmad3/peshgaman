from django import forms
from .models import User

# my forms 
class UserForms(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super(UserForms, self).__init__(*args, **kwargs)


		self.fields['username'].help_text = None
		if not user.is_superuser:
			self.fields['email'].disabled = True
			self.fields['is_author'].disabled = True
			self.fields['username'].disabled = True

	class Meta:
		model = User 
		fields = ['username', 'first_name', 'last_name', 'email', 'is_author']


from django.contrib.auth.forms import UserCreationForm


class RegistationForm(UserCreationForm):
	email = forms.EmailField(max_length=200, help_text='Required')    
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')