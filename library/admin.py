from library.models import Books
from library.models import Students
from library.models import BookIssued
from django.contrib import admin

class StudentAdmin(admin.ModelAdmin):
	list_display = ('s_id', 'name')

class BooksAdmin(admin.ModelAdmin):
	list_display = ('book_id','book_name','author','count')
	



admin.site.register(Books,BooksAdmin)
admin.site.register(Students,StudentAdmin)
admin.site.register(BookIssued)