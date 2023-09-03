import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.core.mail import send_mail
from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, username, phone_number, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a user with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set.')
        email = self.normalize_email(email)
        user = self.model(
            phone_number=phone_number, username=username,
            email=email, is_staff=is_staff, is_active=True, 
            is_superuser=is_superuser, date_joined=now, **extra_fields
        )
        if not extra_fields.get('no_password'):
            user.set_password(password)
        
        user.save(using=self._db)
        return user
    
    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]
            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))

        return self._create_user(username, phone_number, email, password, False, False, **extra_fields)
    
    def create_superuser(self, username, phone_number, email, password, **extra_fields):
        return self._create_user(username, phone_number, email, password, True, True, **extra_fields)
    
    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured user model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(
        _('username'), max_length=32, unique=True,
        help_text=_(
            'required. 30 characters or fewer starting with a letter. Letters, digits, dot and underscore carachters are valid characters.'
        ),
        validators=[
            validators.RegexValidator(
                r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
                _('Enter a valid username starting with a-z. This value may contain only letters, numbers, dot and underscore characters.'),
                'invalid'
            ),
        ],
        error_messages={
            'unique': _("A user with this username already exists."),
        }
    )
    
    first_name = models.CharField(_('firstname'), max_length=30, blank=True)
    last_name = models.CharField(_('lastname'), max_length=32, blank=True)
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    phone_number = models.BigIntegerField(
        _('phone number'), unique=True, null=True, blank=True,
        validators=[
            validators.RegexValidator(
                r'^989[0-3,9]\d{8}$',
                _('Enter a valid mobile number.'),
                'invalid'
            ),
        ],
        error_messages={
            'unique': _("A user with this phone number already exists."),
        }
    )
    
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_(
        'Designates whether the user can log into this admin site.'
    ))
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates wheter this user should be treated as active. Unselect this instead of deleting accounts.'
    ))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(_('last seen'), null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']
    
    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        return self.first_name
    
    def email_user(self, subject, message, from_mail=None, **kwargs):
        send_mail(subject, message, from_mail, [self.email], **kwargs)
        
    @property
    def is_loggedin_user(self):
        return self.phone_number is not None or self.email is not None
    
    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)
        
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(_('nickname'), max_length=32, blank=True)
    avatar = models.ImageField(_('avatar'), blank=True)
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    gender = models.BooleanField(_('gender'), help_text=_('female is False, male is True, null is unset.'))
    province = models.ForeignKey(verbose_name=_('province'), to='province', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        
    @property
    def get_first_name(self):
        return self.user.first_name
    
    @property
    def get_last_name(self):
        return self.user.last_name
    
    def get_nickname(self):
        return self.nick_name if self.nick_name else self.user.username
    

class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DESKTOP = 4
    DEVICE_TYPES = (
        (WEB, _('web')),
        (IOS, _('IOS')),
        (ANDROID, _('android')),
        (DESKTOP, _('desktop')),
    )
    user = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE)
    device_uuid = models.UUIDField(_('Device UUID'), null=True)
    notify_token = models.CharField(
        _('Notification token'), max_length=200, blank=True,
        validators=[
            validators.RegexValidator(
                r'([a-z][A-Z][0-9])\w+', _('Notify token is not valid'), 'invalid'
            ),
        ]
    )
    last_login = models.DateTimeField(_('Last login date'), null=True)
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPES, default=ANDROID)
    device_os = models.CharField(_('device os'), max_length=20, blank=True)
    device_model = models.CharField(_('device model'), max_length=50, blank=True)
    app_version = models.CharField(_('app version'), max_length=20, blank=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    
    class Meta:
        db_table = 'user_devices'
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        unique_together = ('user', 'device_uuid')        
    
    
class Province(models.Model):
    name = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    
    