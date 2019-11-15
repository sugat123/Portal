from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.template import RequestContext
from django.http import HttpResponseRedirect


# Create your views here.

def roomtype(request):
    roomtype = RoomType.objects.all()
    return render(request, 'room/roomtype.html', {'roomtype':roomtype})

@login_required(login_url='/users/login/')
def roomlist(request, roomtype_id):
    room = get_object_or_404(RoomType, pk=roomtype_id)
    searchedroom = SearchedRoom.objects.filter(room_type_id = roomtype_id)
    postedroom = PostedRoom.objects.filter(room_type_id = roomtype_id)
    # image = Image.objects.all()
    context ={'searchedroom':searchedroom, 'postedroom':postedroom, 'room':room}
    return render(request, 'room/roomlist.html', context)

@login_required
def searchroom(request, roomtype_id):
    room = get_object_or_404(RoomType, pk=roomtype_id)
    if request.method == "POST":
        form = SearchRoomForm(request.POST or None)
        if form.is_valid():
            searched_room = form.save(commit=False)
            searched_room.save()
            return redirect('room:roomtype')
        else:
            print(form.errors)
    else:
        form = SearchRoomForm()
    
    context = {'form':form, 'room':room}
    return render(request, 'room/findroom.html', context)

@login_required
def postroom(request, roomtype_id):
    # roomtype = get_object_or_404(RoomType, pk=roomtype_id)
    room = get_object_or_404(RoomType, pk=roomtype_id)
    facilities =  Facility.objects.all()
    ImageFormSet = modelformset_factory(Image, fields=('image',), extra=5)
    if request.method == "POST":
        print("1")
        postedroom_form = PostedRoomForm(request.POST or None)
        # image_form = ImageForm(request.POST or None, request.FILES)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        print("2")

        if postedroom_form.is_valid() and formset.is_valid():
            print("3")
    
            postedroom = postedroom_form.save(commit=False)
            postedroom.save()
           
            # image = image.save(commit=False)
            print("4")
            for form in formset:
                # image = form['image']
                try:
                    photo = Image(posted_room=postedroom, image=form.cleaned_data['image'])
                    photo.save()
                    
                except Exception as e:
                    print(e)
                    print("5")
                    
                
                
            print("6")
            
            return redirect('room:roomtype')
        else:
            print(postedroom_form.errors, formset.errors)
        
    else:
        print("7")
        postedroom_form = PostedRoomForm()
        formset = ImageFormSet(queryset=Image.objects.none())
        context ={'room':room,'facilities':facilities,'postedroom_form':postedroom_form, 'formset': formset}

    return render(request, 'room/addroom.html', context)

# def postroom2(request, id):
#     room = get_object_or_404(RoomType, id=id)
   
#     facilities = Facility.objects.all()

#     ImageFormSet = modelformset_factory(Image, fields=('image',), extra=5)

#     if request.method == 'POST':

#         postedroom_form = PostedRoomForm(request.POST or None)
#         formset = ImageFormSet(request.POST or None, request.FILES or None)

#         if postedroom_form.is_valid() and formset.is_valid():
#             # postedroom = postedroom_form(commit)
#             postedroom.save()
#             for form in formset:
#                 print("1")
#                 # image = form['image']
#                 try:
#                     print("2")
#                     photo = Image(posted_room=postedroom_form, image=form.cleaned_data['image'])
#                     print("3")
#                     photo.save()
#                     print("4")
#                 except Exception as e:
#                     print("5")
#                     print(e)
           

#             return redirect('room:roomtype')
#     else:
#         print("6")
#         postedroom_form = PostedRoomForm()
#         formset = ImageFormSet(queryset=Image.objects.none())

#     context = {'room': room,
#                'formset':formset,
#                 'facilities': facilities,
#                'form': postedroom_form}
#     print("7")
#     return render(request, 'room/addroom.html', context)
        
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

@login_required
def detail(request, user_type, room_id):
    if user_type == 'Job Seeker':
        room = PostedRoom.objects.get(id=room_id)
        # facility = Facility.objects.filter(room_type_id=)
    else:
        room = SearchedRoom.objects.get(id=room_id)

    return render(request, 'room/detail.html', {'room':room})
        

