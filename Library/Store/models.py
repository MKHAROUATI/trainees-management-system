from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.



groupe_choices = (
    ('groupe1', 'Groupe 1'),
    ('groupe2', 'Groupe 2'),
    ('groupe3', 'Groupe 3'),
    ('groupe4', 'Groupe 4'),
)


class CustomUser(AbstractUser):
    grade = models.CharField(max_length=150, null=False,blank=False)

class Groupe(models.Model):
    name = models.CharField(max_length=150, null=False,choices=groupe_choices)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}"



class Stagiaire(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    nom = models.CharField(max_length=150,null=False)
    prenom = models.CharField(max_length=150,null=False)
    grade = models.CharField(max_length=150,null=False)
    unite = models.CharField(max_length=150,null=True)
    pays = models.CharField(max_length=150,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} : {self.groupe.name}"


class Permission(models.Model):
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    motif = models.TextField(max_length=250,null=False)
    destination = models.CharField(max_length=150,null=False)
    duration = models.CharField(max_length=150,null=True, editable=False)
    date_out = models.DateField()
    date_in = models.DateField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate duration based on date_out and date_in
        if self.date_out and self.date_in:
            duration = self.date_in - self.date_out
            if duration.days == 0:
                self.duration = "Vinght Quatre Heures"
            elif duration.days == 1:
                self.duration = "Quarante Huit Heures"
            elif duration.days > 1:
                self.duration = f"{duration.days + 1} Jours"
        else:
            self.duration = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.stagiaire.groupe.owner.username} {self.stagiaire.nom} {self.stagiaire.groupe.name}"


class Renseignement(models.Model):
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    file = models.FileField(upload_to="fiches")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stagiaire} {self.file.name}"

class Consultation(models.Model):
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    medcin_decision = models.TextField(max_length=150,null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stagiaire} {self.medcin_decision}"


class Reservation(models.Model):
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    destination = models.CharField(max_length=150,null=False)
    duration = models.CharField(max_length=150,null=True, editable=False)
    date_out = models.DateField()
    date_in = models.DateField()
    accompagnateur = models.TextField(max_length=250,null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate duration based on date_out and date_in
        if self.date_out and self.date_in:
            duration = self.date_in - self.date_out
            if duration.days == 0:
                self.duration = "Vinght Quatre Heures"
            elif duration.days == 1:
                self.duration = "Quarante Huit Heures"
            elif duration.days > 1:
                self.duration = f"{duration.days + 1} Jours"
        else:
            self.duration = None

        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.id} {self.accompagnateur}"


