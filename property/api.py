from django.http import JsonResponse

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from useraccount.models import User
from .forms import PropertyForm, ReservationForm
from .models import Property, Reservation
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer


# Bringing properties owned by landlord_id
# Check if current logged user favorited any
# Add favorited properties'id's to favorites[]
@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    # Here the previous developer wanted to fuck around a little bit instead of using simply 'user = request.user' provided by DRF
    token_header = request.headers.get("Authorization")
    if not token_header:
        return JsonResponse({"Error": "Missing Authorization header"}, status=401)
    token_header_array = token_header.split()  # Split by space
    if len(token_header_array) != 2 or token_header_array[0].lower() != "bearer":
        return JsonResponse(
            {"Error": "Your Authorization header is fucked up a little"}, status=401
        )
    try:
        token = token_header_array[1]
        validated_token_payload = AccessToken(token)
        user_id = validated_token_payload["user_id"]
        user = User.objects.get(pk=user_id)
        favorites = []
        landlord_id = request.GET.get("landlord_id", "")
        if landlord_id:
            properties = Property.objects.filter(landlord_id=landlord_id)
        if user:
            for property in properties:
                if user in property.favorited.all():
                    favorites.append(property.id)
        serializer = PropertiesListSerializer(properties, many=True)
        return JsonResponse({"data": serializer.data, "favorites": favorites})
    except Exception as e:
        return JsonResponse({"Error": "Invalid or expired token"}, status=401)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    property = Property.objects.get(pk=pk)
    serializer = PropertiesDetailSerializer(property, many=False)
    return JsonResponse(serializer.data)


@api_view(["POST"])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)
    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user
        property.save()
        return JsonResponse({"success": True, "propertyId": property.id})
    else:
        print("error", form.errors, form.non_field_errors)
        return JsonResponse({"errors": form.errors.as_json()}, status=400)


@api_view(["POST"])
def book_property(request, pk):
    form = ReservationForm(request.POST)
    if form.is_valid():
        booking = form.save(commit=False)
        property = Property.objects.get(pk=pk)
        booking.created_by = request.user
        booking.property = property
        booking.save()
        return JsonResponse({"success": True}, status=201)
    else:
        return JsonResponse(
            {"errors from controller": form.errors.as_json()}, status=400
        )


@api_view(["POST"])
def toggle_favorited(request, pk):
    property = Property.objects.get(pk=pk)
    user = request.user
    if user in property.favorited.all():
        property.favorited.remove(user)
        return JsonResponse({"Favorited": False}, status=200)
    else:
        property.favorited.add(user)
        return JsonResponse({"Favorited": True}, status=200)
