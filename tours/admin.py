from django.contrib import admin
from .models import Route, TourPackage, Customer, Booking

# ส่วนที่จะโชว์ประวัติการซื้อตั๋วในหน้าลูกค้า
class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    readonly_fields = ('BookingID', 'PackageID', 'TravelDate', 'TotalAmount', 'BookingStatus')
    can_delete = False

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('CustID', 'FullName', 'Phone')
    inlines = [BookingInline] # เพิ่มบรรทัดนี้เพื่อดูว่าซื้อตั๋วอะไร

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'destination_name', 'is_active') # ใช้ id เล็กตาม model เดิม

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('package_id', 'package_name', 'departure_time') # ใช้ตัวเล็กตาม model เดิม

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('BookingID', 'CustID', 'PackageID', 'BookingStatus')