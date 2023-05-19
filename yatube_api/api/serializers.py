from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from djoser.serializers import UserSerializer
from django.shortcuts import get_object_or_404

from posts.models import Comment, Post, Follow, Group, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Follow

    def validate(self, data):
        user = get_object_or_404(User, username=data['following'].username)
        if Follow.objects.filter(
            user=self.context['request'].user,
            following=user
        ).exists():
            raise serializers.ValidationError('The follow already exists')
        if user == self.context['request'].user:
            raise serializers.ValidationError(
                'User and following are coincide'
            )
        return data


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = '__all__'
