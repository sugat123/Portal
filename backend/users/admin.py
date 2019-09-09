from django.contrib import admin
from .models import *
from django.core.mail import send_mail

admin.site.register(ActivationCode)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):    
    list_display = ('username', 'first_name','email')

    def username(self,object):
        return object.user.username
        
    def first_name(self,object):
        return object.user.first_name
    
    def email(self, object):
        return object.user.email

    actions = [
        'send_email'
    ]

    def send_email(self, request, queryset):
        for profile in queryset:
            send_mail(subject="Employer/Employee Details", message="Hello", from_email='raktim.thapa9999.com',
                       recipient_list=[profile.user.email]) 
    send_email.short_description = "Send email"