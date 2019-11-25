
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.forms.models import modelformset_factory
from .models import *
from house.match import count,match
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/users/login/')
def owner(request):
    facilities = Facility.objects.all()
    c = count()
    match(c)
    ImageFormSet =modelformset_factory(Image, form=ImageForm ,extra=2)
    if request.method == "POST":
        sellerpost_form = SellerPostForm(request.POST or None)
        
        # image_form = ImageForm(request.POST or None, request.FILES)
        formset = ImageFormSet(request.POST or None , request.FILES or None)
        if sellerpost_form.is_valid() and formset.is_valid():
    
            sellerpost_form.save()
            sellerpost = sellerpost_form.save(commit=False)
            
            for form in formset:
                try: 
                    photo = Image(seller_post=sellerpost , image =form.cleaned_data['image'])
                    
                    photo.save()
                except Exception as e:
                    print(e)
            

            return redirect('main')
                
        else:
            print(sellerpost_form.errors , formset.errors)

    else:
        sellerpost_form =SellerPostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'house/ofeatures.html', 
    {'sellerpost_form':sellerpost_form,'formset':formset , 'facilities': facilities})

@login_required(login_url='/users/login/')

def buyer(request):
    facilities = Facility.objects.all()

    if request.method == "POST":
        buyerpost_form = BuyerPostForm(request.POST or None)
     
        if buyerpost_form.is_valid():
    
            # buyerpost = buyerpost_form.save(commit=False)
            buyerpost_form.save()
        
        
            return redirect('main')

        else:
            
            print(buyerpost_form.errors )

    else:
       
        buyerpost_form = BuyerPostForm()
        
    return render(request, 'house/ofeatures.html', 
    {'buyerpost_form':buyerpost_form ,'facilities':facilities} )


@login_required(login_url='/users/login/')

def house_list(request):
    seller= SellerPost.objects.all()
    buyer = BuyerPost.objects.all()

    return render(request, 'house/onewsfeed.html',
     { 'seller' :seller , 'buyer' : buyer })

def sellerhouse_detail (request, id ):
    house = get_object_or_404(SellerPost, id=id)
    print(house)
    price=PRICE[int(house.price)][1]
    images=  Image.objects.all()

    return render(request, 'house/seller_detail.html',
                    { 'house': house , 'price': price , 'images':images})

def buyerhouse_detail(request , id ):

    home = get_object_or_404(BuyerPost, id=id)
    price=PRICE[int(home.price)][1]
    return render(request, 'house/buyer_detail.html',
    { 'home': home , 'price': price})

def add_facility(request):
    if request.method == 'POST':
        form = AddFacilityForm(request.POST or None)
        if form.is_valid():
            facility =form.save(commit=False)
            facility.save()

            return redirect(request.META['HTTP_REFERER'])

        else:
            form =AddFacilityForm()

        return render(request , 'house/add_facility.html', {'form': form})

def email_match(recipient, text):
    subject = 'Match Found'
    send_mail(subject, text,'DJ Group <settings.EMAIL_HOST_USER>', recipient)
              
def email(recipient, text):
    subject = 'Contact Detail'

    send_mail(subject, text,
              'DJ Group <settings.EMAIL_HOST_USER>', recipient)
    return redirect('/')
        
    
        