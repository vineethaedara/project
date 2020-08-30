from django.contrib import admin
from .models import Choice, Question,State,Account
from django.contrib.auth.admin import UserAdmin

class ChoiceInline(admin.TabularInline):
    model = Choice

class AccountAdmin(UserAdmin):
    list_display    =   ('email','username','date_joined','last_login','is_admin','is_staff')
    search_fields    =   ('email','username',)
    readonly_fields =   ('date_joined','last_login')

    filter_horizontal = ()
    list_filter =  ()
    fieldsets = ()




class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question_text']
    list_filter = ['pub_date']
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)     
admin.site.register(State)       
admin.site.register(Account,AccountAdmin)