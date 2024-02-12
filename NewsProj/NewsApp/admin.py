from django.contrib import admin
from .models import Profile,SavePost,SubscriptionPlan,UserProfile
# Register your models here.
""" 
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['profilepic','user','name','about','DOB']
admin.site.register(Profile,ProfileAdmin)

class SavePostAdmin(admin.ModelAdmin):
    list_display = ['author','title','source','description','published_at','url']
admin.site.register(SavePost,SavePostAdmin)

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name','price']
admin.site.register(SubscriptionPlan,SubscriptionPlanAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','subscription_plan','subscription_expiry']
admin.site.register(UserProfile,UserProfileAdmin) """

