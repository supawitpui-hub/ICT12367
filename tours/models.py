from django.db import models

# --- ตารางเดิมของพี่ (ห้ามเปลี่ยนชื่อตัวแปร) ---

class Route(models.Model):
    # ใช้ id เหมือนเดิม เพื่อให้หน้าแรกไม่พัง
    destination_name = models.CharField(max_length=100, verbose_name="ชื่อจังหวัดปลายทาง")
    destination_value = models.CharField(max_length=50, verbose_name="รหัสปลายทาง (ภาษาอังกฤษ)")
    is_active = models.BooleanField(default=True, verbose_name="เปิดให้บริการอยู่หรือไม่")

    class Meta:
        db_table = 'SouthernTour_Routes'
        verbose_name = 'เส้นทางเดินรถ'
        verbose_name_plural = 'เส้นทางเดินรถทั้งหมด'

    def __str__(self):
        return self.destination_name

class TourPackage(models.Model):
    package_id = models.CharField(db_column='PackageID', max_length=50, primary_key=True)
    package_name = models.CharField(db_column='PackageName', max_length=255)
    package_type = models.CharField(db_column='PackageType', max_length=100)
    price_adult = models.DecimalField(db_column='PriceAdult', max_digits=10, decimal_places=2)
    price_child = models.DecimalField(db_column='PriceChild', max_digits=10, decimal_places=2)
    ref_veh_id = models.CharField(db_column='RefVehID', max_length=50, null=True, blank=True)
    departure_time = models.TimeField(db_column='DepartureTime')

    class Meta:
        managed = False
        db_table = 'TourPackages'

    def __str__(self):
        return self.package_name

# --- ส่วนที่เพิ่มเข้าไปใหม่เพื่อให้ Admin ดูประวัติได้ (ไม่กระทบของเก่า) ---

class Customer(models.Model):
    CustID = models.AutoField(db_column='CustID', primary_key=True)
    FullName = models.CharField(db_column='FullName', max_length=255)
    Phone = models.CharField(db_column='Phone', max_length=50)

    class Meta:
        managed = False
        db_table = 'Customers'

    def __str__(self):
        return self.FullName

class Booking(models.Model):
    BookingID = models.AutoField(db_column='BookingID', primary_key=True)
    # เชื่อมเพื่อดูประวัติ
    CustID = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='CustID', related_name='bookings')
    PackageID = models.ForeignKey(TourPackage, on_delete=models.CASCADE, db_column='PackageID')
    TravelDate = models.DateField(db_column='TravelDate')
    TotalAmount = models.DecimalField(db_column='TotalAmount', max_digits=10, decimal_places=2)
    BookingStatus = models.CharField(db_column='BookingStatus', max_length=50)

    class Meta:
        managed = False
        db_table = 'Bookings'