from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField

User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name="Kateqoriya",
                            max_length=255,
                            unique=True)
    image = models.ImageField(verbose_name='Şəkil',
                              null=True, blank=True, default='')
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = "Kateqoriya"
        verbose_name_plural = "Kateqoriyalar"

    def get_absolute_url(self):
        return reverse("shop:categories", args=[self.slug])

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product_type = models.ForeignKey(Category, on_delete=models.RESTRICT)

    name = models.CharField(verbose_name="Ad", max_length=255)

    class Meta:
        verbose_name = 'Məhsulun xüsusiyyəti'
        verbose_name_plural = 'Məhsulun xüsusiyyətləri'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(verbose_name="Ad", max_length=255)
    description = RichTextField(verbose_name='Məzmun', blank=True)
    slug = AutoSlugField(populate_from='title')
    favourites = models.ManyToManyField(
        User, related_name='favourites', default=None, blank=True)
    price = models.DecimalField(
        verbose_name="Qiymət", max_digits=5, decimal_places=2)

    discount_price = models.DecimalField(
        verbose_name="Endirimli qiymət", max_digits=5, decimal_places=2, null=True, blank=True, default=None)

    is_active = models.BooleanField(
        verbose_name="Məhsulun aktivliyi", default=True)

    created_at = models.DateTimeField(
        verbose_name='Əlavə edilmə tarixi', auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(
        verbose_name='Yenilənmə tarixi', auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = 'Məhsul'
        verbose_name_plural = 'Məhsullar'

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.slug])

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(
        ProductSpecification, on_delete=models.RESTRICT)

    value = models.CharField(verbose_name='Value', max_length=255)

    class Meta:
        verbose_name = 'Məhsulun xüsusiyyətinin dəyəri'
        verbose_name = 'Məhsulun xüsusiyyətinin dəyərləri'

    def __str__(self):
        return self.value


def get_image_filename(instance, filename):
    id = instance.product.id
    title = instance.product
    extension = filename.split('.')[-1]
    return "laptops/%s_%s.%s" % (title, id, extension)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='photo')

    image = models.ImageField(verbose_name='Şəkil', null=True, blank=True,
                              upload_to=get_image_filename)

    alt_text = models.CharField(
        verbose_name='Alternativ text', max_length=50, null=True, blank=True)

    is_feature = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)

    def get_first_image(self):
        return self.image

    class Meta:
        verbose_name = 'Məhsulun şəkili'
        verbose_name_plural = 'Məhsulun şəkilləri'
