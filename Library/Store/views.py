import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Consultation, Groupe, Permission, Renseignement, Reservation, Stagiaire
from .forms import AdminConsultationForm, AdminFicheForm, AdminPermissionForm, AdminReservationForm, AdminStagiaireForm, StagiaireForm, PermissionForm, FicheForm, ConsultationForm, ReservationForm
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            groupes = Groupe.objects.all()
            if groupes.exists():
                stagiaires_count = Stagiaire.objects.all().count()

                if stagiaires_count > 0:
                    renseignements = Renseignement.objects.all().count()
                    permissions = Permission.objects.all().count()
                    consultations = Consultation.objects.all().count()
                    reservations = Reservation.objects.all().count()

                    return render(request, 'home.html', {
                        "stagiaires": stagiaires_count,
                        "permissions": permissions,
                        "renseignements": renseignements,
                        "consultations": consultations,
                        "reservations": reservations
                    })
                else:
                    messages.error(request, 'No Stagiaire found for the user in any Groupe')
                    return redirect('index')
            else:
                messages.error(request, 'User is not associated with any Groupe')
                return redirect('index')
        else:
            groupes = Groupe.objects.filter(owner=request.user)
            stagiaires = Stagiaire.objects.filter(groupe__in=groupes).count()
            renseignements = Renseignement.objects.filter(stagiaire__in=Stagiaire.objects.filter(groupe__in=groupes)).count()
            permissions = Permission.objects.filter(stagiaire__in=Stagiaire.objects.filter(groupe__in=groupes)).count()
            consultations = Consultation.objects.filter(stagiaire__in=Stagiaire.objects.filter(groupe__in=groupes)).count()
            reservations = Reservation.objects.filter(stagiaire__in=Stagiaire.objects.filter(groupe__in=groupes)).count()

            return render(request, 'home.html', {
                "stagiaires": stagiaires,
                "permissions": permissions,
                "renseignements": renseignements,
                "consultations": consultations,
                "reservations": reservations
            })
             
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')

#==========================================================STAGIAIRE==================================================================

def add_stagiaire(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                form = AdminStagiaireForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Stagiaire has been added successfully.')
                    return redirect('stagiaires')  # Redirect to a success page or another view
                else:
                    messages.error(request, 'Invalid Form.')
            else:
                form = AdminStagiaireForm()

            return render(request, 'stagiaire/add.html', {'form': form})
        else:
            if request.method == 'POST':
                form = StagiaireForm(request.user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Stagiaire has been added successfully.')
                    return redirect('stagiaires')  # Redirect to a success page or another view
                else:
                    messages.error(request, 'Invalid Form.')
            else:
                form = StagiaireForm(user=request.user)

            return render(request, 'stagiaire/add.html', {'form': form})
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')



def edit_stagiaire(request, pk):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Get the existing Stagiaire instance
            stagiaire = get_object_or_404(Stagiaire, id=pk)
            if request.method == 'POST':
                # Populate the form with the POST data and the instance data
                form = AdminStagiaireForm(request.POST, instance=stagiaire)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Stagiaire has been updated successfully.')
                    return redirect('stagiaires')  # Redirect to a success page or another view
                else:
                    messages.error(request, 'Invalid Form.')
            else:
                # Populate the form with the instance data when rendering the form initially
                form = AdminStagiaireForm(instance=stagiaire)

            return render(request, 'stagiaire/update.html', {'form': form})

        else:
            stagiaire = get_object_or_404(Stagiaire, id=pk)
            if request.user == stagiaire.groupe.owner:
                if request.method == 'POST':
                    # Populate the form with the POST data and the instance data
                    form = StagiaireForm(request.user, request.POST, instance=stagiaire)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Stagiaire has been updated successfully.')
                        return redirect('stagiaires')  # Redirect to a success page or another view
                    else:
                        messages.error(request, 'Invalid Form.')
                else:
                    # Populate the form with the instance data when rendering the form initially
                    form = StagiaireForm(user=request.user, instance=stagiaire)

                return render(request, 'stagiaire/update.html', {'form': form})
            else:
                messages.error(request, 'You do not have permission to edit this Stagiaire.')
                return redirect('index')  # Create an error template for unauthorized access
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')

def delete_stagiaire(request, pk):
    if request.user.is_authenticated:
        stagiaire = get_object_or_404(Stagiaire, id=pk)
        stagiaire.delete()
        messages.success(request, 'Stagiaire has been Deleted successfully.')
        return redirect('stagiaires')
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')


#=======================================================PERMISSION=====================================================================


def add_permission(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                form = AdminPermissionForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Permission has been added successfully.')
                    return redirect('permissions')  # Redirect to a success page or another view
                else:
                    messages.error(request, 'Invalid Form.')
            else:
                form = AdminPermissionForm()
            return render(request, 'permission/add.html', {'form': form})
        else:
            if request.method == 'POST':
                form = PermissionForm(request.user,request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Permission has been added successfully.')
                    return redirect('permissions')  # Redirect to a success page or another view
                else:
                    messages.error(request, 'Invalid Form.')
            else:
                form = PermissionForm(user=request.user)

            return render(request, 'permission/add.html', {'form': form})
            
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')


def edit_permission(request, pk):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            permission = get_object_or_404(Permission, id=pk)
            if request.method == 'POST':
                form = AdminPermissionForm(request.POST, instance=permission)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Permission has been updated successfully.')
                    return redirect('permissions')
                else:
                    messages.error(request, 'Invalid Form.')
            else:
                form = AdminPermissionForm(instance=permission)

            return render(request, 'permission/update.html', {'form': form})
        else:
            permission = get_object_or_404(Permission, id=pk)
            if request.user == permission.stagiaire.groupe.owner:
                if request.method == 'POST':
                    form = PermissionForm(request.user, request.POST, instance=permission)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Permission has been updated successfully.')
                        return redirect('permissions')
                    else:
                        messages.error(request, 'Invalid Form.')
                else:
                    form = PermissionForm(user=request.user, instance=permission)

                return render(request, 'permission/update.html', {'form': form})
            else:
                messages.error(request, 'You do not have permission to edit this Permission.')
                return redirect('index')
            
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')

def delete_permission(request,pk):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            permission = get_object_or_404(Permission, id=pk)
            permission.delete()
            messages.success(request, 'Permission has been Deleted successfully.')
            return redirect('permissions')
        else:
            permission = get_object_or_404(Permission, id=pk)
            permission.delete()
            messages.success(request, 'Permission has been Deleted successfully.')
            return redirect('permissions')
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')

#=======================================================RENSEIGNEMENTS=====================================================================


def add_fiche(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                    form = AdminFicheForm(request.POST,request.FILES)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Permission has been added successfully.')
                        return redirect('renseignements')  # Redirect to a success page or another view
                    else:
                        messages.error(request, 'Invalid Form.')
            else:
                form = AdminFicheForm()
            return render(request, 'renseignement/add.html', {'form': form})
        else:
            if request.method == 'POST':
                form = FicheForm(request.user,request.POST,request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Permission has been added successfully.')
                    return redirect('renseignements')  # Redirect to a success page or another view
                else:
                    messages.error(request, 'Invalid Form.')
            else:
                form = FicheForm(user=request.user)
            return render(request, 'renseignement/add.html', {'form': form})
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')


def edit_fiche(request, pk):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            fiche = get_object_or_404(Renseignement, id=pk)
            if request.method == 'POST':
                form = AdminFicheForm(request.POST,request.FILES, instance=fiche)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Fiche Renseignement has been Updated successfully.')
                    return redirect('renseignements')
                else:
                    messages.error(request, 'Invalid Form.')
            else:
                form = AdminFicheForm(instance=fiche)

            return render(request, 'renseignement/update.html', {'form': form})
        else:
            fiche = get_object_or_404(Renseignement, id=pk)
            if request.user == fiche.stagiaire.groupe.owner:
                if request.method == 'POST':
                    form = FicheForm(request.user,request.POST,request.FILES, instance=fiche)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Fiche Renseignement has been Updated successfully.')
                        return redirect('renseignements')
                    else:
                        messages.error(request, 'Invalid Form.')
                else:
                    form = FicheForm(user=request.user,instance=fiche)

                return render(request, 'renseignement/update.html', {'form': form})
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('logout')

def delete_fiche(request,pk):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            fiche = get_object_or_404(Renseignement, id=pk)
            fiche.delete()
            messages.success(request, 'Fiche Renseignement has been Deleted successfully.')
            return redirect('renseignements')
        else:
            fiche = get_object_or_404(Renseignement, id=pk)
            fiche.delete()
            messages.success(request, 'Fiche Renseignement has been Deleted successfully.')
            return redirect('renseignements')
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('logout')


def display_fiche(request, file_name):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            renseignement = get_object_or_404(Renseignement, file=file_name)
            file_path = renseignement.file.path
            response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="' + file_name + '"'
            return response
        else:
            renseignement = get_object_or_404(Renseignement, file=file_name)
            file_path = renseignement.file.path
            response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="' + file_name + '"'
            return response
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('logout')


#=======================================================CONSULTATION=====================================================================


def add_consultation(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                form = AdminConsultationForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Consultation has been added successfully.')
                    return redirect('consultations')  # Redirect to a success page or another view
                else:
                    messages.error(request, 'Invalid Form.')
            else:
                form = AdminConsultationForm()
            return render(request, 'consultation/add.html', {'form': form})
        else:
            if request.method == 'POST':
                form = ConsultationForm(request.user,request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Consultation has been added successfully.')
                    return redirect('consultations')  # Redirect to a success page or another view
                else:
                    messages.error(request, 'Invalid Form.')
            else:
                form = ConsultationForm(user=request.user)

            return render(request, 'consultation/add.html', {'form': form})
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('logout')




def edit_consultation(request, pk):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            consultation = get_object_or_404(Consultation, id=pk)
            if request.method == 'POST':
                form = AdminConsultationForm(request.POST, instance=consultation)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Consultation has been Updated successfully.')
                    return redirect('consultations')
                else:
                    messages.error(request, 'Invalid Form.')
            else:
                form = AdminConsultationForm(instance=consultation)
            return render(request, 'consultation/update.html', {'form': form})
        else:
            consultation = get_object_or_404(Consultation, id=pk)
            if request.user == consultation.stagiaire.groupe.owner:
                if request.method == 'POST':
                    form = ConsultationForm(request.user,request.POST, instance=consultation)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Consultation has been Updated successfully.')
                        return redirect('consultations')
                    else:
                        messages.error(request, 'Invalid Form.')
                else:
                    form = ConsultationForm(user=request.user,instance=consultation)

                return render(request, 'consultation/update.html', {'form': form})

            else:
                messages.error(request, 'You do not have permission to edit this Consultation.')
                return redirect('index')

    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('logout')

def delete_consultation(request,pk):
    if request.user.is_authenticated:
        if request.user.is_superuser == False:
            consultation = get_object_or_404(Consultation, id=pk)
            consultation.delete()
            messages.success(request, 'Consultation has been Deleted successfully.')
            return redirect('consultations')
        else:
            consultation = get_object_or_404(Consultation, id=pk)
            consultation.delete()
            messages.success(request, 'Consultation has been Deleted successfully.')
            return redirect('consultations')
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('logout')



#=======================================================RESERVATION=====================================================================


def add_reservation(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                form = AdminReservationForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Reservation has been added successfully.')
                    return redirect('reservations') 
                else:
                    messages.error(request, 'Invalid Form.') # Redirect to a success page or another view
            else:
                form = AdminReservationForm()
            return render(request, 'reservation/add.html', {'form': form})
        else:
            if request.method == 'POST':
                form = ReservationForm(request.user,request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Reservation has been added successfully.')
                    return redirect('reservations')
                else:
                    messages.error(request, 'Invalid Form.')  # Redirect to a success page or another view
            else:
                form = ReservationForm(user=request.user)
            return render(request, 'reservation/add.html', {'form': form})  

            
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('logout')




def edit_reservation(request, pk):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            reservation = get_object_or_404(Reservation, id=pk)
            if request.method == 'POST':
                    form = AdminReservationForm(request.POST, instance=reservation)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Reservation has been Updated successfully.')
                        return redirect('reservations')
                    else:
                        messages.error(request, 'Invalid Form.')
            else:
                form = AdminReservationForm(instance=reservation)

            return render(request, 'reservation/update.html', {'form': form})
        else:
            reservation = get_object_or_404(Reservation, id=pk)
            if request.user == reservation.stagiaire.groupe.owner:
                    if request.method == 'POST':
                        form = ReservationForm(request.user,request.POST, instance=reservation)
                        if form.is_valid():
                            form.save()
                            messages.success(request, 'Reservation has been Updated successfully.')
                            return redirect('reservations')
                        else:
                            messages.error(request, 'Invalid Form.')
                    else:
                        form = ReservationForm(user=request.user,instance=reservation)

                    return render(request, 'reservation/update.html', {'form': form})
        
            else:
                messages.error(request, 'You do not have permission to edit this Consultation.')
                return redirect('index')

    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('logout')



def delete_reservation(request,pk):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            reservation = get_object_or_404(Reservation, id=pk)
            reservation.delete()
            messages.success(request, 'Reservation has been Deleted successfully.')
            return redirect('reservations')
        else:
            reservation = get_object_or_404(Reservation, id=pk)
            reservation.delete()
            messages.success(request, 'Reservation has been Deleted successfully.')
            return redirect('reservations')
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('logout')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to the desired page after successful login
            else:
                messages.error(request, 'Invalid username or password.')

        return render(request, 'authentification/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ===========================================DASHBOARD====================================================

def stagiaires(request):
    if request.user.is_authenticated:
        if request.user.is_superuser: 
            stagiaires = Stagiaire.objects.all().order_by('groupe')
            return render(request, 'stagiaire/index.html', {
                "stagiaires": stagiaires,

            })
        else:
            groupes = Groupe.objects.filter(owner=request.user)
            stagiaires = Stagiaire.objects.filter(groupe__in=groupes).order_by('-created_at')
            return render(request, 'stagiaire/index.html', {
                "stagiaires": stagiaires,
            })
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')
    

# ===============================================================================================
def permissions(request):
    if request.user.is_authenticated:
        if request.user.is_superuser: 
            permissions = Permission.objects.all().order_by('stagiaire__groupe')
            return render(request, 'permission/index.html', {
                "permissions": permissions,

            })
        else:   
            groupes = Groupe.objects.filter(owner=request.user)
            stagiaires = Stagiaire.objects.filter(groupe__in=groupes)
            permissions = Permission.objects.filter(stagiaire__in=stagiaires).order_by('-created_at')
            return render(request, 'permission/index.html', {
                "permissions": permissions,
            })
                
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')
    


# ===============================================================================================
def renseignements(request):
    if request.user.is_authenticated:
        if request.user.is_superuser: 
            renseignements = Renseignement.objects.all().order_by('stagiaire__groupe')
            return render(request, 'renseignement/index.html', {
                "renseignements": renseignements,

            })
        else:
            groupes = Groupe.objects.filter(owner=request.user)
            stagiaires = Stagiaire.objects.filter(groupe__in=groupes)
            renseignements = Renseignement.objects.filter(stagiaire__in=stagiaires).order_by('-created_at')
            return render(request, 'renseignement/index.html', {
                "renseignements": renseignements,
            })    
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')
    
    

# ===============================================================================================
def consultations(request):
    if request.user.is_authenticated:
        if request.user.is_superuser: 
            consultations = Consultation.objects.all().order_by('stagiaire__groupe')
            return render(request, 'consultation/index.html', {
                "consultations": consultations,

            })
        else:
            groupes = Groupe.objects.filter(owner=request.user)
            stagiaires = Stagiaire.objects.filter(groupe__in=groupes)
            consultations = Consultation.objects.filter(stagiaire__in=stagiaires).order_by('-created_at')
            return render(request, 'consultation/index.html', {

                "consultations": consultations,

            })
              
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')

# ===============================================================================================
def reservations(request):
    if request.user.is_authenticated:
        if request.user.is_superuser: 
            reservations = Reservation.objects.all().order_by('stagiaire__groupe')
            return render(request, 'reservation/index.html', {
                "reservations": reservations,

            })
        else:
            groupes = Groupe.objects.filter(owner=request.user)
            stagiaires = Stagiaire.objects.filter(groupe__in=groupes)
            reservations = Reservation.objects.filter(stagiaire__in=stagiaires).order_by('-created_at')
            return render(request, 'reservation/index.html', {

                "reservations": reservations,
            })
                
    else:
        messages.error(request, 'Login First to View the Contents')
        return redirect('login')
    
#=======================================================================PDF================================================



    

def pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    # Set encoding to 'utf-8' and use a font that supports French characters
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='utf-8')
    if not pdf.err:
        return result.getvalue()
    return None

#==============================================================================

def pdf_reservation(request, pk, *args, **kwargs):
    if isinstance(pk, dict):
        reservation_id = pk.get('id')
    else:
        reservation_id = pk

    # Ensure reservation_id is defined
    if reservation_id is None:
        raise Http404("Reservation ID not provided or invalid.")

    # Retrieve the Reservation object by ID
    reservation = get_object_or_404(Reservation, id=reservation_id)
    duree = reservation.date_in - reservation.date_out
    reservation_dict = {
        "groupe": reservation.stagiaire.groupe,
        "nom": reservation.stagiaire.nom,
        "prenom": reservation.stagiaire.prenom,
        "grade": reservation.stagiaire.grade,
        "pays": reservation.stagiaire.pays,
        "destination": reservation.destination,
        "duration": reservation.duration,
        "date_out": reservation.date_out,
        "date_in": reservation.date_in,
        "accompagnateur": reservation.accompagnateur,
        "duree" : duree,
        "created_at": reservation.created_at,
    }
    
    pdf_content = pdf('reservation/pdf.html', reservation_dict)
    
    if pdf_content:
        response = HttpResponse(pdf_content, content_type='application/pdf')
        filename = "Reservation_%s.pdf" %("12341231")
        response['Content-Disposition'] = f'inline; filename="{filename}"'

        return response
    else:
        return HttpResponse("Error generating PDF", status=500)
    
 #==============================================================================
    
def pdf_permission(request, pk, *args, **kwargs):
    if isinstance(pk, dict):
        permission_id = pk.get('id')
    else:
        permission_id = pk

    # Ensure reservation_id is defined
    if permission_id is None:
        raise Http404("Reservation ID not provided or invalid.")

    # Retrieve the Reservation object by ID
    permission = get_object_or_404(Permission, id=permission_id)
    duree = permission.date_in - permission.date_out
    

    permission_dict = {
        "groupe": permission.stagiaire.groupe,
        "nom": permission.stagiaire.nom,
        "prenom": permission.stagiaire.prenom,
        "grade": permission.stagiaire.grade,
        "pays": permission.stagiaire.pays,
        "destination": permission.destination,
        "duration": permission.duration,
        "date_out": permission.date_out,
        "date_in": permission.date_in,
        "motif": permission.motif,
        "created_at": permission.created_at,
        "duree" : duree
    }
    
    pdf_content = pdf('permission/pdf.html', permission_dict)
    
    if pdf_content:
        response = HttpResponse(pdf_content, content_type='application/pdf')
        filename = "Permission%s.pdf" %("12341231")
        response['Content-Disposition'] = f'inline; filename="{filename}"'

        return response
    else:
        return HttpResponse("Error generating PDF", status=500)