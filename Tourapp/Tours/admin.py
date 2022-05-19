from django.contrib import admin

from .models import Tour, Category, ImageTour, News, ImageNews, Customer, Comment, Employee

admin.site.register(Category)
admin.site.register(Tour)
admin.site.register(ImageTour)
admin.site.register(News)
admin.site.register(ImageNews)
admin.site.register(Customer)
admin.site.register(Comment)
admin.site.register(Employee)