from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Celebrity, Booking
from .forms import CelebrityForm, BookingForm
from django.contrib import messages

ADMIN_SIGNUP_CODE = "ADMIN2026"  # change this

@login_required
def admin_signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        code = request.POST.get('code')

        if code != ADMIN_SIGNUP_CODE:
            messages.error(request, 'Invalid admin signup code')
            return redirect('admin_signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('admin_signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_staff = True
        user.is_superuser = False  # optional
        user.save()

        login(request, user)
        messages.success(request, 'Admin account created successfully')

        return redirect('dashboard')

    return render(request, 'admin_signup.html')

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid admin credentials')

    return render(request, 'admin_login.html')

def admin_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("admin_login")

def index(request):
    celebindex=Celebrity.objects.order_by('name')[:4]
    context={
        'celebindex':celebindex
    }
    return render(request, 'index.html',context)

def aboutus(request):
    return render(request, 'aboutus.html')

def privacypolicy(request):
    return render(request, 'privacypolicy.html')

def termsandconditions(request):
    return render(request, 'termsandconditions.html')

def contactus(request):
    return render(request, 'contactus.html')

def info(request):
    return render(request, 'info.html')

def celebrity_list(request):
    celebrities = Celebrity.objects.all()
    return render(request, 'celebrity_list.html', {'celebrities': celebrities})


def celebrity_detail(request, slug):
    celebrity = get_object_or_404(Celebrity, slug=slug)
    similar_celebs = Celebrity.objects.filter(category=celebrity.category).exclude(id=celebrity.id)[:3]
    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.celebrity = celebrity
            booking.status = 'pending'  # FORCE safety (important)
            booking.save()#
            
            return redirect('booking_success', booking_id=booking.id)

    return render(request, 'celebrity_detail.html', {
        'celebrity': celebrity,
        'form': form,
        'similar_celebs': similar_celebs,
    })
    

def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})



def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin, login_url='admin_login')
def dashboard(request):
    query = request.GET.get('q')
    
    all_celebrities = Celebrity.objects.order_by('name')
    bookings = Booking.objects.all()
    if query:
        celebrities = all_celebrities.filter(name__icontains=query)[:5]
    else:
        celebrities = all_celebrities[:5]
        
    total_celebs = all_celebrities.count() 
    total_booking = bookings.count() or 0
    pending_bookings = Booking.objects.filter(status='pending').count()
    return render(request, 'dashboard.html', {
        'celebrities': celebrities,
        'bookings': bookings,
        'total_celebs': total_celebs,
        'total_booking' : total_booking,
        'pending_bookings': pending_bookings,
    })


@login_required
def edit_celebrity(request, id):
    celebrity = get_object_or_404(Celebrity, id=id)
    if request.method == 'POST':
        form = CelebrityForm(request.POST, request.FILES, instance=celebrity)
        if form.is_valid():
            form.save()
            return redirect('celeb_all')
    else:
        form = CelebrityForm(instance=celebrity)

    return render(request, 'edit_celebrity.html', {
        'form': form,
        'celebrity': celebrity
    })
    

@login_required
def delete_celebrity(request, id):
    celebrity = get_object_or_404(Celebrity, id=id)

    if request.method == 'POST':
        celebrity.delete()
        return redirect('dashboard')

    return render(request, 'delete_celebrity.html', {
        'celebrity': celebrity
    })


@login_required
def delete_multiple_celebs_page(request):
    celebrities = Celebrity.objects.all().order_by('name')  # can order alphabetically
    return render(request, 'delete_multiple_celebs.html', {
        'celebrities': celebrities
    })

@login_required
def delete_multiple_celebs_action(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('celebrities')
        if selected_ids:
            Celebrity.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f"{len(selected_ids)} celebrity(s) deleted successfully!")
        else:
            messages.warning(request, "No celebrities were selected.")
    return redirect('celeb_all')

@login_required
def add_celebrity(request):
    if request.method == 'POST':
        form = CelebrityForm(request.POST, request.FILES)
        if form.is_valid():
            celebrity = form.save()
            messages.success(
                request,
                f' "{celebrity.name}" added successfully!'
            )

            return redirect('celeb_all')
    else:
        form = CelebrityForm()

    return render(request, 'add_celebrity.html', {'form': form})

@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'approved'
    booking.save()

    messages.success(
        request,
        f'Booking for {booking.celebrity.name} approved successfully.'
    )
    return redirect('bookings')

@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'rejected'
    booking.save()

    messages.warning(
        request,
        f'Booking for {booking.celebrity.name} rejected.'
    )
    return redirect('bookings')


@login_required
def pending_books(request):
    bookings = Booking.objects.all().order_by('-created_at')
    pending_bookings = Booking.objects.filter(status='pending').count()
    context = {
        'pending_bookings': pending_bookings,
        'bookings': bookings,
    }
    return render(request, 'pending_books.html', context)

@login_required
def bookings(request):
    bookings = Booking.objects.all().order_by('-created_at')
    context = {
        'bookings': bookings,
    }
    return render(request, 'bookings.html', context)

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    return render(request, 'booking_detail.html', {
        'booking': booking
    })

@login_required
def celeb_all(request):
    listall=Celebrity.objects.all().order_by('name')
    context ={
        'listall':listall
    }
    return render(request, 'celeb_all.html',context)

@login_required
def celeb_view(request, celebview_id):
    seedetceleb = get_object_or_404(Celebrity, id=celebview_id)

    return render(request, 'celeb_view.html', {
        'seedetceleb': seedetceleb
    })
    
@login_required
def user_profile(request):
    return render(request, 'user_profile.html', {
        'user': request.user
    })
    

@login_required
def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')

        if User.objects.filter(username=new_username).exists():
            messages.error(request, "Username already taken.")
        else:
            request.user.username = new_username
            request.user.save()
            messages.success(request, "Username updated successfully.")
            return redirect('user_profile')

    return render(request, 'change_username.html')

@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')

        if User.objects.filter(email=new_email).exists():
            messages.error(request, "This email is already in use.")
        else:
            request.user.email = new_email
            request.user.save()
            messages.success(request, "Email updated successfully.")
            return redirect('user_profile')

    return render(request, 'change_email.html')