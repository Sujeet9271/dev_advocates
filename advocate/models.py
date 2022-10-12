from datetime import datetime
from email.policy import default
from django.db import models
from django.urls import reverse
from dateutil import relativedelta

# Create your models here.

def company_location(instance,filename):
    return f'{instance.name.replace(" ", "")}/logo/{filename}'


class Company(models.Model):
    name=models.CharField(max_length=255)
    logo=models.ImageField(upload_to=company_location,default='old_logo.png')
    summary = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'

    def url(self):
        return reverse("company", kwargs={"id": self.pk})


    class Meta:
        db_table='companies'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['id']
    
def advocate_location(instance,filename):
    return f'{instance.company.name.replace(" ", "")}/advocates/{instance.name.replace(" ", "")}/{filename}'

class Advocate(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='advocates')
    name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to=advocate_location,default='adv_def.png')
    short_bio = models.TextField()
    long_bio = models.TextField()
    date_joined = models.DateField()


    def __str__(self):
        return f'{self.name}'
    
    @property
    def experience(self):
        date_joined = self.date_joined
        today = datetime.today().date()
        delta = relativedelta.relativedelta(today, date_joined)
        return f'{delta.years} years, {delta.months} months, {delta.days} days'

    def url(self):
        return reverse("advocate", kwargs={"id": self.pk})
    
    class Meta:
        db_table='advocates'
        verbose_name = 'Advocate'
        verbose_name_plural = 'Advocates'
        ordering = ['id']



class SocialLinks(models.Model):
    advocate = models.ForeignKey(Advocate,on_delete=models.CASCADE,related_name='links')
    name=models.CharField(max_length=255)
    url=models.URLField(max_length=100)

    def __str__(self):
        return f'{self.name}: {self.url}'

    class Meta:
        db_table = "social_links"
        verbose_name = 'Social Link'
        verbose_name_plural = 'Social Links'
        ordering = ['id']