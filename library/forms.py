from django import forms
from library.models import Books
from django.core.validators import validate_email


class AddBookForm(forms.Form):
	book_id = forms.IntegerField()
	book_name = forms.CharField(max_length=50)
	count = forms.IntegerField()
	author = forms.CharField(max_length=50)

	def clean_book_name(self):
		book_name = self.cleaned_data['book_name']
		if len(book_name) < 3:
			raise forms.ValidateError("Atleast 3 characters required!")
		else:
			return book_name

	
class AddStudentForm(forms.Form):
	s_id = forms.CharField(max_length=4)
	name = forms.CharField(max_length=50)
	email = forms.EmailField()

	def clean_name(self):
		name = self.cleaned_data['name']
		if len(name) < 3:
			raise forms.ValidateError("Atleast 3 characters required")
		else:
			return name

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			validate_email(email)
			return email
		except ValidationError:
			raise forms.ValidationError("Enter a valid email address")

		
