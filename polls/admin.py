from polls.models import Poll
from django.contrib import admin
from polls.models import Choice

#admin.site.register(Poll)
class ChoiceInLine(admin.TabularInline):
	model = Choice
	extra = 3
	

class PollAdmin(admin.ModelAdmin):
	fieldsets = [
		('Question',			{ 'fields': ['question']}),
		('Date information', {'fields': ['pub_date'],'classes':['collapse']})
	]
	inlines = [ChoiceInLine]
admin.site.register(Poll,PollAdmin)
#admin.site.register(Choice)