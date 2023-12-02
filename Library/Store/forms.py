from django import forms

from .models import Groupe, Stagiaire, Permission, Renseignement, Consultation, Reservation


class StagiaireForm(forms.ModelForm):
    class Meta:
        model = Stagiaire
        fields = ['nom', 'prenom', 'grade', 'unite','groupe', 'pays']

    def __init__(self,user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and placeholders for each field
        self.fields['nom'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nom'})
        self.fields['prenom'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Prénom'})
        self.fields['grade'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Grade'})
        self.fields['unite'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Unité'})
        self.fields['groupe'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select a Groupe'})
        self.fields['pays'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Pays'})
        self.fields['groupe'].queryset = Groupe.objects.filter(owner=user)


class PermissionForm(forms.ModelForm):
    date_out = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date de Sortie'}),
        input_formats=['%Y-%m-%d']
    )

    date_in = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date de Retour'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Permission
        fields = ['stagiaire', 'motif', 'destination', 'date_out', 'date_in']


    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and placeholders for each field
        self.fields['stagiaire'].queryset = Stagiaire.objects.filter(groupe__owner=user)
        self.fields['stagiaire'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select a Stagiaire'})
        self.fields['motif'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Motif'})
        self.fields['destination'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Destination'})






class FicheForm(forms.ModelForm):


    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Renseignement
        fields = ['stagiaire', 'file']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and placeholders for each field
        self.fields['stagiaire'].queryset = Stagiaire.objects.filter(groupe__owner=user)
        self.fields['stagiaire'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select a Stagiaire'})



class ConsultationForm(forms.ModelForm):

    medcin_decision = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'La decision de medcin'}))

    class Meta:
        model = Consultation
        fields = ['stagiaire', 'medcin_decision']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and placeholders for each field
        self.fields['stagiaire'].queryset = Stagiaire.objects.filter(groupe__owner=user)
        self.fields['stagiaire'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select a Stagiaire'})





class ReservationForm(forms.ModelForm):

    accompagnateur = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Accompgnements'}))
    destination = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destination'}))

    date_out = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date de Sortie'}),
        input_formats=['%Y-%m-%d']
    )

    date_in = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date de Retour'}),
        input_formats=['%Y-%m-%d']
    )



    class Meta:
        model = Reservation
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and placeholders for each field
        self.fields['stagiaire'].queryset = Stagiaire.objects.filter(groupe__owner=user)
        self.fields['stagiaire'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select a Stagiaire'})



#===========================================SUPERUSER==========================================================================




class AdminStagiaireForm(forms.ModelForm):
    class Meta:
        model = Stagiaire
        fields = ['nom', 'prenom', 'grade', 'unite','groupe', 'pays']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and placeholders for each field
        self.fields['nom'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nom'})
        self.fields['prenom'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Prénom'})
        self.fields['grade'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Grade'})
        self.fields['unite'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Unité'})
        self.fields['groupe'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select a Groupe'})
        self.fields['pays'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Pays'})
        self.fields['groupe'].queryset = Groupe.objects.all()


class AdminPermissionForm(forms.ModelForm):
    date_out = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date de Sortie'}),
        input_formats=['%Y-%m-%d']
    )

    date_in = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date de Retour'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Permission
        fields = ['stagiaire', 'motif', 'destination', 'date_out', 'date_in']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and placeholders for each field
        self.fields['stagiaire'].queryset = Stagiaire.objects.all().order_by('groupe')
        self.fields['stagiaire'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select a Stagiaire'})
        self.fields['motif'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Motif'})
        self.fields['destination'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Destination'})






class AdminFicheForm(forms.ModelForm):


    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Renseignement
        fields = ['stagiaire', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and placeholders for each field
        self.fields['stagiaire'].queryset = Stagiaire.objects.all()
        self.fields['stagiaire'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select a Stagiaire'})



class AdminConsultationForm(forms.ModelForm):

    medcin_decision = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'La decision de medcin'}))

    class Meta:
        model = Consultation
        fields = ['stagiaire', 'medcin_decision']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and placeholders for each field
        self.fields['stagiaire'].queryset = Stagiaire.objects.all()
        self.fields['stagiaire'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select a Stagiaire'})





class AdminReservationForm(forms.ModelForm):

    accompagnateur = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Accompgnements'}))
    destination = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destination'}))

    date_out = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date de Sortie'}),
        input_formats=['%Y-%m-%d']
    )

    date_in = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date de Retour'}),
        input_formats=['%Y-%m-%d']
    )



    class Meta:
        model = Reservation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stagiaire = Stagiaire.objects.all().order_by('groupe')
        # Add Bootstrap classes and placeholders for each field
        self.fields['stagiaire'].queryset = stagiaire
        self.fields['stagiaire'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select a Stagiaire'})
