from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RoomType(models.Model):
    kitchen = models.IntegerField()
    bedroom = models.IntegerField()
    hall = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together =(('kitchen', 'bedroom', 'hall'),)

    def __str__(self):
        return "Type-(Kitchen-{}, Bedroom-{}, Hall-{})".format(self.kitchen, self.bedroom, self.hall)

class Facility(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    #posted_room = models.ForeignKey(PostedRoom, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)

    class Meta:
        unique_together = (("room_type", "title"))
    
    def __str__(self):
        # return "{0}'s Skill: {1}".format(self.room_type, self.title)
        return("{0}'s Facility:{1}".format(self.room_type, self.title))


class PostedRoom(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=50, null=False, blank=False)
    location = models.CharField(max_length=50, null=False, blank=False)
    conditon = models.TextField(blank=True, null=True)
    facility = models.ManyToManyField(Facility)
    price = models.CharField(max_length=100, blank=False, null=False)
    contact = models.CharField(max_length=15)
    
    def __str__(self):
        return "Posted Room in location {}".format(self.location)

    def get_facility(self):
        return "\n, ".join([f.title for f in self.facility.all()])

def get_image_filename(instance, filename):
    id = instance.posted_room.id
    return "postedroom_image/{}".format(id)

class Image(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    posted_room = models.ForeignKey(PostedRoom, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                                   blank=True, null=True)

class SearchedRoom(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    facility = models.ManyToManyField(Facility)

    def __str__(self):
        return "Searched Room in location {}".format(self.location)




    


