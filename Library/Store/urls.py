from django.urls import path
from . import views


urlpatterns = [
    # NORMAL USER 
    path('', views.index, name='index'),

    # LOGIN MECHNISM
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    #=========================================================USER=====================================================


    path('add_stagiaire/', views.add_stagiaire,name="add_stagiaire"),
    path('edit_stagiaire/<int:pk>', views.edit_stagiaire,name="edit_stagiaire"),
    path('delete_stagiaire/<int:pk>', views.delete_stagiaire,name="delete_stagiaire"),

    path('add_permission/', views.add_permission,name="add_permission"),
    path('edit_permission/<int:pk>', views.edit_permission,name="edit_permission"),
    path('delete_permission/<int:pk>', views.delete_permission,name="delete_permission"),

    path('add_fiche/', views.add_fiche, name="add_fiche"),
    path('edit_fiche/<int:pk>', views.edit_fiche, name="edit_fiche"),
    path('delete_fiche/<int:pk>', views.delete_fiche, name="delete_fiche"),
    path('display_fiche/<path:file_name>', views.display_fiche, name="display_fiche"),

    

    path('add_consultation/', views.add_consultation, name="add_consultation"),
    path('edit_consultation/<int:pk>', views.edit_consultation, name="edit_consultation"),
    path('delete_consultation/<int:pk>', views.delete_consultation, name="delete_consultation"),


    path('add_reservation/', views.add_reservation, name="add_reservation"),
    path('edit_reservation/<int:pk>', views.edit_reservation, name="edit_reservation"),
    path('delete_reservation/<int:pk>', views.delete_reservation, name="delete_reservation"),


    path('stagiaires/', views.stagiaires, name="stagiaires"),
    path('permissions/', views.permissions, name="permissions"),
    path('renseignements/', views.renseignements, name="renseignements"),
    path('consultations/', views.consultations, name="consultations"),
    path('reservations/', views.reservations, name="reservations"),

    #================================================================PDF================================================


    path('reservation/<int:pk>', views.pdf_reservation, name="pdf_reservation"),
     path('permission/<int:pk>', views.pdf_permission, name="pdf_permission"),
    #path('pdf/consultation/<int:pk>', views.edit_consultation, name="edit_consultation"),
    #path('pdf/permission/<int:pk>', views.edit_permission,name="edit_permission"),


    
]
