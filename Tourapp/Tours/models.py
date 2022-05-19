from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from ckeditor.fields import RichTextField


class Employee(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='employee/%Y/%m')


class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(ModelBase):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tour(ModelBase):
    name = models.CharField(max_length=100, unique=True)
    numbersOfDay = models.SmallIntegerField(null=False)
    numbersOfPeople = models.SmallIntegerField(null=False)
    destination = models.CharField(max_length=100, null=False)
    price = models.CharField(null=False,max_length=100)
    category = models.ForeignKey(Category,related_name='tours', on_delete=models.CASCADE, null=True)
    content = RichTextField(null=True)
    image = models.ImageField(null=True, upload_to='tour/%Y/%m')

    def __str__(self):
        return self.name


class Image(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True)
    name = models.CharField(null=False, max_length=100)
    link = models.ImageField(null=False, upload_to='image/%Y/%m')

    class Meta:
        abstract = True


class ImageTour(Image):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='imagesTour', null=True)

    def __str__(self):
        return self.name


class News(ModelBase):
    name = models.CharField(null=False, max_length=100)
    description = RichTextField()
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True,upload_to='news/%Y/%m')

    def __str__(self):
        return self.name


class ImageNews(Image):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='imagesNews', null=True)

    def __str__(self):
        return self.name


class Customer(AbstractBaseUser):
    username = models.CharField(null=False, max_length=120, unique=True)
    name = models.CharField(null=True, max_length=100)
    phone = models.CharField(null=True, max_length=100)
    email = models.CharField(null=True, max_length=100)
    avatar = models.ImageField(upload_to='customer/%Y/%m', null=True)
    dob = models.DateField()
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.name


class Order(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE,null=True, related_name='orders')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name='orders')


class Comment(ModelBase):
    content = models.TextField()
    news = models.ForeignKey(News,
                               related_name='comments',
                               on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Like(ModelBase):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    class Meta:
        unique_together = ['customer','news']
        abstract = True


class Rating(ModelBase):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    rate = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = ['customer', 'tour']
        abstract = True
