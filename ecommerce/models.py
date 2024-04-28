from django.db import models
from django.urls import reverse
from django.conf import settings
from book.models import Book
from django.utils import timezone

# https://pypi.org/project/shortuuid/
from shortuuid.django_fields import ShortUUIDField 



 # CART
class OrderBook(models.Model):
    id         = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    order      = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='orderbooks')
    book       = models.ForeignKey('book.Book', on_delete=models.CASCADE,  null=True )
    quantity   = models.PositiveIntegerField(default=1, null=True, blank=False)
    price      = models.DecimalField(default=00.00, max_digits=10, decimal_places=2 ,blank=False)
    book_title = models.CharField(max_length=200, default="", blank=True)  
    def __str__(self):
             return 'order id'+str(self.order.id)+'user'+str(self.order.user.email)+"book"+str(self.book.title)
           
    




class OrderStatus(models.TextChoices):
    PENDING    = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED    = 'Shipped'
    DELIVERED  = 'Delivered'
    CANCELLED  = 'Cancelled'

class PaymentStatus(models.TextChoices):
    PAID   = 'Paid'
    UNPAID = 'Unpaid' 

class PaymentMode(models.TextChoices):
    COD  = 'COD'
    CARD = 'CARD' 

class Order(models.Model):
    id             = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True , blank=False, related_name='orders')
    orderbooks     = models.ManyToManyField(Book, through='OrderBook')
    total_amount   = models.IntegerField(default=0) # total price
    order_date     = models.DateTimeField(auto_now_add=True, auto_now=False)   
    city           = models.CharField(max_length=400, default="", blank=False)
    zip_code       = models.CharField(max_length=100, default="", blank=False)
    street         = models.CharField(max_length=500, default="", blank=False)
    state          = models.CharField(max_length=100, default="", blank=False)
    country        = models.CharField(max_length=100, default="", blank=False)
    phone_no       = models.CharField(max_length=100, default="", blank=False)
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_mode   = models.CharField(max_length=30, choices=PaymentMode.choices, default=PaymentMode.COD)
    status         = models.CharField(max_length=60, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    
    
    def __str__(self):
        return f"Order No. #{self.id}"
    
    def get_absolute_url(self):
        return reverse('order-detail', kwargs = {'id':self.id})      # view_name='{model_name}-detail'
    
    class Meta:
        ordering = ('order_date',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    @property
    def orderbooks(self):
        orderbooks = OrderBook.objects.all().filter(order = self)
        print("orderbooks3 =" + str(orderbooks)) 
        return orderbooks
    


    # def get_total_quantity(self):
    #     total_quantity = 0
    #     order_books = self.get_order_books()
    #     for item in order_books:
    #         total_quantity += item.bookQuantity
    #     return total_quantity

    # def get_total_price(self):
    #     total_price = 0.0
    #     order_books = self.get_order_books()
    #     for item in order_books:
    #         total_price += item.bookPrice * item.bookQuantity
    #     return total_price
    
    

   




# This Cart model is not need, because the model OrderBook is does instead 
# class Cart(models.Model): 
#     id       = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
#     user     = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=False, related_name='cart') 
#     books    = models.ManyToManyField(Book)    
 
#     def __str__(self):
#         return str(self.user.email)





class Payment(models.Model):
    id           = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False )
    order        = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    amount       = models.FloatField(null=True, blank=True)
    is_paid      = models.BooleanField(default=False)
    checkout_id  = models.CharField(max_length=500)
    payment_date = models.DateTimeField(auto_now_add=True)