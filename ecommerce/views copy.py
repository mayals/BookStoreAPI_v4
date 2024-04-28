from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics, response, status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from .models import Order, OrderBook
from book.models import Book
from .serializers import OrderSerializer,OrderBookSerializer


########################################## Order ######################################################
# POST
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data 
    orderbooks = request.data['orderbooks']
    if orderbooks and len(orderbooks) == 0:
        return response.Response({'error': 'No order recieved'},status=status.HTTP_400_BAD_REQUEST)
    else:   
        total_amount = sum(float(item['price']) * int(item['quantity']) for item in orderbooks)
        order = Order.objects.create(
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
        for item in orderbooks:
                    print('item ='+str(item))
                    book = Book.objects.get(id = item['book']) # 'book'=  value of book id come from related field orderbooks that come from OrderBook model
                    book_title = book.title 
                    orderbook = OrderBook.objects.create(
                                                        book= book,
                                                        order = order, # the order we created above 
                                                        quantity = item['quantity'],# 'quantity'=  value of quantity come from related field orderbooks that come from OrderBook model
                                                        price = item['price'],# 'price'=  value of 'price' come from related field orderbooks that come from OrderBook model
                                                        book_title = book_title
                    )
        serializer = OrderSerializer(order, many=False)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)



# 'get': 'list'
# 'get': 'retrieve',
# 'put': 'update',                                         
# 'patch': 'partial_update',                                       
# 'delete': 'destroy'                                    
class OrderViewSet(viewsets.ModelViewSet):
    queryset= Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
 




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