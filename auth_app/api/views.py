from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import RegistrationSerializer, EmailLoginSerializer

# permission_classes = [IsAuthenticated]

class RegistrationView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "user_id": user.id,
                "email": user.email,
                "fullname": user.first_name,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response(
                {"detail": "email query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            serializers.EmailField().run_validation(email)
        except serializers.ValidationError:
            return Response(
                {"detail": "email is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "user not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "id": user.id,
                "email": user.email,
                "fullname": user.get_full_name(),
            },
            status=status.HTTP_200_OK,
        )
    
class EmailLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = EmailLoginSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "user_id": user.id,
                "email": user.email,
                "fullname": user.first_name,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)