from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from api.views import *

router = SimpleRouter()
router.register(r'gitlink', GitGiveLinkView, basename='gitlink')
router.register(r'gitgetall', GitGetAllView, basename='gitgetall')
router.register(r'gitcreate', GitCreateView, basename='gitcreate')
router.register(r'gitcreateuser', GitCreateUser, basename='gitcreateuser')
router.register(r'scrapycreate', GitCreateForApi, basename='scrapycreate')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gitoveral/', GitOverallStatView.as_view(), name='gitoveral'),
    path('gitindividualstats/<int:pk>/', GitIndividualStatView.as_view(), name='gitindividualstats'),
    path('gitgetrep/<int:pk>/', GitGetRepView.as_view(), name='gitgetrep')
]

urlpatterns += router.urls
