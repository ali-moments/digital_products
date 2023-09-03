from django.db import models
from django.utils.translation import gettext_lazy

class Category(models.Model):
    parent = models.ForeignKey('self', verbose_name=gettext_lazy('parent'), blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=gettext_lazy('title'), max_length=50)
    description = models.TextField(verbose_name=gettext_lazy('description'), blank=True)
    avatar = models.ImageField(verbose_name=gettext_lazy('avatar'), blank=True, upload_to='categories/')
    is_enable = models.BooleanField(verbose_name=gettext_lazy('is enable'), default=True)
    create_time = models.DateTimeField(verbose_name=gettext_lazy('created time'), auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=gettext_lazy('updated time'), auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = gettext_lazy('Category')
        verbose_name_plural = gettext_lazy('Categories')

    def __str__(self) -> str:
        return self.title

class Product(models.Model):
    title = models.CharField(verbose_name=gettext_lazy('title'), max_length=50)
    description = models.TextField(verbose_name=gettext_lazy('description'), blank=True)
    avatar = models.ImageField(verbose_name=gettext_lazy('avatar'), blank=True, upload_to='products/')
    is_enable = models.BooleanField(verbose_name=gettext_lazy('is enable'), default=True)
    categories = models.ManyToManyField('Category', verbose_name=gettext_lazy('categories'), blank=True)
    create_time = models.DateTimeField(verbose_name=gettext_lazy('created time'), auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=gettext_lazy('updated time'), auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = gettext_lazy('Product')
        verbose_name_plural = gettext_lazy('Products')
    
    def __str__(self) -> str:
        return self.title

class File(models.Model):
    FILE_AUDIO = 1
    FILE_VIDEO = 2
    FILE_PDF = 3
    FILE_TYPES = (
        (FILE_AUDIO, gettext_lazy('audio')),
        (FILE_VIDEO, gettext_lazy('video')),
        (FILE_PDF, gettext_lazy('pdf')),
    )
    product = models.ForeignKey('Product', verbose_name=gettext_lazy('products'), related_name='files' , on_delete=models.CASCADE)
    title = models.CharField(verbose_name=gettext_lazy('title'), max_length=50)
    file_type = models.PositiveSmallIntegerField(verbose_name=gettext_lazy('file type'), choices=FILE_TYPES, blank=True, null=True)
    file = models.FileField(verbose_name=gettext_lazy('file'), upload_to='files/%Y/%m/%d/')
    is_enable = models.BooleanField(verbose_name=gettext_lazy('is enable'), default=True)
    create_time = models.DateTimeField(verbose_name=gettext_lazy('created time'), auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=gettext_lazy('updated time'), auto_now=True)

    class Meta:
        db_table = 'files'
        verbose_name = gettext_lazy('File')
        verbose_name_plural = gettext_lazy('Files')

    def __str__(self) -> str:
        return self.title
    