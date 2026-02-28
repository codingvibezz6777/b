from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('celebrity_list', views.celebrity_list, name='celebrity_list'),
    path('celebrity/<slug:slug>/', views.celebrity_detail, name='celebrity_detail'),
    path('signup/', views.admin_signup, name='admin_signup'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path("logout/", views.admin_logout, name="admin_logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt',
            html_email_template_name='password_reset_email.html',
    ), name='password_reset'),
    path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name="password_reset_confirm"),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name="password_reset_complete"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('info/', views.info, name='info'),
    path('contactus/', views.contactus, name='contactus'),
    path('termsandconditions/', views.termsandconditions, name='termsandconditions'),
    path('privacypolicy//', views.privacypolicy, name='privacypolicy'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('pending_books', views.pending_books, name='pending_books'),
    path('bookings', views.bookings, name='bookings'),
    path('celeb_all', views.celeb_all, name='celeb_all'),
    path('dashboard/celebrity/add/', views.add_celebrity, name='add_celebrity'),
    path('dashboard/celebrity/edit/<int:id>/', views.edit_celebrity, name='edit_celebrity'),
    path('dashboard/celebrity/delete/<int:id>/', views.delete_celebrity, name='delete_celebrity'),
    path('dashboard/celebrity/delete-multiple/', views.delete_multiple_celebs_page, name='delete_multiple_celebs'),
    path('dashboard/celebrity/delete-multiple-action/', views.delete_multiple_celebs_action, name='delete_multiple_celebs_action'),
    path('booking/<int:booking_id>/approve/', views.approve_booking, name='approve_booking'),
    path('booking/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('seedetceleb/<int:celebview_id>/', views.celeb_view, name='celeb_view'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/change-username/', views.change_username, name='change_username'),
    path('profile/change-email/', views.change_email, name='change_email'),
    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),

]
