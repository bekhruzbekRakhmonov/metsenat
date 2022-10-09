from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
from .auth import forms as auth_forms

class UserAdmin(BaseUserAdmin):
    form = auth_forms.UserChangeForm
    add_form = auth_forms.UserCreationForm
    
    list_display = ('id','username','fullname',)
    list_filter = ('username',)
    fieldsets = (
        (None,{'fields':('username','password',)}),
        ('Personal info',{'fields':('fullname','last_login',)}),
        ('Permissions',{'fields':('is_superuser','is_staff','is_active','groups',)})
    )

    # add fieldsets
    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields': ('username','fullname','is_superuser','last_login','is_active','is_staff','password1','password2'),
        }),
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

class OrgApplicationAdmin(admin.ModelAdmin):
	list_display = ("fullname","phone","payment_amount",
		"org_name","status","is_org","is_physical")

class PhysicalApplicationAdmin(admin.ModelAdmin):
	list_display = ("fullname","phone","payment_amount","status",
		"is_org","is_physical",)

class StudentAdmin(admin.ModelAdmin):
    list_display = ("fullname","phone","college",
                    "degree","tution_fee","unpaid_tution_fee",)

admin.site.register(models.OrgApplication,OrgApplicationAdmin)
admin.site.register(models.PhysicalApplication,PhysicalApplicationAdmin)
admin.site.register(models.Student,StudentAdmin)
admin.site.register(models.TransactionTracker)
admin.site.register(models.User,UserAdmin)
