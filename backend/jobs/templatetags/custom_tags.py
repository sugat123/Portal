from jobs.models import *
from django import template
register = template.Library()


@register.simple_tag
def check(verifiedid):
    print(verifiedid)
    verify = Verification.objects.filter(id=verifiedid)
    
    for i in verify:
        if i.paid_status is True:
            return True
        else:
            return False
   
    
