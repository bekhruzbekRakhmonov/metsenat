from django import forms
from django.utils.translation import gettext as _

from . import models

class StudentCreationForm(forms.ModelForm):
    class Meta:
        model = models.Student
        exclude = ["created_at","unpaid_tution_fee"]


class StudentChangeForm(forms.ModelForm):
    class Meta:
        model = models.Student
        exclude = ["unpaid_tution_fee"]

class AddSponsorForm(forms.ModelForm):
    org_sponsor = forms.ModelChoiceField(queryset=models.OrgApplication.objects.filter(status="verified"),required=False)
    physical_sponsor = forms.ModelChoiceField(queryset=models.PhysicalApplication.objects.filter(status="verified"),required=False)
    class Meta:
        model = models.TransactionTracker
        fields = ["org_sponsor","physical_sponsor","student","amount"]

class SponsorFilterForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(SponsorFilterForm, self).__init__(*args, **kwargs)
        self.fields["fullname"].required = False
        self.fields["payment_amount"].required = False
        self.fields["status"].required = False

        self.fields["payment_amount"].initial = 0

class OrgSponsorFilterForm(SponsorFilterForm):
    class Meta:
        model = models.OrgApplication
        fields = ["fullname","payment_amount","status"]

class PhysicalSponsorFilterForm(SponsorFilterForm):
    class Meta:
        model = models.PhysicalApplication
        fields = ["fullname","payment_amount","status"]

class StudentFilterForm(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = ["fullname","college","tution_fee"]

    def __init__(self,*args,**kwargs):
        super(StudentFilterForm, self).__init__(*args, **kwargs)
        self.fields["fullname"].required = False
        self.fields["college"].required = False
        self.fields["tution_fee"].required = False

        self.fields["tution_fee"].initial = 0

class SponsorEditForm(forms.Form):
    status_choices = (
        ("pending", _("Pending")),
        ("verified", _("Verified")),
        ("rejected", _("Rejected")),
        ("new", _("New")),
    )

    status = forms.ChoiceField(label=_("Status"),choices=status_choices)
