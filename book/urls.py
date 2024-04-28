from django.urls import path
from rest_framework.routers import DefaultRouter
from book import views



# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename="categories")     # Category  
router.register('publishers', views.PublisherViewSet, basename="publishers")    # Publisher 
router.register('authors', views.AuthorViewSet, basename="authors")             # Author
router.register('tags', views.TagViewSet, basename="tags")                      # Tags
router.register('books', views.BookViewSet, basename="books")                   # Book
# router.register('reviews', views.ReviewViewSet, basename="reviews")           # Review

# The API URLs are now determined automatically by the router.
urlpatterns =  router.urls  + [
    path('books/categories/<str:slug>/', views.CategoryViewSet.as_view({'get': 'retrieve'}, name='book:categories-detail')), #name=basename-detail
    path('books/publishers/<str:slug>/', views.PublisherViewSet.as_view({'get': 'retrieve'}, name='book:publishers-detail')),  #name=basename-detail
    path('books/authors/<str:slug>/', views.AuthorViewSet.as_view({'get': 'retrieve'}, name='book:authors-detail')),  #name=basename-detail
    path('books/tags/<str:slug>/', views.TagViewSet.as_view({'get': 'retrieve'}, name='book:tags-detail')),  #name=basename-detail
    path('books/books/<str:slug>/', views.BookViewSet.as_view({'get': 'retrieve'}, name='book:books-detail')),  
    #Review
    path("books/books/<str:slug>/create-review/", views.ReviewCreateAPIView.as_view(), name="book-create-review"),
    path("books/books/<str:slug>/reviews/", views.ReviewListAPIView.as_view(), name="book-reviews-list"),
    path('books/reviews/<int:id>/', views.ReviewRetrieveUpdateDestroyAPIView.as_view(),name='retrieve-update-destroy-review'), 
    # path("review/<int:id>/", views.ReviewViewSet.as_view({'get': 'retrieve'}), name="book:review-detail"),
]


