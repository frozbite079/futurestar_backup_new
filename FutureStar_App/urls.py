"""FutureStar_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *
from django.conf.urls import handler404

# handler404 = 'FutureStar_App.views.custom_404_view'


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('user/<int:pk>/toggle-status/', ToggleUserStatusView.as_view(), name='user_toggle_status'),
    path('user_profile/',UserProfileView.as_view(),name='user_profile'),
    path('edit_profile/', UserUpdateProfileView.as_view(), name='edit_profile'),
    # path('change_password/', ChangePasswordView.as_view(), name='change_password'),

    path('roles/', RoleListView.as_view(), name='role_list'),
    path('roles/create/', RoleCreateView.as_view(), name='role_create'),
    path('roles/update/<int:pk>/', RoleUpdateView.as_view(), name='role_update'),
    path('roles/delete/<int:pk>/', RoleDeleteView.as_view(), name='role_delete'),

    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),

    path('system-settings/', System_Settings.as_view(),name="system_settings"),


    #error
    path('error/', ErrorView.as_view(), name='error'),

    path('home/', Dashboard.as_view(),name="home"),


#Gender Role URL
    path('gender/', GenderListView.as_view(), name='gender_list'),
    path('gender/create/', GenderCreateView.as_view(), name='gender_create'),
    path('gender/update/<int:pk>/', GenderUpdateView.as_view(), name='gender_update'),
    path('gender/delete/<int:pk>/', GenderDeleteView.as_view(), name='gender_delete'),


    # GameType URL
    path('gametype/', GameTypeListView.as_view(), name='gametype_list'),
    path('gametype/create/', GameTypeCreateView.as_view(), name='gametype_create'),
    path('gametype/update/<int:pk>/', GameTypeUpdateView.as_view(), name='gametype_update'),
    path('gametype/delete/<int:pk>/', GameTypeDeleteView.as_view(), name='gametype_delete'),

    # FieldCapacity URL
    path('fieldcapacity/', FieldCapacityListView.as_view(), name='fieldcapacity_list'),
    path('fieldcapacity/create/', FieldCapacityCreateView.as_view(), name='fieldcapacity_create'),
    path('fieldcapacity/update/<int:pk>/', FieldCapacityUpdateView.as_view(), name='fieldcapacity_update'),
    path('fieldcapacity/delete/<int:pk>/', FieldCapacityDeleteView.as_view(), name='fieldcapacity_delete'),

    # Ground Materials URL
    path('groundmaterial/', GroundMaterialListView.as_view(), name='groundmaterial_list'),
    path('groundmaterial/create/', GroundMaterialCreateView.as_view(), name='groundmaterial_create'),
    path('groundmaterial/update/<int:pk>/', GroundMaterialUpdateView.as_view(), name='groundmaterial_update'),
    path('groundmaterial/delete/<int:pk>/', GroundMaterialDeleteView.as_view(), name='groundmaterial_delete'),

    # Tournament Style URL
    path('tournamentstyle/', TournamentStyleListView.as_view(), name='tournamentstyle_list'),
    path('tournamentstyle/create/', TournamentStyleCreateView.as_view(), name='tournamentstyle_create'),
    path('tournamentstyle/update/<int:pk>/', TournamentStyleUpdateView.as_view(), name='tournamentstyle_update'),
    path('tournamentstyle/delete/<int:pk>/', TournamentStyleDeleteView.as_view(), name='tournamentstyle_delete'),

    # Event Type URL
    path('eventtype/', EventTypeListView.as_view(), name='eventtype_list'),
    path('eventtype/create/', EventTypeCreateView.as_view(), name='eventtype_create'),
    path('eventtype/update/<int:pk>/', EventTypeUpdateView.as_view(), name='eventtype_update'),
    path('eventtype/delete/<int:pk>/', EventTypeDeleteView.as_view(), name='eventtype_delete'),





]
