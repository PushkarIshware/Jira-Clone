from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, SigninSerializer, ProfileSerializer, ProfileUpdateSerializer
from django.contrib.auth import authenticate
import jwt
from django.conf import settings
from aub_jira.permissions import CustomJWTTokenAuthentication

# User = get_user_model()

def get_generic_response():
    
    response = {
        'status_code': 200,
        'error': '',
        'message': '',
        'data': '',
    }
    return response

class RegisterUser(APIView):
    def post(self, request):
        response = get_generic_response()

        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response['message'] = "Account created successfully. Please Signin."
            response['status_code'] = status.HTTP_201_CREATED
            return JsonResponse(response)
        response['message'] = "error occured during creating new user"
        response['status_code'] = status.HTTP_302_FOUND
        response['error'] = serializer.errors
        return JsonResponse(response)
    

class LoginUser(APIView):
    def post(self, request):
        response = get_generic_response()

        serializer = SigninSerializer(data=request.data)

        if serializer.is_valid():

            user = authenticate(username=str(serializer.validated_data['email']), password=str(serializer.validated_data['password']))
            
            if user and user.is_active:
                payload = {'email': serializer.validated_data['email']}
                
                jwt_token = jwt.encode(payload, settings.JWT_TOKEN_SECRET_NAME, algorithm=settings.JWT_TOKEN_ALGORITHM)

                response['message'] = "Here is your Token"
                response['status_code'] = status.HTTP_201_CREATED
                response['data'] = jwt_token
                return JsonResponse(response)
        else:
            response['message'] = "Invalid email/password"
            response['status_code'] = status.HTTP_404_NOT_FOUND
            return JsonResponse(response)
        

class UserProfile(APIView):
    permission_classes = [CustomJWTTokenAuthentication, ]
    
    def get(self, request):

        response = get_generic_response()

        serializer = ProfileSerializer(request.user)
        response['status_code'] = status.HTTP_200_OK
        response['message'] = "profile fetched successfully"
        response['data'] = serializer.data
        return JsonResponse(response)

class UpdateProfile(APIView):

    permission_classes = [CustomJWTTokenAuthentication, ]

    def patch(self, request):
        response = get_generic_response()

        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response['message'] = "Profile updated"
            response['status_code'] = status.HTTP_200_OK
            return JsonResponse(response)
        response['message'] = "something went wrong"
        response['status_code'] = status.HTTP_404_NOT_FOUND
        response['error'] = serializer.errors
        return JsonResponse(response)