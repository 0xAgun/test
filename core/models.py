from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Lincesekeys(models.Model):
    Keys = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.Keys



class Userreports(models.Model):
    SERV = (
        ('P1', 'P1'),
        ('P2', 'P2'),
        ('P3', 'P3'),
        ('P4', 'P4'),
        ('P5', 'P5'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    descrip = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=50, choices=SERV)
    # image = models.ImageField(blank=True, null=True)
    date_of_report = models.DateTimeField(auto_now_add=True, null=True)
    admin_approved = models.BooleanField(default=False)

    def __str__(self):
        self.author = str(self.user)
        if self.admin_approved:
            return self.title + ' by ' + self.author + ' | Accepted'

        return self.title + ' by ' + self.author + ' | Unaccepted'

    def get_points(self):
        dics = {'P1':100, 'P2':70, 'P3':50, 'P4':30, 'P5':10}
        if self.admin_approved:
            points = dics[self.severity]

            return points

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reports = models.ForeignKey(Userreports, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

    def add_points(self):
        fil = reports.objects.filter(users=self.user.id)
        return fil

class Images(models.Model):
    reports = models.ForeignKey(Userreports, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.reports.title + "'s image"

class Comments(models.Model):
    reports = models.ForeignKey(Userreports, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reports.title

                    


