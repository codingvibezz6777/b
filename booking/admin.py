from django.contrib import admin
from .models import Celebrity, Booking

@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'category', 'available', 'currency', 'stagename')
    

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'celebrity', 'event_date', 'created_at')
    
    
