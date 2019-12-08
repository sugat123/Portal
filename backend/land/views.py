from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.template import RequestContext
from django.http import HttpResponseRedirect

# Create your views here.


@login_required(login_url='/users/login/')
def landformbuy(request):
    facilities = Facility.objects.all()
    if request.method == "POST":
        searched_form = SearchLandForm(request.POST or None)
        if searched_form.is_valid():
            # searched_room = form.save(commit=False)
            searched_form.save()
            return redirect('land:landformbuy')
        else:
            print(searched_form.errors)
    else:
        searched_form = SearchLandForm()

    context = {'searched_form': searched_form, 'facilities': facilities}
    return render(request, 'land/landform.html', {})


@login_required(login_url='/users/login/')
def landformsell(request):
    facilities = Facility.objects.all()
    ImageFormSet = modelformset_factory(Image, fields=('image',), extra=4)
    if request.method == "POST":
        print("1")
        postedland_form = PostedLandForm(request.POST or None)
        # image_form = ImageForm(request.POST or None, request.FILES)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        print("2")

        if postedland_form.is_valid() and formset.is_valid():
            print("3")

            postedland_form.save()
            posted_land = postedland_form.save(commit=False)

            # image = image.save(commit=False)
            print("4")
            for form in formset:
                # image = form['image']
                try:
                    photo = Image(posted_room=posted_room,
                                  image=form.cleaned_data['image'])
                    photo.save()

                except Exception as e:
                    print(e)
                    print("5")

            # working without commit = False

            print("6")

            return redirect('land:landformsell')
        else:
            print(postedland_form.errors, formset.errors)

    else:
        print("7")
        postedroom_form = PostedLandForm()
        formset = ImageFormSet(queryset=Image.objects.none())

    context = {'facilities': facilities,
               'postedland_form': postedland_form, 'formset': formset}

    return render(request, 'land/landform.html', context)


@login_required(login_url='/users/login/')
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
    return render(request, 'land/add_facility.html', {'form': form})
