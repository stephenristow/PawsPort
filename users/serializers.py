from rest_framework import serializers


class UserUpdateIn(serializers.Serializer):
    pawsword = serializers.CharField(max_length=255, required=False, allow_blank=True)
    username = serializers.CharField(max_length=32, required=False, allow_blank=True)


class UserPublicOut(serializers.Serializer):
    username = serializers.CharField()


class UserPrivateOut(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.IntegerField()
    username = serializers.CharField()
