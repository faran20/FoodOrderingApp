from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.permission import IsStaff, IsSuperUser
from users.models import User
from users.serializers.staff.profile_serializers import StaffProfileSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsStaff | IsSuperUser])
def staff_profile(request):
    if request.method == "GET":
        serializer = StaffProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = StaffProfileSerializer(data=request.data["user"])
        print(request.user)
        if serializer.is_valid(raise_exception=ValueError) or serializer.is_valid(raise_exception=Exception):
            user_account= request.user
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            first_name = serializer.validated_data["first_name"]
            last_name = serializer.validated_data["last_name"]
            birth_date = serializer.validated_data["birth_date"]
            email = serializer.validated_data["email"]
            phone = serializer.validated_data["phone"]

            if user_account.username != username:
                if User.objects.filter(username=username):
                    return Response("user with this username already exists",
                                    status=status.HTTP_400_BAD_REQUEST)
                user_account.username = username

            if user_account.email != email:
                if User.objects.filter(email=email):
                    return Response("user with this email already exists",
                                    status=status.HTTP_400_BAD_REQUEST)
                user_account.email = email

            user_account.set_password(password)
            user_account.first_name = first_name
            user_account.last_name = last_name
            user_account.birth_date = birth_date
            user_account.phone = phone
            user_account.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.error_messages,
                    status=status.HTTP_400_BAD_REQUEST)