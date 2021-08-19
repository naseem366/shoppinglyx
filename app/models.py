from django.db import models
from django.contrib.auth.models import User
#from django.core.validators import maxValueValidator,minValueValidator
# Create your models here.
STATE_CHOICES=(
	
('AP','Andhra Pradesh'),
('AR','Arunachal Pradesh'),
('AS' ,'Assam'),
('BR' ,'Bihar'),
('CT' , 'Chhattisgarh'),
('GA' , 'Goa'),
('GJ' , 'Gujarat'),
('HR' , 'Haryana'),
('HP' , 'Himachal Pradesh'),
('JK' , 'Jammu and Kashmir'),
('JH' , 'Jharkhand'),
('KA' , 'Karnataka'),
('KL' , 'Kerala'),
('MP' , 'Madhya Pradesh'),
('MH' , 'Maharashtra'),
('MN' , 'Manipur'),
('ML' , 'Meghalaya'),
('MZ' , 'Mizoram'),
('NL' , 'Nagaland'),
('OR' , 'Odisha'),
('PB' , 'Punjab'),
('RJ' , 'Rajasthan'),
('SK' , 'Sikkim'),
('TN' , 'Tamil Nadu'),
('TG' , 'Telangana'),
('TR' , 'Tripura'),
('UT' , 'Uttarakhand'),
('UP' , 'Uttar Pradesh'),
('WB' , 'West Bengal'),
('AN' , 'Andaman and Nicobar Islands'),
('CH' , 'Chandigarh'),
('DN' , 'Dadra and Nagar Haveli'),
('DD' , 'Daman and Diu'),
('DL' , 'Delhi'),
('LD' , 'Lakshadweep'),
('PY' , 'Puducherry'),

	)

class Customer(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	name=models.CharField(max_length=200)
	locality=models.CharField(max_length=200)
	city=models.CharField(max_length=200)
	zipcode=models.IntegerField()
	state=models.CharField(choices=STATE_CHOICES,max_length=50)

	def __str__(self):
		return str(self.id)

CATEGORY_CHOICES=(

('M','MOBILE'),
('L','LAPTOP'),
('TW','Top Wear'),
('BW','Bottom Wear'),
	)

class Product(models.Model):
	title=models.CharField(max_length=100)
	selling_price=models.FloatField()
	discount_price=models.FloatField()
	description=models.TextField()
	brand=models.CharField(max_length=200)
	category=models.CharField(choices=CATEGORY_CHOICES,max_length=50)
	product_image=models.ImageField(upload_to='productimg')

	def __str__(self):
		return str(self.id)


class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	quntity=models.PositiveIntegerField(default=1)

	def __str__(self):
		return str(self.id)
	@property
	def total_cost(self):
		return self.quntity * self.product.selling_price


STATUS_CHOICES=(

('Accepted','Accepted'),
('Packed','packed'),
('On The Way','On The Way'),
('Delivered','Delivered'),
('Cancel','Cancel'),

	)

class OrderPlaced(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	quntity=models.PositiveIntegerField(default=1)
	ordered_date=models.DateTimeField(auto_now_add=True)
	status=models.CharField(choices=STATUS_CHOICES,max_length=50,default='Pending')


	@property
	def total_cost(self):
		return self.quntity * self.product.selling_price

