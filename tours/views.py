from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import connection 
from .models import Route, TourPackage 
from .forms import CustomerRegisterForm
from datetime import date 
from django.contrib import messages

# --- 1. หน้าแรก ---
def index(request):
    destinations = Route.objects.filter(is_active=True)
    return render(request, 'tours/index.html', {'destinations': destinations})

# --- 2. ระบบสมัครสมาชิก ---
def register_view(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            full_name = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
            phone = form.cleaned_data.get('username')
            email = f"{phone}@southerntour.com"
            province = "ไม่ระบุ"
            cust_type = "General"
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "EXEC [dbo].[sp_AddCustomer] @FullName=%s, @Phone=%s, @Email=%s, @Province=%s, @CustomerType=%s", 
                        [full_name, phone, email, province, cust_type]
                    )
            except Exception as e:
                print("🚨 SQL Error (sp_AddCustomer):", e)
            login(request, user)
            return redirect('index')
    else:
        form = CustomerRegisterForm()
    return render(request, 'tours/register.html', {'form': form})

# --- 3. ระบบ Login ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'tours/login.html', {'form': form})

# --- 4. ระบบ Logout ---
def logout_view(request):
    logout(request)
    return redirect('index')

# --- 5. ระบบค้นหาเที่ยวรถ ---
def search_trips(request):
    destination_val = request.GET.get('destination')
    selected_route = None
    schedules = []
    if destination_val:
        selected_route = Route.objects.filter(destination_value=destination_val).first()
        if selected_route:
            search_term = selected_route.destination_name
            if " " in search_term:
                search_term = search_term.split(" ")[0]
            schedules = TourPackage.objects.filter(package_name__icontains=search_term).order_by('departure_time')
    return render(request, 'tours/search_results.html', {
        'selected_route': selected_route,
        'schedules': schedules
    })

# --- 6. ระบบจองที่นั่ง ---
@login_required(login_url='login')
def booking_view(request, package_id):
    package = TourPackage.objects.get(package_id=package_id)
    if request.method == 'POST':
        selected_seat = request.POST.get('selected_seat')
        user_phone = request.user.username 
        if selected_seat:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT CustID FROM Customers WHERE RTRIM(LTRIM(Phone)) = %s", [user_phone.strip()])
                    row = cursor.fetchone()
                    if row:
                        cust_id = row[0] 
                        travel_date = date.today() 
                        total_amount = package.price_adult 
                        booking_channel = 'Website' 
                        cursor.execute(
                            "EXEC [dbo].[sp_AddBooking] @CustID=%s, @PackageID=%s, @TravelDate=%s, @TotalAmount=%s, @BookingChannel=%s, @SeatNumber=%s",
                            [cust_id, package_id, travel_date, total_amount, booking_channel, selected_seat]
                        )
                        return render(request, 'tours/booking_success.html', {
                            'seat': selected_seat, 
                            'package': package
                        })
            except Exception as e:
                print(f"🚨 SQL Error (sp_AddBooking): {e}")

    booked_seats = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.SeatNumber 
                FROM SeatManagement s
                INNER JOIN Bookings b ON s.BookingID = b.BookingID
                WHERE b.PackageID = %s
            """, [package_id])
            booked_seats = [str(row[0]) for row in cursor.fetchall()]
    except Exception as e:
        print(f"🚨 SQL Error (Seat Check): {e}")

    total_seats = range(1, 31)
    return render(request, 'tours/booking.html', {
        'package': package,
        'total_seats': total_seats,
        'booked_seats': booked_seats
    })

# --- 7. ระบบประวัติการจอง ---
@login_required(login_url='login')
def my_bookings(request):
    user_phone = request.user.username.strip()
    bookings = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT b.BookingID, p.PackageName, p.DepartureTime AS TravelDate, 
                       b.TotalAmount, b.BookingStatus
                FROM Bookings b
                INNER JOIN Customers c ON b.CustID = c.CustID
                INNER JOIN TourPackages p ON b.PackageID = p.PackageID
                WHERE RTRIM(LTRIM(c.Phone)) = %s
                ORDER BY b.BookingID DESC
            """, [user_phone])
            columns = [col[0] for col in cursor.description]
            bookings = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"🚨 SQL Error (My Bookings): {e}")
    return render(request, 'tours/my_bookings.html', {'bookings': bookings})

# --- 8. หน้าแสดง QR Code ชำระเงิน ---
@login_required(login_url='login')
def payment_view(request, booking_id):
    booking = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT b.BookingID, p.PackageName, b.TotalAmount 
                FROM Bookings b
                JOIN TourPackages p ON b.PackageID = p.PackageID
                WHERE b.BookingID = %s
            """, [booking_id])
            row = cursor.fetchone()
            if row:
                booking = {'id': row[0], 'name': row[1], 'amount': row[2]}
    except Exception as e:
        print(f"🚨 Error fetching payment: {e}")
    return render(request, 'tours/payment.html', {'booking': booking})

# --- 9. ยืนยันการชำระเงิน ---
@login_required(login_url='login')
def confirm_payment(request, booking_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Bookings 
                SET BookingStatus = 'จ่ายเงินแล้ว' 
                WHERE BookingID = %s
            """, [booking_id])
    except Exception as e:
        print(f"🚨 Error updating status: {e}")
    return redirect('booking_ticket', booking_id=booking_id)

# --- 10. ระบบยกเลิกการจอง ---
@login_required(login_url='login')
def cancel_booking(request, booking_id):
    try:
        with connection.cursor() as cursor:
            # อัปเดตสถานะเป็น ยกเลิกแล้ว เฉพาะที่ยังไม่ได้จ่าย
            cursor.execute("""
                UPDATE Bookings 
                SET BookingStatus = 'ยกเลิกแล้ว' 
                WHERE BookingID = %s AND BookingStatus IN ('Pending', 'รอชำระเงิน')
            """, [booking_id])
            messages.success(request, f"ยกเลิกการจอง #{booking_id} เรียบร้อยแล้ว")
    except Exception as e:
        print(f"🚨 Error cancelling: {e}")
        messages.error(request, "ไม่สามารถยกเลิกได้ กรุณาติดต่อเจ้าหน้าที่")
    return redirect('my_bookings')

# --- 11. หน้าตั๋ว ---
@login_required(login_url='login')
def booking_ticket(request, booking_id):
    ticket = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT b.BookingID, p.PackageName, p.DepartureTime, b.TotalAmount, b.BookingStatus
                FROM Bookings b
                JOIN TourPackages p ON b.PackageID = p.PackageID
                WHERE b.BookingID = %s
            """, [booking_id])
            row = cursor.fetchone()
            if row:
                ticket = {
                    'id': row[0], 'package': row[1], 
                    'date': row[2], 'amount': row[3], 'status': row[4]
                }
    except Exception as e:
        print(f"🚨 Error fetching ticket: {e}")
    return render(request, 'tours/ticket.html', {'ticket': ticket})

# --- 12. หน้าติดต่อเรา ---
def contact_view(request):
    return render(request, 'tours/contact.html')