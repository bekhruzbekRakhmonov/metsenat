from django.db import models,transaction,IntegrityError
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone

from . import validators
from . import managers

class User(AbstractBaseUser,PermissionsMixin): 
    username = models.CharField(_("Username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[validators.UsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        })

    fullname = models.CharField(
        _("Full name"),
        max_length=255,
        null=True)
    phone = models.CharField(
        _("Phone number"),
        max_length=13,
        validators=[validators.PhoneNumberValidator()],
        null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("Date joined"), default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["fullname","phone"]

    objects = managers.CustomUserManager()

class Application(models.Model):
    fullname = models.CharField(
        _("Full name"),
        max_length=255,
        null=True)

    phone = models.CharField(
        _("Phone number"),
        max_length=13,
        validators=[validators.PhoneNumberValidator()])

    payment_amount = models.FloatField(
        _("Payment Amount"),validators=[validators.payment_amount_validator])

    status_choices = (
        ("pending", _("Pending")),
        ("verified", _("Verified")),
        ("rejected", _("Rejected")),
        ("new", _("New")),
    )

    status = models.CharField(_("Status"),max_length=8,choices=status_choices,default="pending")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.fullname

class PhysicalApplication(Application):
    @property
    def is_physical(self):
        return True

    @property
    def is_org(self):
        return False

class OrgApplication(Application):
    org_name = models.CharField(_("Organisation name"),max_length=255,blank=True)

    @property
    def is_physical(self):
        return False

    @property
    def is_org(self):
        return True

class Student(models.Model):
    fullname = models.CharField(_("Full name"),max_length=255)
    phone = models.CharField(_("Phone number"),max_length=13,
        validators=[validators.PhoneNumberValidator()])

    degree_choices = (
        ("bachelor", "Bachelor"),
        ("master", "Master"),
    )
    degree = models.CharField(_("Choose a degree"),max_length=8,
        choices=degree_choices,default="bachelor")
    college_choices = (
        ("INHA", "INHA"),
        ("WIUT", "WIUT"),
        ("TDIU", "TDIU"),
        ("MDIST", "MDIST"),
    )
    college = models.CharField(_("Choose a college"),max_length=255,
        choices=college_choices)
    tution_fee = models.FloatField(_("Tution fee"),
        validators=[validators.payment_amount_validator])

    unpaid_tution_fee = models.FloatField(_("Unpaid Tution fee"),
        validators=[validators.payment_amount_validator])
    
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname


class TransactionTracker(models.Model):
    org_sponsor = models.ForeignKey(
        OrgApplication,
        related_name="transaction_org_sponsor",
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    physical_sponsor = models.ForeignKey(
        PhysicalApplication,
        related_name="transaction_physical_sponsor",
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    student = models.ForeignKey(
        Student,
        related_name="transaction_student",
        on_delete=models.CASCADE,
        null=True)

    amount = models.FloatField(null=True,
        validators=[validators.payment_amount_validator])

    created_at = models.DateTimeField(auto_now_add=True)

    def validate(self):
        if all([self.student,self.amount]) and any([self.org_sponsor,self.physical_sponsor]):
            return True
        return False

    def init(self):
        valid = self.validate()
        if valid:
            if self.org_sponsor is not None and self.physical_sponsor is None:
                self.sponsor = self.org_sponsor
            elif self.org_sponsor is None and self.physical_sponsor is not None:
                self.sponsor = self.physical_sponsor
            else:
                return 

            return self
        return

    def __str__(self):
        return f"{self.org_sponsor}  {self.student}  {self.amount}"

    def can_be_sponsor(self):
        if (self.sponsor.payment_amount > self.amount) and (
                self.sponsor.status == "verified" or self.sponsor.status == "new"):
            return True
        return False

    def is_valid(self):
        can_be_sponsor = self.can_be_sponsor()
        if can_be_sponsor:
            if (self.student.unpaid_tution_fee - self.amount) >= 0:
                return True

        return False

    def do_transaction(self):
        if self.is_valid():
            self.sponsor.payment_amount = self.sponsor.payment_amount - self.amount
            try:
                self.sponsor.save()
                self.student.unpaid_tution_fee = self.student.unpaid_tution_fee - self.amount
                self.student.save()
                print(":=> KELDI")
                return True
            except IntegrityError:
                print(":=> KELDI")
                transaction.rollback()
        return False

    @classmethod
    def get_sponsors(cls,is_org=False,is_physical=False,student_id=None):
        if is_org:
            return cls.objects.filter(physical_sponsor=None,student__id=student_id)
        elif is_physical:
            return cls.objects.filter(org_sponsor=None,student__id=student_id)
        else:
            return cls.objects.filter(student__id=student_id)

    @property
    def sponsor(self):
        if self.physical_sponsor is not None:
            return self.physical_sponsorr
        elif self.org_sponsor is not None:
            return self.org_sponsor