from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext as _

class CustomUserManager(BaseUserManager):
    def create_superuser(self,username,phone,fullname,password,**others):
        others.setdefault('is_staff',True)
        others.setdefault('is_superuser',True)
        others.setdefault('is_active',True)

        if others.get('is_staff') is not True:
            raise ValueError(_("Superuser must be assigned to is_staff=True"))
        if others.get('is_superuser') is not True:
            raise ValueError(_("Superuser must be assigned to is_superuser=True"))

        user = self.create_user(username,phone,fullname,password,**others)
        # user.is_admin = True
        user.save(using=self._db)

        return user

    def create_user(self,username,phone,fullname,password,**others):
        others.setdefault('is_active',True)
        if not username:
            raise ValueError(_("You must provide an username"))
        user = self.model(username=username,phone=phone,fullname=fullname,**others)
        user.set_password(password)
        user.save(using=self._db)

        return user
