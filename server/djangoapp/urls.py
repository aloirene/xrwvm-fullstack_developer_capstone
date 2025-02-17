from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('register/', views.registration, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_request, name='logout'),

    # ✅ Fetch dealerships
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>/', views.get_dealerships, name='get_dealers_by_state'),

    # ✅ Fetch cars
    path('get_cars/', views.get_cars, name='get_cars'),

    # ✅ Fetch specific dealer details
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='get_dealer_details'),

    # ✅ Fetch dealer reviews
    path('dealer/<int:dealer_id>/reviews/', views.get_dealer_reviews, name='get_dealer_reviews'),

    # ✅ Insert a new review
    path('add_review/', views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)