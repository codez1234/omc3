
from distutils import text_file
# from ipaddress import ip_address
from urllib import request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets

from account.models import User
from database.models import TblUserDevices, TblUserSites

from account.phone_number_validation import check_phone_number
from account.serializers import *
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from modules.createOrWriteTextFile import request_text_file, response_text_file
from modules.errors import messages
from modules.deviceCheck import check_device
from django.shortcuts import get_object_or_404


# ++++++++++++++++++++++++++++++++++++++++ #

# ++++++++++++++++++++++++++++++++++++++++++++++++ #


# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        # print(request.user)
        request_text_file(user=request.user.id, value=request.data)
        email_or_phone = request.data.get("email_or_phone")
        password = request.data.get('password')
        email = ""
        print(request.data)
        if request.data.get('ip_address') is None:
            response_text_file(
                value={"status": "error", 'message': messages.get("ip_error")})
            return Response({"status": "error", 'message': messages.get("ip_error")}, status=status.HTTP_400_BAD_REQUEST)

        if "@" in email_or_phone:
            email = email_or_phone
        else:
            validate_phone_number = check_phone_number(email_or_phone)
            user = {}
            try:
                user = User.objects.get(
                    mobile=validate_phone_number)
            except:
                user = {}
            if user:
                email = user.email
            else:
                (email, password) = (None, None)

        user = authenticate(email=email, password=password)

        if user is not None:
            obj = check_device(user.id, request.data.get(
                'device_model'),  request.data.get('imei_number'))

            if obj is not None:
                token = get_tokens_for_user(user)
                response_text_file(user=user.id, value={"status": "success", 'message': messages.get(
                    "login_success"), "data": {'token': token, }})
                return Response({"status": "success", 'message': messages.get("login_success"), "data": {'token': token, }}, status=status.HTTP_200_OK)
            response_text_file(user=user.id, value={
                               "status": "error", 'message': messages.get("device_information_error")})
            return Response({"status": "error", 'message': messages.get("device_information_error")}, status=status.HTTP_404_NOT_FOUND)
        else:
            response_text_file(value={"status": "error", 'message': messages.get(
                "wrong_email_or_phone_and_password")})
            return Response({"status": "error", 'message': messages.get("wrong_email_or_phone_and_password")}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        print(request.user.id)
        request_text_file(user=request.user.id, value=request.data)
        serializer = UserProfileSerializer(request.user)
        response_text_file(user=request.user.id, value={
                           "status": "success", 'message': "user data", "data": serializer.data})
        return Response({"status": "success", 'message': "user data", "data": serializer.data}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request_text_file(user=request.user.id, value=request.data)
        password = request.data.get('password')
        password2 = request.data.get('password2')
        obj = check_device(request.user.id, request.data.get(
            'device_model'),  request.data.get('imei_number'))

        if request.data.get('ip_address') is None:
            response_text_file(
                value={"status": "error", 'message': messages.get("ip_error")})
            return Response({"status": "error", 'message': messages.get("ip_error")}, status=status.HTTP_400_BAD_REQUEST)

        if obj is not None:
            serializer = UserChangePasswordSerializer(
                data={"password": password, "password2": password2}, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            response_text_file(user=request.user.id,
                               value={"status": "success", 'message': messages.get("password_changed")})
            return Response({"status": "success", 'message': messages.get("password_changed")}, status=status.HTTP_200_OK)
        response_text_file(user=request.user.id, value={
            "status": "error", 'message': messages.get("device_information_error")})
        return Response({"status": "error", 'message': messages.get("device_information_error")}, status=status.HTTP_404_NOT_FOUND)


# # +++++++++++++++++++++++++++++++++++++++++++++++++++ #

class UserTblAttendanceView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user.id
        value = request.data
        request_text_file(user=user, value=value)
        ip_address = value.get('ip_address')
        obj = check_device(user, value.get(
            'device_model'), value.get('imei_number'))

        if ip_address is None:
            response_text_file(
                value={"status": "error", 'message': messages.get("ip_error")})
            return Response({"status": "error", 'message': messages.get("ip_error")}, status=status.HTTP_400_BAD_REQUEST)

        if obj is not None:
            data = value
            data["fld_user_id"] = user
            data["fld_ip_address"] = ip_address
            serializer = TblAttendanceSerializer(
                data=data)
            if serializer.is_valid():
                serializer.save()
                response_text_file(user=user, value={
                                   "status": "success", 'message': 'Data Created'})
                return Response({"status": "success", 'message': 'Data Created'}, status=status.HTTP_201_CREATED)
            response_text_file(user=user, value=serializer.errors)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        response_text_file(user=user, value={
            "status": "error", 'message': messages.get("device_information_error")})
        return Response({"status": "error", 'message': messages.get("device_information_error")}, status=status.HTTP_404_NOT_FOUND)


class UserSitesView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        id = request.user.id
        request_text_file(user=id, value=request.data)

        sites = get_object_or_404(TblUserSites, fld_user_id=id)
        # print(id)
        serializer = TblUserSitesSerializer(sites)
        response_text_file(user=id, value={
                           "status": "success", 'message': "user sites", "data": serializer.data})
        return Response({"status": "success", 'message': "user sites", "data": serializer.data}, status=status.HTTP_200_OK)
