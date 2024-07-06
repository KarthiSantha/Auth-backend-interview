from django.urls import path
from .views import *

urlpatterns = [
    
    path('signup/' , sign_up , name= 'signup'),
    path('login/' , sign_in , name= 'login'),
    path('reset_password/' , reset_password , name= 'reset_password'),
    path('invite_member/' , invite_member , name= 'invite_member'),
    path('delete_member/<int:member_id>/' , delete_member , name= 'delete_member'),
    path('update_member/<int:member_id>/' , update_member , name= 'update_member'),
    path('role_wise_number_of_users/' , role_wise_number_of_users , name= 'role_wise_number_of_users'),


    path('organization_wise_number_of_members/' , organization_wise_number_of_members , name= 'logout'),
    path('orgranisation_wise_role_number_of_users/' , orgranisation_wise_role_number_of_users , name= 'logout'),

]

