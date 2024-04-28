from django.urls import path
from rest_framework.routers import DefaultRouter
from ecommerce import views



# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('orders', views.OrderViewSet, basename="orders")     # Order  


# https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#binding-viewsets-to-urls-explicitly
order_detail = views.OrderViewSet.as_view({
                                            'get': 'retrieve',
                                            'put': 'update',
                                            'patch': 'partial_update',
                                            'delete': 'destroy'
})


urlpatterns =  router.urls  + [
    # Order Endpoints:
    path('orders/orders/create_order/', views.create_order, name="create-order"),
    path('orders/orders/',views.OrderViewSet.as_view({'get': 'list'}), name='orders-list'),
    path('orders/orders/<str:id>/', order_detail, name='orders-detail'),   #name=basename-detail
    path('orders/orders/<str:id>/update_status/', views.update_order_status, name='update-order-status'), 
    
    # OrderBook Endpoints
    path('orderbooks_view/', views.orderbooks_view, name='orderbooks_view'), 
   
    # payment
    path('pay/', views.StripeView.as_view(), name='pay'),
   


    #('orders/<str:book_id>/create_order/', views.OrderCreateAPIView.as_view(), name="create_order"),
    # path('ordrs/orders/<int:id>/cancel/', views.ReviewRetrieveUpdateDestroyAPIView.as_view(),name='retrieve-update-destroy-review'),
    # Cart and Checkout Endpoints:
    # /cart/add
    # /cart
    # /cart/update/{cart_item_id}
    # /cart/remove/{cart_item_id}
    # /checkout
    
]


