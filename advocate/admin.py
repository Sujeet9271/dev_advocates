from django.contrib import admin

from advocate.models import Advocate, Company, SocialLinks

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id','name','logo']
    list_display_links = ['id','name',]

class SocialLinkInline(admin.StackedInline):
    model = SocialLinks
    extra = 0

class AdvocateAdmin(admin.ModelAdmin):
    list_display=['id','name','profile_pic','company','experience']
    list_display_links=['id','name',]
    list_filters = ['company']
    inlines = [SocialLinkInline]

# Register your models here.
admin.site.register(Company,CompanyAdmin)
admin.site.register(Advocate,AdvocateAdmin)
