from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from .models import Profile,Post,User,Comment

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','username', 'email','full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()



class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user','bio','location','birth_date','followers_count','following_count']

    def get_followers_count(self,obj):
        return obj.followers.count()

    def get_following_count(self,obj):
        return obj.following.count()



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['post','author','content','created_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)



class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['author','content','created_at','updated_at','likes']

    def validate(self, obj):
        if len(obj) > 1000:
            raise serializers.ValidationError("1000 tadan kam bo'lishi kerak.")
        return obj

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all()


