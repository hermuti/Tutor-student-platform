import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role = models.CharField(max_length=20, choices=[('Student', 'Student'), ('Tutor', 'Tutor'), ('Admin', 'Admin')])
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    preferred_learning_mode = models.CharField(max_length=100, choices=[('Online', 'Online'), ('In-Person', 'In-Person')])
    education_level = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Student Profile"

class TutorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    cv = models.FileField(upload_to='tutor_documents/cv/')
    resume = models.FileField(upload_to='tutor_documents/resume/')
    proof_of_identity = models.FileField(upload_to='tutor_documents/identity/')
    personal_statement_or_teaching_philosophy = models.TextField()

    def __str__(self):
         return f"{self.user.username}'s Tutor Profile"

class TutorEducation(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=[('High School Diploma', 'High School Diploma'), ('College Degree', 'College Degree'), ('Masters', 'Masters'), ('PhD', 'PhD')])
    file = models.FileField(upload_to='tutor_documents/education/')

    def __str__(self):
        return f"{self.tutor.user.username} - {self.document_type}"


class TutorCertification(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    file1 = models.FileField(upload_to='tutor_documents/certifications/', blank=True, null=True)
    file2 = models.FileField(upload_to='tutor_documents/certifications/', blank=True, null=True)
    file3 = models.FileField(upload_to='tutor_documents/certifications/', blank=True, null=True)

    def __str__(self):
        return f"{self.tutor.user.username} - {self.name}"

class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Admin Profile"
