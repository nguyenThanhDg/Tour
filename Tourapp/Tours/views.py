from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import Category, Tour, News, Customer, Comment, Employee, Like, Rating
from .perms import CommentOwnerPerms
from .serializers import CategorySerializer, TourSerializer, ImageTourSerializer, NewsSerializer, ImageNewsSerializer, \
    CustomerSerializer, CreateCommentSerializer, EmployeeSerializer, CommentSerializer


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer

    @action(methods=['get'],detail=True,url_path='tours')
    def get_tour(self,request,pk):
        categories = self.get_object()
        tours = categories.tours.filter(active=True)

        q = request.query_params.get('q')
        if q is not None:
            tours = tours.filter(name__icontains=q)
        return Response(TourSerializer(tours, many=True, context={"request": request}).data,status = status.HTTP_200_OK)


class TourViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Tour.objects.filter(active=True)
    serializer_class = TourSerializer

    def get_queryset(self):
        queryset = self.queryset

        kw = self.request.query_params.get("kw")
        if kw:
            queryset = queryset.filter(subject__icontains=kw)

        category_id = self.request.query_params.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    @action(methods=['get'], detail=True, url_path='imagesTour')
    def get_images(self, request, pk):
        tour = Tour.objects.get(pk=pk)
        images = tour.imagesTour.filter(active=True)

        return Response(data=ImageTourSerializer(images, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='rate', detail=True)
    def rating(self, request, pk):
        news = self.get_object()
        user = request.user

        r, _ = Rating.objects.get_or_create(news=news, user=user)
        r.rate = request.data.get('rate', 0)
        try:
            r.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)


class NewsViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = News.objects.filter(active=True)
    serializer_class = NewsSerializer

    @action(methods=['get'], detail=True, url_path='imagesNews')
    def get_images(self, request, pk):
        tour = News.objects.get(pk=pk)
        images = tour.imagesNews.filter(active=True)

        return Response(data=ImageNewsSerializer(images, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='comment')
    def get_comment(self, request, pk):
        news = self.get_object()
        comments = news.comments.select_related('customer').filter(active=True)
        return Response(CommentSerializer(comments, many=True).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        news = self.get_object()
        user = request.user

        l, _ = Like.objects.get_or_create(news=news, user=user)
        l.active = not l.active
        try:
            l.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)


class CustomerViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView):
    queryset = Customer.objects.filter(active=True)
    serializer_class = CustomerSerializer


class CommentViewSet(viewsets.ViewSet, generics.ListAPIView,generics.CreateAPIView,generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CreateCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update','destroy']:
            return [CommentOwnerPerms()]

        return [permissions.IsAuthenticated()]


class EmployeeViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Employee.objects.filter(is_active=True)
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current-user", detail=False)
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class AuthInfo(APIView):
    def get(self, request):
        return Response(data=settings.OAUTH2_INFO, status=status.HTTP_200_OK)