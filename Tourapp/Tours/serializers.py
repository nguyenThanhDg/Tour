import requests
from rest_framework import serializers
from .models import Category, Tour, ImageTour, News, ImageNews, Customer, Comment, Employee, Like, Rating


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    class Meta:
        model = Tour
        fields = ['id', 'name', 'image', 'numbersOfDay', 'numbersOfPeople', 'destination', 'price', 'content']

    def get_image(self, obj):
        request = self.context['request']
        path = '/static/%s' % obj.image
        return request.build_absolute_uri(path)


class ImageTourSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField(source='link')

    def get_link(self, obj):
        request = self.context['request']
        path = '/static/%s' % obj.link
        return request.build_absolute_uri(path)

    class Meta:
        model = ImageTour
        fields = ['id', 'link']


class NewsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, obj):
        request = self.context['request']
        path = '/static/%s' % obj.image
        return request.build_absolute_uri(path)

    class Meta:
        model = News
        fields = ['id','name', 'description', 'tour', 'image']


class ImageNewsSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField(source='link')

    def get_link(self, obj):
        request = self.context['request']
        path = '/static/%s' % obj.link
        return request.build_absolute_uri(path)

    class Meta:
        model = ImageNews
        fields = ['id', 'link']


class CustomerSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(source='avatar')

    def get_avatar(self, obj):
        request = self.context['request']
        path = '/static/%s' % obj.avatar
        return request.build_absolute_uri(path)

    class Meta:
        model = Customer
        fields = ['username', 'password', 'name', 'phone', 'email', 'avatar', 'dob']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        customer = Customer(**data)
        customer.set_password(customer.password)
        customer.save()

        return customer


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'customer', 'news']


class CommentSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Comment
        exclude = ['active']


class EmployeeSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(source='avatar')

    def get_avatar(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith("/static"):

            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name',
                  'username', 'password', 'email',
                  'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        employee = Employee(**data)
        employee.set_password(employee.password)
        employee.save()

        return employee


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'active']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rate']