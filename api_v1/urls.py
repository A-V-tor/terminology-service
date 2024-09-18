from django.urls import path

from .routes import AllHandBookAPI, CheckElementAPI, HandBookElementListAPI

urlpatterns = [
    path('refbooks/', AllHandBookAPI.as_view(), name='all_handbooks'),
    path(
        'refbooks/<int:id>/elements/',
        HandBookElementListAPI.as_view(),
        name='elements',
    ),
    path(
        'refbooks/<int:id>/check_element/',
        CheckElementAPI.as_view(),
        name='check_element',
    ),
]
