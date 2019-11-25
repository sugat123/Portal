from .models import *
from django.contrib.auth.models import User
import jobs.views
import house.views
from difflib import SequenceMatcher
from django.core.mail import send_mail



def count():
    sellers = SellerPost.objects.all()
    buyers = BuyerPost.objects.all()
    s_matched = []
    b_matched = []
    score = []
      
    for seller in sellers:
        for buyer in buyers:
        # print(s.id)
            if seller.price == buyer.price:
                s= SequenceMatcher(None ,seller.location , buyer.location)

                if( s.ratio() > 0.6):
                    seller_facility = seller.facility.all()
                    buyer_facility = buyer.facility.all()
                    list1 = []

                    for facility in seller_facility:
                        x= facility.id
                        list1.append(x)
                    print(len(list1))


                    list2 = []

                    for facility in buyer_facility:
                        y = facility.id
                        list2.append(y)

                    print("pritining...")
                    print(list1, list2)
                    count = 0
                    if len(list1)>=len(list2):
                        total = len(list1)
                    else:
                        total = len(list2)
                    for i in list1:
                        for j in list2:
                            if i == j :
                                count = count + 1
                    
                    print(count)
                    score_temp = count/total
                    print(score_temp)
                    
                    if score_temp >= 0.65:
                        s_matched.append(seller.user_id)
                        b_matched.append(buyer.user_id)
                        score.append(score_temp)
                    

    return (s_matched, b_matched, score)







def match(count):
    s = count[0]
    b = count[1]
    score = count[2]
    

    sellered = []
    buyered = []
    matches = []
    test = []
    test_s = []
    test_b = []

    for n in Matched.objects.all():
        test.append((n.seller.id, n.buyer.id, n.score))
        test_s.append((n.seller.id))
        test_b.append((n.buyer.id))

    # print("length:", len(list(zip(s, b, score))))


    for i, j, l in zip(s, b, score):

        if (i, j, l) not in test:
                post = SellerPost.objects.filter(user_id=i).first()
                sellered.append(post.user.email)

                text1 = ' We have found the best match for the house you had posted. Please Check you account to find the detail and for payment '
                house.views.email_match([post.user.email], text1)

                # sms(post.user.profile.number, text1)
                apply=BuyerPost.objects.filter(user_id=j).first()

                buyered.append(apply.user.email)

                text2 = ' We have found the best match for the job you needed. Please Check you account to find the detail and for payment '
                house.views.email_match([apply.user.email], text2)

                # sms(apply.user.profile.number, text2)

    for k in range(len(s)):

        matches.append((s[k], b[k], score[k]))
        if (s[k], b[k], score[k]) not in test:
            match = Matched()
            user1 = User.objects.get(id=s[k])
            match.seller = user1
            user2 = User.objects.get(id=b[k])
            match.buyer = user2
            match.score = score[k]
            match.save() 

    print(matches)
