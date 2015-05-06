from django.contrib import admin
from django.contrib.auth.models import Permission
from User.models import User
from Course.models import Course

# Register your models here.
def make_staff(UserAdmin, request, queryset):
    queryset.update(is_staff=True)

#Redifining UserAdmin funciton
class UserAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'email', 'is_staff')
    search_fields = ['email']
    actions = [make_staff]

admin.site.register(User, UserAdmin)
admin.site.register(Course)

