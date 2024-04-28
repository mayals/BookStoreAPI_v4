from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework import viewsets, mixins, permissions, generics, response, status, validators
from .models import Category,Publisher,Author,Tag,Review,Book
from .serializers import CategorySerializer,PublisherSerializer,AuthorSerializer,TagSerializer,ReviewSerializer,BookSerializer
from common import permissions as custom_permissions
#https://www.django-rest-framework.org/api-guide/viewsets/#custom-viewset-base-classes
from django_auto_prefetching import AutoPrefetchViewSetMixin

# Not: category have no permission for update
class CategoryViewSet(viewsets.mixins.CreateModelMixin, mixins.ListModelMixin, 
                      mixins.RetrieveModelMixin,mixins.DestroyModelMixin, viewsets.GenericViewSet):                      
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug' 

    def get_permissions(self):
        if self.action in["create","destroy"]:
            self.permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]   
        else:
            self.permission_classes = [permissions.IsAuthenticated]       
        return super().get_permissions()



class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug' 

    def get_permissions(self):
        if self.action in["create","destroy"]:
            self.permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]   
        else:
            self.permission_classes = [permissions.IsAuthenticated]       
        return super().get_permissions()




class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            self.permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]   
        else:
            self.permission_classes = [permissions.IsAuthenticated]       
        return super().get_permissions()    



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug' 

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            self.permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]   
        else:
            self.permission_classes = [permissions.IsAuthenticated]       
        return super().get_permissions()

 


# https://docs.djangoproject.com/en/4.2/topics/db/models/#extra-fields-on-many-to-many-relationships
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug' 
    
    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            self.permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]   
        else:
            self.permission_classes = [permissions.IsAuthenticated]       
        return super().get_permissions()

    def get_serializer_class(self):
          self.serializer_class = BookSerializer 
          return super().get_serializer_class()
    

    # Important NOTE we must write create function because we must add the the data that insert in the fields:
    # of types ForeignKey field and ManyToManyField  :
    # 'category' , 'publishers' , 'authors' and 'tags'
    # without this create function inside BookViewSet these fields remain empty ! 
    
  
    """
    # in postman we must POST data when send request as this mannar :
    {
    "title": "gggggg666",
    "category": "english drama",
    "publishers": ["china publisher","uae publisher"],
    "authors": ["ali nasir"],
    "tags": ["home tag"]
    }
    """


    def create(self,request,*args, **kwargs):
        data = request.data
        # print(data) 
        print(data['title'])
        if data['title'] == "" or data['category']  == "" or data['publishers']  == "" or data['authors']  == "" or data['tags'] == "" :
            print(data['title'])
            return response.Response({"error": "the fields : ( title - category - publishers - authors - tags ) are required"})
    
        title = data.get('title')
        if  Book.objects.filter(title=title).exists():
            return response.Response({"error":"The book's title must be unique"})
        
        # this for create book with only title field
        new_book = Book.objects.create(title= data.get('title'))
        new_book.save()
        print('new_book='+ str(new_book))
    
         # adding  the content of category field content
        category = data.get('category')
        cat_name = data.get('category',[])        #string
        print('cat_name='+ str(type(cat_name)))   # string 
        print('cat_name='+ str(cat_name))
        category_obj = Category.objects.get(name= cat_name) #obj # get category object from its name
        print('category_obj='+ str(category_obj))
        new_book.category = category_obj 
        new_book.save()
        print('new_book.category='+ str(new_book.category))

        # adding the content of publishers field
        publishers = data.get('publishers')    
        publishers_names = request.data.get('publishers',[])
        print('publishers_names='+ str(publishers_names))    
        print('publishers_names='+ str(type(publishers_names)))    # list of name strings      
        if publishers_names : # list of publishers names strings ['strnamepub1','strnamepub2','',...]
            for item in publishers_names: # loop on list to took the names
                print('item='+ str(item))           
                publisher_obj = Publisher.objects.get(name=item) # get object by its name
                new_book.publishers.add(publisher_obj) #add object 
        new_book.save()
                    
        # adding the content of authors field
        authors = data.get('authors')        
        authors_full_names = request.data.get('authors',[])
        print('authors_full_names='+ str(authors_full_names))    
        print('authors_full_names='+ str(type(authors_full_names)))     # string       
        if authors_full_names:
            for item in authors_full_names:
                print('item='+ str(item))   
                author_obj = Author.objects.get(full_name=item)
                # print('author_obj='+ str(author_obj))
                new_book.authors.add(author_obj)
        new_book.save()


        # adding the content of tags field                        
        tags = data.get('tags')
        tags_names = request.data.get('tags')
        print('tags_names='+ str(tags_names))    
        print('tags_names='+ str(type(tags_names)))     # string       
        if tags_names:
            for item in tags_names:
                print('item='+ str(item))   
                tag_obj = Tag.objects.get(name=item)
                # print('tag_obj='+ str(tag_obj))
                new_book.tags.add(tag_obj)
        new_book.save()
        
        serializer = BookSerializer(new_book)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
# else:        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       

   

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance_obj = self.get_object()
        #serializer = self.get_serializer(data=request.data)
        input_data = request.data
        data = input_data
        # if not serializer.is_valid(): not work because
        # return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        print(data['title'])
        if data['title'] == "" or data['category']  == "" or data['publishers']  == "" or data['authors']  == "" or data['tags'] == "" :
            print(data['title'])
            return response.Response({"error": "the fields : ( title - category - publishers - authors - tags ) are required"})
    
        title = data.get('title')
        if  Book.objects.filter(title=title).exists():
            return response.Response({"error":"The book's title must be unique"})
        istance_title = instance_obj.title
        updated_title = data.get('title', istance_title)
        
        updated_book = Book.objects.create(title = updated_title)
        
        # modify updated_category_object
        istance_category_name = instance_obj.category.name
        print('istance_category_name='+ str(istance_category_name))
        print('istance_category_name type='+ str(type(istance_category_name)))  #str
        print("hiii")
        updated_category_name = data.get('category', istance_category_name)
        updated_category_object = Category.objects.get(name= updated_category_name)
        print('updated_category_object='+ str(updated_category_object))
        print('updated_category_object type='+ str(type(updated_category_object))) #obj
        updated_book.category = updated_category_object
        
        # modify updated_publishers_object
        list_instance_publishers_names = instance_obj.publishers
        print('list_instance_objects_names='+ str(list_instance_publishers_names))
        print('list_instance_objects_names type='+ str(type(list_instance_publishers_names)))
        publishers_names = request.data.get('publishers',list_instance_publishers_names)
        print('publishers_names='+ str(publishers_names))    
        print('publishers_names='+ str(type(publishers_names)))    # list of name strings      
        # list of publishers names strings ['strnamepub1','strnamepub2','',...]
        for item in publishers_names: # loop on list to took the names
            print('item='+ str(item))           
            publisher_obj = Publisher.objects.get(name=item) # get object by its name
            updated_book.publishers.add(publisher_obj) #add object 
        updated_book.save()    
        
        # modify updated_authors_object
        list_instance_authors_names = instance_obj.authors
        print('list_instance_authors_names='+ str(list_instance_authors_names))
        print('list_instance_authors_names type='+ str(type(list_instance_authors_names)))
        authors_names = request.data.get('authors',list_instance_authors_names)
        print('publishers_names='+ str(authors_names))    
        print('publishers_names='+ str(type(authors_names)))    # list of name strings      
        # list of authors names strings ['strnamepub1','strnamepub2','',...]
        for item in authors_names: # loop on list to took the names
            print('item='+ str(item))           
            authors_obj = Author.objects.get(full_name=item) # get object by its name
            updated_book.authors.add(authors_obj) #add object 
        updated_book.save()

        # modify updated_authors_object
        list_instance_tags_names = instance_obj.tags
        print('list_instance_tags_names='+ str( list_instance_tags_names))
        print('list_instance_tags_names type='+ str(type( list_instance_tags_names)))
        tags_names = request.data.get('tags',list_instance_tags_names)
        print('tags_names='+ str(tags_names))    
        print('tags_names='+ str(type(tags_names)))    # list of name strings      
        # list of publishers names strings ['strnamepub1','strnamepub2','',...]
        for item in tags_names: # loop on list to took the names
            print('item='+ str(item))           
            tags_obj = Tag.objects.get(name=item) # get object by its name
            updated_book.tags.add(tags_obj) #add object 
        updated_book.save()
        # save updated book  obj
        updated_book.save()
        serializer = BookSerializer(updated_book)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


        # # print("kwargs="+str(kwargs))
        # partial = kwargs.pop('partial', False)
        # print("partial="+str(partial))
        # instance = self.get_object()
        # print("instance="+str(instance))
        # serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)

        # if getattr(instance, '_prefetched_objects_cache', None):
        #     # If 'prefetch_related' has been applied to a queryset, we need to
        #     # forcibly invalidate the prefetch cache on the instance.
        #     instance._prefetched_objects_cache = {}

        # return response.Response(serializer.data)







class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Ensure a user makes only ony one review per course
            book_slug = self.kwargs["slug"]
            book = get_object_or_404(Book, slug=book_slug)
            user = self.request.user
            if not Review.objects.filter(book=book,user=self.request.user).exists():    
                serializer.save(book=book, user=self.request.user)
                # book.reviews_count+= 1
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            else:   #unique_together = ("user", "book") in models.Rview
                raise validators.ValidationError({"IntegrityError": "This user has already created a review about this book"},)




class ReviewListAPIView(AutoPrefetchViewSetMixin, generics.ListAPIView):
    serializer_class = ReviewSerializer 
    queryset = Review.objects.all()
    permission_classes = [custom_permissions.IsReviewCreatorOrReadOnly]
    
    # pagination_class = CustomPagination 
    # renderer_classes = [CustomRenderer]
    
    def get_queryset(self):
        slug = self.kwargs["slug"]
        print(super().get_queryset().filter(user__is_active=True, book__slug=self.kwargs["slug"]))
        return super().get_queryset().filter(user__is_active=True, book__slug=self.kwargs["slug"])





class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_permissions(self):
        if self.action in ['update','partial_update','destroy']:
            self.permission_classes = [permissions.IsAuthenticated,custom_permissions.IsCreatorOrReadOnly]   
        else:
            self.permission_classes = [permissions.IsAuthenticated]       
        return super().get_permissions()
    

    def get_object(self):
        id = self.kwargs["id"]
        obj = get_object_or_404(Review, id=id)
        self.check_object_permissions(self.request,obj)
        return obj 





    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}

    #     return response.Response(serializer.data, status=status.HTTP_201_CREATED)                                        
                                            
                                           


# class ReviewViewSet(viewsets.ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'id' 

#     def get_serializer_class(self):
#           self.serializer_class = ReviewSerializer 
#           return super().get_serializer_class()
    # def get_permissions(self):
    #     if self.action in ['create','update','partial_update','destroy']:
    #         self.permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]   
    #     else:
    #         self.permission_classes = [permissions.IsAuthenticated]       
    #     return super().get_permissions()

    

    # def perform_create(self, serializer): 
    #     user = self.request.user 
    #     book = self.kwargs.get('course_pk')
    #     serializer.save(user=user,book=book) 
