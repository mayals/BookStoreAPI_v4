import django_filters
from .models import Book 

class BookFilter(django_filters.FilterSet):
    '''Customize filter to allow any Caps'''
    category_name = django_filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    
    class Meta:
        model = Book 
        fields = ['category_name', 'ISBN', 'title','publishers',
                  'authors', 'tags', 'average_rating', 'publish_date',
                  'num_pages', 'condition', 'stock', 'created_at', 'updated_at'
        ]

       