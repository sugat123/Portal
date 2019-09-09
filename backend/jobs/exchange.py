from jobs.models import Exchange, Match, Verification, Payment
from django.contrib.auth.models import User
import jobs.views


def exchange():
    test = []
    count = 0
    for q in Exchange.objects.all():
        test.append((q.match_id, q.user_id))

    for match in Match.objects.all():
        for j in Verification.objects.filter(match_id=match.id):
            if (j.match_id, j.user_id) not in test:
                count = count + 1
                print(count)
                if count == 2:
                    # for n in User.objects.filter(id=j.user_id):
                    #     if n.profile.user_type == 'Job Seeker':
                    for k in User.objects.filter(id=match.applied_id):
                        for m in User.objects.filter(id=match.posted_id):
                            text1 = "Your payment has been completed and this is the contact number: " + \
                                m.profile.number + " of employeer: " + m.username + " for job you applied."
                            # sms(m.profile.number, text2 ) #sms to giver
                            # sms(k.profile.number, text1 ) #sms to seeker
                            # email to seeker
                            jobs.views.email([k.email], text1)
                            e1 = Exchange()
                            e1.user_id = k.id
                            e1.match_id = match.id
                            e1.save()

                            text2 = "Your payment has been completed and this is the contact number: " + \
                                k.profile.number + " of job seeker: " + k.username + " for the job you posted."
                            # email to giver
                            jobs.views.email([m.email], text2)
                            e2 = Exchange()
                            e2.user_id = m.id
                            e2.match_id = match.id
                            e2.save()


def verify():
    test = []
    for l in Verification.objects.all():
        test.append(l.payment_id)
    print(test)

    for i in Match.objects.all():
        for j in Payment.objects.all():
            if j.id not in test:
                if i.applied_id == j.profile_id and i.job_type == j.product:

                    v = Verification()
                    v.payment_id = j.id
                    v.user_id = j.profile_id
                    v.paid_status = True
                    v.match_id = i.id
                    v.save()
                elif i.posted_id == j.profile_id and i.job_type == j.product:

                    v = Verification()
                    v.payment_id = j.id
                    v.user_id = j.profile_id
                    v.paid_status = True
                    v.match_id = i.id
                    v.save()
