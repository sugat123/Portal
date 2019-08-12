from .models import *

posted = PostedJob.objects.filter(job_type='cook')
applied = AppliedJob.objects.all()
