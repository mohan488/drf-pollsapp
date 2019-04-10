from django.urls import path
# from pollsapp import routers

from . import views
# from . import api

# router = routers.SharedAPIRootRouter()
# router.register(r'questions', api.QuesViewSet)
# router.register(r'choices', api.ChoiceViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('track/<int:idTrack>/', views.trackResource.as_view(), name='track_resource'),
    path('track/', views.trackCollection.as_view(), name='track_collection'),
    path('question/<int:idTrack>/', views.questionResource.as_view(), name='question_resource'),
    path('choice/<int:idChoice>/', views.choiceResource.as_view(), name='choice_resource'),
    path('count/<int:idQuestion>/', views.choiceCountResource.as_view(), name='choice_count_resource')
]
