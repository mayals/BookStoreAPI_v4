from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Category, Publisher, Author, Tag, Review, Book
from rest_framework.validators import UniqueValidator
from . import validators as CustomValidator
from urllib.parse import urlparse

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100,required=True,validators=[UniqueValidator(queryset=Category.objects.all())])    
    books_category = serializers.SerializerMethodField
    
    def validate_name(self, value):
        if value is None:
            raise serializers.ValidationError("The category's name is required") 
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("The category name's must be unique")     
        print(value)
        return  value
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'created_at','books_category']
        extra_kwargs = {
                    'name' :  {'required' : True, 'unique':True},
                    'id'   :  {'read_only': True },
                    'slug' :  {'read_only': True },
                   'books_category':{'read_only':True},
        }

    def get_books_category(self, obj):
            books_category = Book.category.all().filter(category=self)
            return books_category




class PublisherSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100,required=True,validators=[UniqueValidator(queryset=Publisher.objects.all())] ) 
    social_twitter = serializers.URLField(required=False,validators=[CustomValidator.validate_hostname('twitter.com', 'www.twitter.com')])

    def validate_name(self, value):
        if value is None:
            raise serializers.ValidationError("The publisher's name is required") 
        if Publisher.objects.filter(name=value).exists():
            raise serializers.ValidationError("The publisher name's must be unique")     
        return  value
    
    def validate_social_twitter(self, value): 
        if value is not None:
            hostnames = set(hostnames)
            try:
                result = urlparse(value)
                if result.hostname not in hostnames:
                    serializers.ValidationError(f'The hostname {result.hostname} is not allowed.')
            except ValueError:
                raise serializers.ValidationError('invalid url')
        return  value       
        
    def validate_website(value):
        obj = urlparse(value)
        if 'com' not in obj.hostname or 'www' not in obj.hostname :   # url.hostname     "www.example.com"
            raise serializers.ValidationError('please enter valid website url')

    
    class Meta:
        model = Publisher
        fields = ['id','name', 'slug', 'address', 'website','social_twitter', 'created_at', 'updated_at']
        extra_kwargs = {
                    'id'   : {'read_only': True },
                    'name' : {'required' : True, 'unique':True},
                    'slug' : {'read_only': True },
                    'address' : {'required' : False },
                    'website' : {'required' : False },
                    'social_twitter' : {'required' : False },
                    # 'books': {'read_only': True },
        }      




  

class AuthorSerializer(serializers.ModelSerializer):
    full_name =serializers.CharField(max_length=200,required=True,validators=[UniqueValidator(queryset=Author.objects.all())] ) 

    class Meta:
        model = Author
        fields = ['id', 'full_name', 'slug', 'email', 'bio', 'pic', 'website', 'created_at', 'updated_at']
        extra_kwargs = {
                    'id'        : {'read_only': True },
                    'full_name' : {'required' : True, 'unique':True},
                    'slug'      : {'read_only': True },
                    'website'   : {'required' : False },
                    'email'     : {'required' : False },
                    'bio'       : {'required' : False },
                    'pic'       :  {'required' : False },
                    'books'     : {'read_only': True },
                    'social_twitter' : {'required' : False },
        } 

    def validate_full_name(self, value):
        if value is None:
            raise serializers.ValidationError("Author's full_name is required") 
        if Author.objects.filter(full_name=value).exists():
            raise serializers.ValidationError("Author's full_name must be unique")     
        print(value)
        return  value
    
    # def get_full_name(self, obj):
    #     return obj.get_author_fullname 




class TagSerializer(serializers.ModelSerializer):

    def validate_name(self, value):
        if value is None:
            raise serializers.ValidationError('The Tag field is required') 
        if Tag.objects.filter(name=value).exists():
            raise serializers.ValidationError("The tag name's must be unique")     
        print(value)
        return  value
      
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        extra_kwargs = {
                    'name' : {'required' : True},
                    'id'   : {'read_only': True },
                    'slug' : {'read_only': True },
        }
    








class BookSerializer(serializers.ModelSerializer):
    title      = serializers.CharField(max_length=200,required=True,validators=[UniqueValidator(queryset=Book.objects.all())] )
    # many to one field
    category   = serializers.StringRelatedField()  # to display category_id asredable  use name field  insead of id field                                                                                                           #   many books(ForignKey)  -  to   - one category(primary key)
    # many to many field
    publishers = PublisherSerializer(many=True, required=True) # Nested serialization
    authors    = AuthorSerializer(many=True, required=True) # Nested serialization
    tags       = TagSerializer(many=True, required=True)  # Nested serialization
    # related_field  read_only
    
    book_reviews    = serializers.SerializerMethodField # read_only field from another table Review
    reviews_count   = serializers.SerializerMethodField
    average_rating  = serializers.SerializerMethodField
    class Meta:
        model = Book
        fields = ['id', 'title', 'slug', 'category', 'publishers', 'authors', 'tags',
                  'ISBN','publish_date', 'num_pages', 'cover_image', 'page_image',
                  'condition', 'stock', 'created_at', 'updated_at', 'bookPrice',
                  'average_rating', 'reviews_count',
                  'book_reviews' # read_only field from another table Review
                ]
        extra_kwargs = {
                    'id'          : {'read_only': True },
                    'title'       : {'required' : True, 'unique':True},
                    
                    'category'    : {'required' : True },
                    
                    'authors'      : {'required' : True },
                    'tags'         : {'required' : True },
                    'publishers'   : {'required' : True },
                    
                    'cover_image' : {'required' : False},
                    'page_image'  : {'required' : False},
                    'book_reviews' : {'read_only': True }, # related_field
        } 

    #book_reviews  related_field  read_only
    @property
    def get_book_reviews(self):
        reviews = Review.objects.all().filter(book=self)
        return reviews
    
    @property
    def get_reviews_count(self):
        reviews_count = Review.objects.all().filter(book=self).count()
        return reviews_count

    



    
    # validate_field
    def validate_title(self, value):
        if value is None:
            raise serializers.ValidationError('The title field is required') 
        if Book.objects.filter(title=value).exists():
            raise serializers.ValidationError("The book's title must be unique")     
        print(value)
        return  value

    def validate_category(self, value):
        if value is None:
            raise serializers.ValidationError('The category field is required')     
        print(value)
        return  value
    
    def validate_authors(self, value):
        if value is None:
            raise serializers.ValidationError('The authors field is required')     
        print(value)
        return  value

    
    def validate_tags(self, value):
        if value is None:
            raise serializers.ValidationError('The tags field is required')     
        print(value)
        return  value

    
    def validate_publishers(self, value):
        if value is None:
            raise serializers.ValidationError('The publishers field is required')     
        print(value)
        return  value
    


    def create(self, validated_data):
        return validated_data
    
    # def create(self, validated_data):
    #     publishers_data = validated_data.pop('publishers')
    #     authors_data    = validated_data.pop('authors')
    #     tags_data       = validated_data.pop('tags')
        
    #     book = Book.objects.create(**validated_data)
    #     print(book)
    #     for publisher_data in publishers_data:
    #         publisher, created_publisher= Publisher.objects.get_or_create(**publisher_data)
    #         book.publishers.add(publisher)
    #         print(publishers_data)
           
    #     for author_data in authors_data:
    #         author, created_author= Author.objects.get_or_create(**author_data)
    #         book.authors.add(author)
    #         print(authors_data)

    #     for tag_data in tags_data:
    #         tag, created_tag= Tag.objects.get_or_create(**tag_data)
    #         book.tags.add(tag)
    #         print(tags_data)
    #     return book
    
    
    
    # def create(self, validated_data):
    #     publishers_data = validated_data.pop('publishers')
    #     book = Book.objects.create(**validated_data)
    #     for data in publishers_data:
    #         room, created = Rooms.objects.get_or_create(**data)
    #         module.rooms.add(room)
    #     return module
    
    


    # def create(self, validated_data): # work ok :)
    #     book = Book(
    #                 title       = validated_data.get('title') ,  # any title , must be unique
    #                 category    = validated_data.get('category') , # this field choicen from categories list 
    #                 publishers  = validated_data.get('publishers') ,  #  this field choicen from publishers list
    #                 tags        = validated_data.get('tags'),    #  this field choicen from tags list 
    #                 authors     = validated_data.get('authors'),   # this field choicen from likes list 
    #                 # author      = self.context.get('request').user, # username  get from username list  
    #     )
    #     book = super().create(validated_data)
    #     return book
                    

    # def create(self, validated_data):
    #     publishers_data = validated_data.pop('publishers')
    #     authors_data = validated_data.pop('authors')
    #     tags_data = validated_data.pop('tags')
        
    #     book = Book.objects.create(**validated_data)
        
    #     for publisher_data in publishers_data:
    #         Book.objects.create(book=book, **publisher_data)
        
    #     for author_data in authors_data:
    #         Book.objects.create(book=book, **author_data)
        
    #     for tag_data in tags_data:
    #         Book.objects.create(book=book, **tag_data)
    #     return book




class ReviewSerializer(serializers.ModelSerializer):
    user  = serializers.StringRelatedField()  #  many reviews (ForignKey) -  to   - one user (primary key)
    book  = serializers.StringRelatedField()  #  many reviews (ForignKey) -  to   - one book (primary key)  
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating_value', 'rating_text', 'created_at', 'updated_at']
        

