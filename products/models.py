from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('title'), max_length=50)
    description = models.TextField(verbose_name=_('description'), blank=True)
    avatar = models.ImageField(verbose_name=_('avatar'), blank=True, upload_to='categories/')
    is_enable = models.BooleanField(verbose_name=_('is enable'), default=True)
    create_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self) -> str:
        return self.title

class Product(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=50)
    description = models.TextField(verbose_name=_('description'), blank=True)
    avatar = models.ImageField(verbose_name=_('avatar'), blank=True, upload_to='products/')
    is_enable = models.BooleanField(verbose_name=_('is enable'), default=True)
    categories = models.ManyToManyField('Category', verbose_name=_('categories'), blank=True)
    create_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
    
    def __str__(self) -> str:
        return self.title

class File(models.Model):
    FILE_AUDIO = 1
    FILE_VIDEO = 2
    FILE_PDF = 3
    FILE_TYPES = (
        (FILE_AUDIO, _('audio')),
        (FILE_VIDEO, _('video')),
        (FILE_PDF, _('pdf')),
    )
    product = models.ForeignKey('Product', verbose_name=_('products'), related_name='files' , on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('title'), max_length=50)
    file_type = models.PositiveSmallIntegerField(verbose_name=_('file type'), choices=FILE_TYPES, blank=True, null=True)
    file = models.FileField(verbose_name=_('file'), upload_to='files/%Y/%m/%d/')
    is_enable = models.BooleanField(verbose_name=_('is enable'), default=True)
    create_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        db_table = 'files'
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def __str__(self) -> str:
        return self.title
    