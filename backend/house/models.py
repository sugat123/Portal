from django.db import models
from django.contrib.auth.models import User


class Facility(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=250 , unique=True)

    def __str__(self):
        return " facility-{}".format(self.title)


class SellerPost(models.Model):
    owner_name = models.CharField(max_length=250)
    price = models.CharField(max_length=50)
    location = models.CharField(max_length=250)
    area = models.CharField(max_length=250)
    floor = models.IntegerField()
    no_of_room = models.IntegerField()
    direction_faced = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact =  models.CharField( max_length = 120, null=True , blank=True)
    facility = models.ManyToManyField(Facility)
    

    class Meta :
        verbose_name_plural='House detail posted by Seller'
    
    def __str__(self):
        return " owner_name-{}".format(self.owner_name)

class BuyerPost(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.CharField(max_length=50 , null=True , blank=True)
    location = models.CharField(max_length=250)
    area = models.CharField(max_length=250)
    floor = models.IntegerField(null=True)
    no_of_room = models.IntegerField()
    direction_faced = models.CharField(max_length=50)
    contact =  models.CharField(max_length=120 , null=True , blank=True)
    facility = models.ManyToManyField(Facility)



    class Meta :
        verbose_name_plural='House detail posted by Buyer'
    
    def __str__(self):
        return " no_of_room-{}".format(self.no_of_room)

    
def get_image_filename(instance, filename):
    id = instance.seller_post.id
    return "sellerhouse_image/{}".format(id)

class Image(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    seller_post = models.ForeignKey(SellerPost, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                                 verbose_name='Image')

class Matched(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey( User , on_delete=models.CASCADE,related_name='%(class)s_seller_user_id')
    buyer = models.ForeignKey( User , on_delete=models.CASCADE,related_name='%(class)s_buyer_user_id')
    score = models.FloatField()

    class Meta:
        verbose_name_plural = 'Matches Houses '

    def __str__(self):
        return 'score-{}'.format(self.score)