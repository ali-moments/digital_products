from django.urls import path

from .views import home_page, package_detail

urlpatterns = [
    path('', home_page, name='home page'),
    path('packages/<int:package_id>/', package_detail, name='package details'),
]