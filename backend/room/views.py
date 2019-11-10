from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.template import RequestContext


# Create your views here.

def roomtype(request):
    roomtype = RoomType.objects.all()
    return render(request, 'room/roomtype.html', {'roomtype':roomtype})


def roomlist(request, roomtype_id):
    room = get_object_or_404(RoomType, pk=roomtype_id)
    image = Image.objects.all()
    return render(request, 'room/roomlist.html',{'room':room, 'images':image})


def findroom(request, roomtype_id):
    return render(request, 'room/findroom.html')

@login_required
def postroom(request, roomtype_id):
    # roomtype = get_object_or_404(RoomType, pk=roomtype_id)
    room = get_object_or_404(RoomType, pk=roomtype_id)
    facilities =  Facility.objects.all()
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)
    if request.method == "POST":
        postedroom_form = PostedRoomForm(request.POST or None)
        # image_form = ImageForm(request.POST or None, request.FILES)
        formset = ImageFormSet(request.Post, request.FILES, queryset=Image.objects.none())

        if postedroom_form.is_valid() and formset.is_valid():
    
            postedroom = postedroom_form.save(commit=False)
            postedroom.save()
            # image = image.save(commit=False)
            for form in formset.cleaned_data:
                image = form['image']
                photo = Image(post=postedroom_form, image=image)
                photo.save()

    else:
        postedroom_form = PostedRoomForm()
        formset = ImageFormSet(queryset=Image.objects.none())
        context ={'room':room,'facilities':facilities,'postedroom_form':postedroom_form, 'formset': formset}
        return render(request, 'room/addroom.html', context)
        
@login_required
def add_facility(request):
    if request.method == 'POST':
        form = AddFacilityForm(request.POST or None)
        if form.is_valid():
            facility = form.save(commit=False)
            facility.save()
            # messages.success(request, 'Facility added')
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = AddFacilityForm()
    return render(request, 'room/add_facility.html', {'form': form})
        

