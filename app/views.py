from django.shortcuts import render

# Create your views here.
from  rest_framework.decorators import  api_view
from django.utils import timezone
from  rest_framework.response import  Response 

from .models import *
from .serializers import *

@api_view(['POST'])
def sign_up(request):
    response = {}
    try:

        email = request.data.get('email')
        password = request.data.get('password')
        organization = request.data.get('organization_name')

        role_name = 'Owner'
    except Exception as e:
        response['message'] = "Not a valid request"
        response['status'] = 400
        return Response(response)

    try:
        user = User.objects.create(email=email, password=password)
        organization = Organization.objects.create(name=organization)
        role , created =  Role.objects.get_or_create(name=role_name)
        Member.objects.create(user = user , organization = organization , role =role)

        response['message'] = "User created successfully"
        response['status'] = 200
        return Response(response)
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 500
        return Response(response)
        


@api_view(['POST'])
def sign_in(request):
    response = {}
    try:
        email = request.data.get('email')
        password = request.data.get('password')
    except Exception as e:
        response['message'] = "Not a valid request"
        response['status'] = 400
        return Response(response)
    
    try:
        user = User.objects.get(email=email, password=password)
        user.last_login_time = timezone.now()
        user.save()
        response['message'] = "User login successfully"
        response['status'] = 200
        return Response(response)
    except User.DoesNotExist:
        response['message'] = "Invalid credentials"
        response['status'] = 401
        return Response(response)
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 500
        return Response(response)
    
       


@api_view(['POST'])
def reset_password(request):
    response = {}
    try:
        email = request.data.get('email')
        new_password = request.data.get('new_password')
    except Exception as e:
        response['message'] = "Not a valid request"
        response['status'] = 400
        return Response(response)
    
    try:
        user = User.objects.get(email=email)
        user.password = new_password
        user.save()
        response['message'] = "Password reset successfully"
        response['status'] = 200
        return Response(response)
    except User.DoesNotExist:
        response['message'] = "User not found"
        response['status'] = 404
        return Response(response)
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 500
        return Response(response)




@api_view(['POST'])
def invite_member(request):
    response = {}
    try:
        email = request.data.get('email')
        organization_id = request.data.get('organization_id')
        role_name = request.data.get('role_name')
    except Exception as e:
        response['message'] = "Not a valid request"
        response['status'] = 400
        return Response(response)
    
    try:
        organization = Organization.objects.get(id=organization_id)
        role , created =  Role.objects.get_or_create(name=role_name)

        # user_email = Member.objects.filter()
        
        user , created  = User.objects.get_or_create(email= email , defaults= {'password': 'defaultpassword'})
        Member.objects.create(user = user , organization = organization , role =role)

        response['message'] = "Member invited successfully"
        response['status'] = 200
        return Response(response)
    except Organization.DoesNotExist:
        response['message'] = "Organization not found"
        response['status'] = 404
        return Response(response)
    except Role.DoesNotExist:
        response['message'] = "Role not found"
        response['status'] = 404
        return Response(response)
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 500
        return Response(response)
    

@api_view(['DELETE'])
def delete_member(request , member_id):
    response = {}
    try:
        member = Member.objects.get(id=member_id)
        member.delete()
        response['message'] = "Member deleted successfully"
        response['status'] = 200
        return Response(response)
    except Member.DoesNotExist:
        response['message'] = "Member not found"
        response['status'] = 404
        return Response(response)
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 500
        return Response(response)
    


@api_view(['PUT'])
def update_member(request, member_id):
    response = {}
    new_role = request.data.get('new_role')
    try:
        member = Member.objects.get(id=member_id)
        role , created =  Role.objects.get_or_create(name=new_role)
        member.role = role
        member.save()
        response['message'] = "Member updated successfully"
        response['status'] = 200
        return Response(response)
    
    except Member.DoesNotExist:
        response['message'] = "Member not found"
        response['status'] = 404
        return Response(response)
    except Role.DoesNotExist:
        response['message'] = "Role not found"
        response['status'] = 404
        return Response(response)
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 500
        return Response(response)
    
       

@api_view(['GET'])
def role_wise_number_of_users(request):
    response = {}
    try:
        roles = Role.objects.all()
        data = {}
        for role in roles:
            count = Member.objects.filter(role=role).count()
            data[role.name] = count
        response['data'] = data
        response['message'] = "Role wise number of users"
        response['status'] = 200
        return Response(response)
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 500
        return Response(response)
    


@api_view(['GET'])
def  organization_wise_number_of_members(request):
    response = {}
    try:
        organizations = Organization.objects.all()
        data = {}
        for organization in organizations:
            count = Member.objects.filter(organization=organization).count()
            data[organization.name] = count
        response['data'] = data
        response['message'] = "Organization wise number of members"
        response['status'] = 200
        return Response(response)
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 500
        return Response(response)


@api_view(['GET'])
def orgranisation_wise_role_number_of_users(request):
    response = {}
    try:
        from_time = request.query_params.get('from_time')
        to_time = request.query_params.get('to_time')
        status_filter = request.query_params.get('status')
        organizations = Organization.objects.all()
        data = {}
        for organization in organizations:
            roles = Role.objects.all()
            organization_data = {}
            for role in roles:
                members = Member.objects.filter(organization=organization, role=role)
                if from_time and to_time:
                    members = members.filter(added_at__range = [from_time, to_time])
                if status_filter:
                    members = members.filter(use__is_active=status_filter)


                organization_data[role.name] = members.count()
            data[organization.name] = organization_data
        response['data'] = data
        response['message'] = "Organisation wise role wise number of users"
        response['status'] = 200
        return Response(response)
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 500
        return Response(response)
    
    