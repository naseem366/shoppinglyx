from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Customer,Product,Cart,OrderPlaced
from django.views import View 
from .forms import CustomerRegistrationForm,AddProductForm
from django.contrib.auth.models import User,auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomerProfileForm
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import stripe
from django.conf import settings
stripe.api_key=settings.STRIPE_SECRET_KEY

#def home(request):
 #return render(request, 'app/home.html')

class ProductView(View):
 	def get(self,request):
	 	topwears=Product.objects.filter(category='TW')
	 	bottomwears=Product.objects.filter(category='BW')
	 	mobiles=Product.objects.filter(category='M')
	 	totalItem=len(Cart.objects.filter(user=request.user))

	 	context={
	 	'topwears':topwears,
	 	'bottomwears':bottomwears,
	 	'mobiles':mobiles,
	 	'totalItem':totalItem,
	 	}
	 	return render(request, 'app/home.html',context)


#def product_detail(request):
 #return render(request, 'app/productdetail.html')

class ProductDetailView(View):
	def get(self , request , pk):
		product=Product.objects.get(pk=pk)
		totalItem=len(Cart.objects.filter(user=request.user))
		item_already_in_cart=False
		if request.user.is_authenticated:
			item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
		return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalItem':totalItem})

@login_required
def add_to_cart(request):
	user=request.user
	product_id=request.GET.get('prod_id')
	product=Product.objects.get(id=product_id)
	Cart(user=user,product=product).save()
	return redirect('/cart')


def buy_now(request):
	user=request.user
	product_id=request.GET.get('prod_id')
	product=Product.objects.get(id=product_id)
	Cart(user=user,product=product).save()
	return redirect('/checkout')
 #return render(request, 'app/buynow.html')


@login_required
def show_cart(request):
	if request.user.is_authenticated:
		user=request.user
		cart=Cart.objects.filter(user=user)
		totalItem=len(Cart.objects.filter(user=request.user))
		amount=0.0
		shipping_amount=70.0
		total_amount=0.0
		cart_product=[p for p in Cart.objects.all() if p.user ==user]
		if cart_product:
			for p in cart_product:
				tempamount=(p.quntity * p.product.selling_price)
				amount +=tempamount
				totalamount=shipping_amount + amount
			return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalItem':totalItem})
		else:

		    return render(request, 'app/emptycart.html')

def plus_cart(request):
	if request.method =='GET':
		prod_id=request.GET['prod_id']
		c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quntity+=1
		c.save()
		amount=0.0
		shipping_amount=70.0
		total_amount=0.0
		cart_product=[p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount=(p.quntity * p.product.selling_price)
			amount +=tempamount
			totalamount=shipping_amount + amount

		data={
		
		'quntity':c.quntity,
		'amount':amount,
		'totalamount':totalamount
		}
		return JsonResponse(data)

def minus_cart(request):
	if request.method =='GET':
		prod_id=request.GET['prod_id']
		c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quntity-=1
		c.save()
		amount=0.0
		shipping_amount=70.0
		total_amount=0.0
		cart_product=[p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount=(p.quntity * p.product.selling_price)
			amount +=tempamount
			totalamount=shipping_amount + amount

		data={
		
		'quntity':c.quntity,
		'amount':amount,
		'totalamount':totalamount
		}
		return JsonResponse(data)


def remove_cart(request):
	if request.method =='GET':
		prod_id=request.GET['prod_id']
		totalItem=len(Cart.objects.filter(user=request.user))
		c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount=0.0
		shipping_amount=70.0
		total_amount=0.0
		cart_product=[p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount=(p.quntity * p.product.selling_price)
			amount +=tempamount
			#totalamount=shipping_amount + amount

		data={
		
		'amount':amount,
		'totalamount':amount+shipping_amount,
		'totalItem':totalItem,
		}
		return JsonResponse(data)


@login_required
def address(request):
	address=Customer.objects.filter(user=request.user)
	return render(request, 'app/address.html',{'address':address})
    #return render(request, 'app/address.html',{'address':address})



@login_required
def orders(request):
	user=request.user
	order_placed=OrderPlaced.objects.filter(user=user)
	totalItem=len(Cart.objects.filter(user=request.user))
	return render(request, 'app/orders.html',{'order_placed':order_placed,'totalItem':totalItem})

#naseem h pagal 

#def change_password(request):
 #return render(request, 'app/changepassword.html')




def mobile(request,data=None):
	if data==None:
		mobiles=Product.objects.filter(category='M')
	elif data == 'redmi' or data=='samsung':
		mobiles=Product.objects.filter(category='M').filter(brand=data)
	elif data=='bellow':
		mobiles=Product.objects.filter(category='M').filter(selling_price__lt=10000)
	elif data=='above':
		mobiles=Product.objects.filter(category='M').filter(selling_price__gt=10000)

	return render(request, 'app/mobile.html',{'mobiles':mobiles})
	
class CustomerRegistrationView(View):
	def get(self,request):
		form=CustomerRegistrationForm()
		return render(request, 'app/customerregistration.html',{'form':form})
	def post(self,request):
		form=CustomerRegistrationForm(request.POST)
		if form.is_valid():
			messages.success(request,'Congratulation!! Registered Successfully ')
			form.save()
		return render(request, 'app/customerregistration.html',{'form':form})
		
@method_decorator(login_required,name='dispatch')
class CustomerProfileView(View):
	def get(self , request):
		form=CustomerProfileForm()
		return render(request, 'app/profile.html',{'form':form})
	def post(self,request):
		form=CustomerProfileForm(request.POST)
		
		if form.is_valid():
			user=request.user
			name=form.cleaned_data['name']
			locality=form.cleaned_data['locality']
			city=form.cleaned_data['city']
			state=form.cleaned_data['state']
			zipcode=form.cleaned_data['zipcode']
			reg=Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
			reg.save()
			messages.success(request,'Congratulation !! Profile Updated Successfully')
		return render(request, 'app/profile.html',{'form':form})


@login_required
def checkout(request):
	user=request.user
	address=Customer.objects.filter(user=user)
	cart_items=Cart.objects.filter(user=user)
	amount=0.0
	shipping_amount=70.0
	total_amount=0.0
	cart_product=[p for p in Cart.objects.all() if p.user ==user]
	if cart_product:
		for p in cart_product:
			tempamount=(p.quntity * p.product.selling_price)
			amount +=tempamount
			totalamount=shipping_amount + amount

	return render(request, 'app/checkout.html',{'address':address,'amount':amount,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
	user=request.user
	custid=request.GET.get('custid')
	print(custid)
	customer=Customer.objects.get(id=custid)
	cart=Cart.objects.filter(user=user)
	for c in cart:
		OrderPlaced(user=user,customer=customer,product=c.product,quntity=c.quntity).save()
		c.delete()
	return redirect('/orders')

def user_management(request):
	if request.user.is_superuser:
	    form=User.objects.all()
	    return render(request,'app/show.html',{'form':form})
	else:
		user=request.user
		form=Customer.objects.filter(user=user)
		return render(request,'app/page.html',{'form':form})


def addproduct(request):
    if request.method=='POST': # this means the form has data
        form = AddProductForm(request.POST) # get the form and it data
        if form.is_valid(): # check if it is valid
            title = form.cleaned_data.get('title') # clean the data
            selling_price= form.cleaned_data.get('selling_price') # clean the data
            discount_price= form.cleaned_data.get('discount_price') # clean the data
            form.save() # save the data to the model
            messages.success(request, 'Your product has been added!')
            return redirect('addproduct')
        else: # form not valid so display message and retain the data entered
            form = AddProductForm(request.POST)
            messages.success(request, 'Error in creating your product, the form is not valid!')
            return render(request, 'app/addproduct.html', {'form':form})
    else: #the form has no data
        form = AddProductForm() #produce a blank form
        return render(request, 'app/addproduct.html', {'form':form})


class AddProductView(View):
	def get(self,request):
		form=AddProductForm()
		return render(request,'app/addproduct.html',{'form':form})
	def post(self, request):
		form=AddProductForm(request.POST)
		if form.is_valid():
			print("hello form datas")
			messages.success(request,'Congratulation !! Product Add Successfully')
			form.save()
			print("form is save or not ")
		return render(request, 'app/addproduct.html',{'form':form})


# client id = AbdFmXZxL1sDFNizsIM20px-XP_zck-hj9eYh-XHDYEApVMS3yYPHfSxY5maTaxBbA40_Jly6dNDXMxA
# sandbox acc = akashkhan1@gmail.com

# Secret key = EH2wr8FXK_pe5plIzVBWL--vVwJn6hwHxXUBJaccimJi6q0zOAkTtp5YHI41pqsECxhKAk1o8mW6_paN