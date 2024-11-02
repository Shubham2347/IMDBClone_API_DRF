from django.urls import path,include
from watchlist_app.api.views import (WatchListAV, WatchDetailAV,StreamPlatformDetailAV,
                                    StreamPlatformListAV,ReviewList,ReviewDetail,ReviewCreate)

''' function based url
#from watchlist_app.api.views import movie_list,movie_detail
urlpatterns = [
    path("list/",movie_list,name="movie_list"),
    path("<int:pk>",movie_detail,name="movie_detail")
]
'''

#class based url
urlpatterns = [
    path("list/",WatchListAV.as_view(),name="watch_list"),
    path("<int:pk>", WatchDetailAV.as_view(),name="watch_detail"),
    path("stream/",StreamPlatformListAV.as_view(),name="stream_list"),
    path("stream/<int:pk>", StreamPlatformDetailAV.as_view(),name="stream_detail"),

    path("stream/<int:pk>/review-create",ReviewCreate.as_view(),name="review_create"),
    #review for perticular movie
    path("stream/<int:pk>/review",ReviewList.as_view(),name="review_list"),
    #review for individual
    path("stream/review/<int:pk>",ReviewDetail.as_view(),name="review_detail"),


]



