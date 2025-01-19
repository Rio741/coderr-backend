from django.urls import path
from .views import RegistrationView, CustomLoginView, UserProfileDetailView, BusinessProfilesListView, CustomerProfilesListView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/business/', BusinessProfilesListView.as_view(), name='business-profiles'),
    path('profiles/customer/', CustomerProfilesListView.as_view(), name='customer-profiles'),
]