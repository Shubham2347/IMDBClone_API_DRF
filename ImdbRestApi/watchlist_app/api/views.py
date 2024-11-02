from django.shortcuts import render
from rest_framework.response import Response
from watchlist_app.models import WatchList,StreamPlatform,Review
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import AdminOrReadOnly,ReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle

from django_filters.rest_framework import DjangoFilterBackend

# watchlist api crud
class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request):
        movies=WatchList.objects.all()
        serializer=WatchListSerializer(movies,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer=WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request,pk):
        try:
            movies=WatchList.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer=WatchListSerializer(movies)
        return Response(serializer.data)
    
    def put(self,request,pk):
        movies=WatchList.objects.get(pk=pk)
        serializer=WatchListSerializer(movies,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        movies=WatchList.objects.get(pk=pk)
        movies.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#streamplatform api crud -->      notimp modelviewset and router refer notebook
class StreamPlatformListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request):
        platform=StreamPlatform.objects.all()
        serializer=StreamPlatformSerializer(platform,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer=StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request,pk):
        try:
            platform=StreamPlatform.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer=StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self,request,pk):
        platform=StreamPlatform.objects.get(pk=pk)
        serializer=StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        platform=StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Review Api -->  using concrete class view --- (type-5 view)


class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class=ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk=self.kwargs.get("pk")
        movie=WatchList.objects.get(pk=pk)

        # User Update
        review_user=self.request.user
        review_querset=Review.objects.filter(watchlist=movie,review_user=review_user)
        if review_querset.exists():
            raise ValidationError("you have already reviewed this movie")
        
        #custom calculation permission
        if movie.number_rating==0:
            movie.avg_rating=serializer.validated_data['rating']
        else:
            movie.avg_rating=(movie.avg_rating+serializer.validated_data['rating'])/2
        movie.number_rating=movie.number_rating+1
        movie.save()
        serializer.save(watchlist=movie,review_user=review_user)

class ReviewList(generics.ListCreateAPIView):
    # queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    # object level permisions
    # permission_classes=[IsAuthenticatedOrReadOnly]
    throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer    
      # object level permisions
    permission_classes=[IsAuthenticated]
    # permission_classes=[AdminOrReadOnly]

    #custom permission
    # permission_classes=[ReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope='review-detail'



















# Review Api -->  using generic api and mixin
'''
class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class=ReviewSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class=ReviewSerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

'''







    #BEFORE UPDATING MODELS VIEW is class based
'''
    class MovieListAV(APIView):
    def get(self, request):
        movies=Movie.objects.all()
        serializer=MovieSerializer(movies,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer=MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class MovieDetailAV(APIView):
    def get(self, request,pk):
        movies=Movie.objects.get(pk=pk)
        serializer=MovieSerializer(movies)
        return Response(serializer.data)
    
    def put(self,request,pk):
        movies=Movie.objects.get(pk=pk)
        serializer=MovieSerializer(movies,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        movies=Movie.objects.get(pk=pk)
        movies.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    '''








# function based type1
'''
from rest_framework.decorators import api_view
@api_view(['GET','POST'])
def movie_list(request):
    if request.method == 'GET':
        movies=Movie.objects.all()
        serializer=MovieSerializer(movies,many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':    
        serializer=MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        

@api_view(['GET','PUT','DELETE'])
def movie_detail(request,pk):
    if request.method=='GET':
        movies=Movie.objects.get(pk=pk)
        serializer=MovieSerializer(movies)
        return Response(serializer.data)
    
    if request.method=='PUT':
        try:
            movies=Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'Error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)    
        serializer=MovieSerializer(movies,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        
    if request.method=='DELETE':    
        movies=Movie.objects.get(pk=pk)
        movies.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''