from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    '''
    (<django.db.models.fields.AutoField: id>, 
    <django.db.models.fields.CharField: password>, 
    <django.db.models.fields.DateTimeField: last_login>, 
    <django.db.models.fields.BooleanField: is_superuser>, 
    <django.db.models.fields.CharField: username>, 
    <django.db.models.fields.CharField: first_name>, 
    <django.db.models.fields.CharField: last_name>, 
    <django.db.models.fields.EmailField: email>, 
    <django.db.models.fields.BooleanField: is_staff>, 
    <django.db.models.fields.BooleanField: is_active>, 
    <django.db.models.fields.DateTimeField: date_joined>)
    '''
