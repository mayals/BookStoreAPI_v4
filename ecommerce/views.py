from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import viewsets, permissions, generics, response, status,serializers
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from .models import Order, OrderBook
from book.models import Book
from .serializers import OrderSerializer,OrderBookSerializer,StripeSerializer
import stripe


########################################## Order ######################################################
# POST
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    data = request.data 
    orderbooks = request.data['orderbooks']  #  contains item data info about item we orderd 
    if orderbooks and len(orderbooks) == 0:
        return response.Response({'error': 'No order recieved'},status=status.HTTP_400_BAD_REQUEST)
    else:  
        for item in orderbooks :
            book = Book.objects.get(id = item['book'])  # 'book'  contain the value of id of selected book
            quantity =  item['quantity']
            if int(book.stock_quantity) > 0 :
                if int(quantity) > int(book.stock_quantity):
                    return  response.Response({'error':'Not enough stock available.'},status=status.HTTP_400_BAD_REQUEST)
            else:
                book.stock_quantity = 0
                book.save()
                return  response.Response({'error':f"This book '{book.title}' out of stock."},status=status.HTTP_400_BAD_REQUEST) 


        total_amount = sum(float(item['price']) * int(item['quantity']) for item in orderbooks)
                
        
        if not Order.objects.filter(user= request.user).exists():
            ## NEW ORDER ##  
            new_order = Order.objects.create(
                                            user         = request.user,
                                            order_date   = timezone.now(),
                                            city         = request.data['city'],
                                            zip_code     = request.data['zip_code'],
                                            street       = request.data['street'],
                                            phone_no     = request.data['phone_no'],
                                            country      = request.data['country'],
                                            state        = request.data['state'],
                                            total_amount = total_amount
            )
            ## orderbooks items  meaning CART items
            # Start adding items of orderbooks in the new_order we created above ## i.e., start add to cart that inside this order ##
            for item in orderbooks:
                    book = Book.objects.get(id = item['book']) # 'book'=  value of book id come from related field orderbooks that come from OrderBook model
                    book_title = book.title
                    orderbook = OrderBook.objects.create(
                                                        book       = book,
                                                        order      = new_order, # the order we created above 
                                                        quantity   = item['quantity'],# 'quantity'=  value of quantity come from related field orderbooks that come from OrderBook model
                                                        price      = item['price'],# 'price'=  value of 'price' come from related field orderbooks that come from OrderBook model
                                                        book_title = book_title
                    )
                    book.stock_quantity -= orderbook.quantity
                    book.save()
            serializer = OrderSerializer(new_order, many=False)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        
        ##  OLD ORDER completing ## 
        old_order = get_object_or_404(Order,user= request.user) # old order for  the same user(request.user) we find 
        ## orderbooks items meaning CART items
        # Start adding items of orderbooks in the new_order we created above ## i.e.,start add to cart that inside this order ##
        for item in orderbooks:
                book = Book.objects.get(id = item['book']) # 'book'=  value of book id come from related field orderbooks that come from OrderBook model
                book_title = book.title 
                if OrderBook.objects.all().filter(order=old_order,book=book).exists():
                    orderbook = OrderBook.objects.all().get(order=old_order,book=book)
                    orderbook.quantity  += int(item['quantity']) 
                    orderbook.save()
                    book.stock_quantity -= int(orderbook.quantity)
                    book.save()
                else:
                    orderbook = OrderBook.objects.create(
                                                        book       = book,
                                                        order      = old_order, # the order we created above 
                                                        quantity   = item['quantity'],# 'quantity'=  value of quantity come from related field orderbooks that come from OrderBook model
                                                        price      = item['price'],# 'price'=  value of 'price' come from related field orderbooks that come from OrderBook model
                                                        book_title = book_title
                    )
                    book.stock_quantity -= int(orderbook.quantity)
                    book.save()
        serializer = OrderSerializer(old_order, many=False)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)  
          
          


# 'get': 'list'
# 'get': 'retrieve',                                     
# 'delete': 'destroy'                                    
class OrderViewSet(viewsets.ModelViewSet):
    queryset= Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
 



# PUT
# PATCH
@api_view(['PUT','PATCH'])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_order_status(request,id):
    order = get_object_or_404(Order, id=id)
    order.status = request.data['status']
    order.save()
    serializer = OrderSerializer(order,many=False)
    return response.Response(serializer.data, status=status.HTTP_201_CREATED)





################################### OrderBook ###########################################
# https://www.django-rest-framework.org/api-guide/views/#api_view
#  OrderBook_view
@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def orderbooks_view(request):
    user = request.user
    order = get_object_or_404(Order ,user= request.user)
    if order :
        order_books =  OrderBook.objects.all().filter(order=order)
        # fields = ['id','order', 'book', 'quantity', 'price' ,'book_title']  
        # order_books = []
        # order = order
        # for item in order_books:
        #     book = item.book
        #     book_title = item.book_title
        #     book_quantity = item.quantity
        #     book_price = item.price
        #     item_cost = int(item.quantity) * float(item.price)
                   
            
        #     order_books.add({
        #                         'order'     : order,
        #                         'book'      :
        #                         'book_title': book_title,
        #                         'book_quantity': book_quantity,
        #                         'book_price': book_price,
        #                         'item_cost': item_cost
        #     })

        serializer = OrderBookSerializer(order_books, many=True)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED) 
        #return response.Response({ 'order_books': order_books  },status=status.HTTP_201_CREATED)
    return response.Response(status=status.HTTP_404_NOT_FOUND)  
  






########################################## Payment ####################################################################################


class PaymentView():
    pass




class StripeView(generics.CreateAPIView):
    serializer_class = StripeSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = Order.objects.get(id=serializer.validated_data['order'])
            total_amount  = order.total_amount 
            user = request.user
            stripe.api_key = settings.STRIPE_SECRET
            intent = stripe.PaymentIntent.create(
                                            # Stripe uses cents instead of dollars
                                            amount=int(total_amount * 100),
                                            currency="usd",
                                            description="Payment for " + order.id,
                                            receipt_email=user.email,
                                            automatic_payment_methods={"enabled": True},
            )
            response_data = {
                'client_secret': intent.client_secret
            }
            return response.Response(data=response_data, status=status.HTTP_201_CREATED)
        
        else:
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# class CreatePaymentIntent(APIView):
#     def post(self, request, *args, **kwargs):
#         amount = request.data.get('amount')  # Amount in cents
#         currency = 'usd'

#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         intent = stripe.PaymentIntent.create(
#                                             amount=amount,
#                                             currency=currency
#         )
#         return response.Response({'client_secret': intent.client_secret})



















# class OrderCreateAPIView(generics.CreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     # http_method_names = ["post"]

    # def perform_create(self, serializer):   
            ## NEW ORDER ##    
                                  #  Order fields = ['id', 'user', 'order_date', 'status',
                                  #'total_amount', 'city', 'zip_code', 'street', 'state',
                                  #'country', 'phone_no', 'payment_status', 'payment_mode',  
                                  #'orderbooks', # related_field -- come from OrderBook model  
            # data = self.request.data
            # print("data=" + str(data))                     
            # orderbooks = self.request.data['orderbooks']  #this data come  from related field orderbooks fom anothe model OrderBook
            # print("orderbooks1=" + str(orderbooks)) 
            # if orderbooks and len(orderbooks) == 0:
            #     return response.Response({'error': 'No order recieved'},status=status.HTTP_400_BAD_REQUEST)
            # else:
               
            #     total_amount = sum(float(item['price']) * int(item['quantity']) for item in orderbooks)
  
            #     # CREATE NEW ORDER #                   
            #     order = Order.objects.create(
            #                             user         = self.request.user,
            #                             order_date   = timezone.now(),
            #                             city         = self.request.data['city'],
            #                             zip_code     = self.request.data['zip_code'],
            #                             street       = self.request.data['street'],
            #                             phone_no     = self.request.data['phone_no'],
            #                             country      = self.request.data['country'],
            #                             state        = self.request.data['state'],
            #                             total_amount = total_amount
            #     )
                # CREATE NEW orderbook inside the a bove order, i.e, orderbooks CONTAIN order FIELD #
                # orderbooks = self.request.data['orderbooks']
                # print("orderbooks2=" + str(orderbooks)) 
                # for item in orderbooks:
                #     print('item ='+str(item))
                #     book = Book.objects.get(id = item['book']) # 'book'=  value of book id come from related field orderbooks that come from OrderBook model
                #     book_title = book.title 
                #     orderbook = OrderBook.objects.create(
                #                                         book= book,
                #                                         order = order, # the order we created above 
                #                                         quantity = item['quantity'],# 'quantity'=  value of quantity come from related field orderbooks that come from OrderBook model
                #                                         price = item['price'],# 'price'=  value of 'price' come from related field orderbooks that come from OrderBook model
                #                                         book_title = book_title,
                #     )
                #     order.save()
                #     orderbooks= order.orderbooks.all()
                #     serializer = OrderSerializer(order, many=False)
                #     return response.Response(serializer.data, status=status.HTTP_201_CREATED)
                # print("orderbooks3=" + str(orderbooks))
             
        #return response.Response({"IntegrityError": "This user already has order"},status=status.HTTP_400_BAD_REQUEST)
            
        




        
         # https://docs.djangoproject.com/en/4.2/topics/db/queries/#making-queries
            # https://stackoverflow.com/questions/50015204/direct-assignment-to-the-forward-side-of-a-many-to-many-set-is-prohibited-use-e
        # old order 
        # order =  Order.objects.filter(user=self.request.user)
            #raise validators.ValidationError({"IntegrityError": "This user has already order"},)
            
            
            # def get_serializer_context(self):
            #     print(super().get_serializer_context())
                 # Assuming you have user authentication
           
           
           
            # Ensure there is only one open order for request user 
            # if not Order.objects.filter(user=self.request.user).exists():    
            #     serializer.save(user=self.request.user) # here we open a new order for this user
            #     book_id = self.kwargs.get('book_id')
            #     book = Book.objects.get(Book, pk=book_id)
            #     user = self.request.user 
            #     order = Order.objects.create(user=user)
            #     order.books = order.add(book)
            #     order.save()
            #     serializer = self.serializer_classs(queryset=order,many=False) 
            #     serializer.save()
            #     return serializer.data
            # serializer.save(user=self.request.user)
            # old_order = get_object_or_404(Order,user=self.request.user)
            # old_books= old_order.books.all()
            # new_book = Book.objects.get(Book, pk=book_id)
            # books = old_books.add(new_book)
            # serializer.save(user=user, books=books)     # book.reviews_count+= 1
            # return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            # else:   #unique_together = ("user", "book") in models.Rview
            # raise validators.ValidationError({"IntegrityError": "This user already has order"},)