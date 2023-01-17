from django.contrib import admin
from .models import User,Listing,Bid,Comment,WatchList


class WatchListAdmin(admin.ModelAdmin):
    filter_horizontal=("watchlist",)
    list_display=("id","user")
    
class UserAdmin(admin.ModelAdmin):
    list_display= ("id","username")

# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchList,WatchListAdmin)