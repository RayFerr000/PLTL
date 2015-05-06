from django.contrib.auth.models import BaseUserManager


class CustUserManager(BaseUserManager):
    def create_user(self, fname,lname, email, password):
    	user = self.model(fname = fname, lname = lname, email = self.normalize_email(email))
    	user.is_active = True
    	user.set_password(password)
    	user.save(force_insert = True)
    	return user

    def create_superuser(self, fname, lname, email, password):
        user = self.create_user(fname,lname,email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
