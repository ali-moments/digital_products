from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.validators import validate_sku

class Package(models.Model):
    title = models.CharField(_('title'), max_length=50)
    sku = models.CharField(_('stock keeping unit'), max_length=20, validators=[validate_sku])
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='packages/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    price = models.PositiveIntegerField(_('price'), default=0)
    duration = models.DurationField(_('duration'), blank=True, null=True)
    gateways = models.ManyToManyField('payments.Gateway')
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    
    class Meta:
        db_table = 'packages'
        verbose_name = _('package')
        verbose_name_plural = _('packages')
        
    def __str__(self) -> str:
        return self.title
    
    
class Subscription(models.Model):
    user = models.ForeignKey('users.User', related_name='%(class)s', on_delete=models.CASCADE)
    package = models.ForeignKey(Package, related_name='%(class)s', on_delete=models.CASCADE)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    expire_time = models.DateTimeField(_('expire time'), blank=True, null=True)
    
    class Meta:
        db_table = 'subscriptions'
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
        
    