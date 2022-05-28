from rest_framework import status, viewsets, generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from user.serializers import LogoutSerializer, PermissionSerializer, Permission, Group, GroupSerializer
from user.serializers import GroupReadSerializer, User, UserCreateSerializer, UserReadSerializer
from user.serializers import SetGroupSerializer, SetPermissionSerializer
from api.views import NestedSerializerMixin
from rest_framework_simplejwt.tokens import TokenError


class LogoutView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        success = True
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except TokenError:
            success = False

        return Response({'success': success}, status=status.HTTP_200_OK)


class PermissionView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Permission.objects.all()


class GroupView(NestedSerializerMixin):
    serializer_class = GroupSerializer
    read_serializer_class = GroupReadSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Group.objects.all()


class UserView(NestedSerializerMixin):
    serializer_class = UserCreateSerializer
    read_serializer_class = UserReadSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=True, methods=["post"], serializer_class=SetGroupSerializer)
    def set_groups(self, request):
        obj = self.get_object()
        data = request.data
        serializer = SetGroupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        rmv_groups = obj.groups.all()
        for group in rmv_groups:
            obj.groups.remove(group)
        groups = validated_data['groups']
        for group in groups:
            obj.groups.add(group)
        read = UserReadSerializer(obj)
        return Response(read.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], serializer_class=SetPermissionSerializer)
    def set_permissions(self, request):
        obj = self.get_object()
        data = request.data
        serializer = SetPermissionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        rmv_permissions = obj.groups.all()
        for permission in rmv_permissions:
            obj.user_permissions.remove(permission)
        user_permissions = validated_data['user_permissions']
        for permission in user_permissions:
            obj.groups.add(permission)
        read = UserReadSerializer(obj)
        return Response(read.data, status=status.HTTP_200_OK)
