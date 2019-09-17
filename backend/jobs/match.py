from .models import *
import jobs.views


def count():
    p = PostedJob.objects.all()
    a_matched = []
    p_matched = []
    score = []
    job_type = []
    for s in p:
        # print(s.id)
        posted = PostedJob.objects.get(id=s.id)
        a = posted.skills.all()
        list1 = []

        for i in a:
            list1.append(i.id)

        # print(list1)
        a = AppliedJob.objects.all()
        for x in a:
            # print(x.id)
            applied = AppliedJob.objects.get(id=x.id)
            b = applied.skills.all()
            list2 = []

            for j in b:
                list2.append(j.id)
            # print(list2)

            count = 0
            for k in list1:
                for l in list2:
                    if k == l:
                        count = count+1
            # print(count)
            score_temp = count/len(list1)
            if score_temp >= 0.65:
                p_matched.append(s.user_id)
                a_matched.append(x.user_id)
                score.append(score_temp)
                job_type.append(x.job_type.id)

    return [p_matched, a_matched, score, job_type]


def match(c):
    p = c[0]
    a = c[1]
    s = c[2]
    job = c[3]

    posted = []
    applied = []
    matches = []
    test = []
    test_p = []
    test_a = []

    for n in Match.objects.all():
        test.append((n.posted_id, n.applied_id, n.score))
        test_p.append((n.posted_id))
        test_a.append((n.applied_id))

    for i, j, l in zip(p, a, s):

        if (i, j, l) not in test:
            for post in PostedJob.objects.filter(user_id=i):
                posted.append(post.user.email)

                text1 = ' We have found the best match for the job you had posted. Please Check you account to find the detail and for payment '
                jobs.views.email_match([post.user.email], text1)

                # sms(post.user.profile.number, text1)
            for apply in AppliedJob.objects.filter(user_id=j):

                applied.append(apply.user.email)

                text2 = ' We have found the best match for the job you needed. Please Check you account to find the detail and for payment '
                jobs.views.email_match([apply.user.email], text2)

                # sms(apply.user.profile.number, text2)

    for k in range(len(p)):

        matches.append((p[k], a[k], s[k]))
        if (p[k], a[k], s[k]) not in test:
            match = Match()
            match.posted_id = p[k]
            match.applied_id = a[k]
            match.score = s[k]
            match.job_type = int(job[k])
            match.save()

    print(matches)
