from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.models import Permission, Group
from user.models import User


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.refresh = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.refresh).blacklist()

        except TokenError:
            self.fail('Bad Token')


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupReadSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email',
                  'name', 'lastname')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserReadSerializer(serializers.ModelSerializer):
    groups = GroupReadSerializer(many=True)
    user_permissions = PermissionSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'lastname', 'description', 'is_active', 'is_superuser', 'groups',
                  'user_permissions')


class SetGroupSerializer(serializers.Serializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Group.objects.all(),
        help_text='groups relation'
    )


class SetPermissionSerializer(serializers.Serializer):
    user_permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Permission.objects.all(),
        help_text="permission relation"
    )
