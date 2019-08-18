from .models import *


# p = PostedJob.objects.all()
# a = AppliedJob.objects.all()


def count():
    p = PostedJob.objects.all()
    a_matched = []
    p_matched = []
    score = []
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
                p_matched.append(s.id)
                a_matched.append(x.id)
                score.append(score_temp)

    return [p_matched, a_matched, score]
