from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Ngo(models.Model):
    name = models.CharField(max_length=255, default="No Name")
    contact_no = models.CharField(max_length=20, default="000 000 000 00")
    contact_email = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(default="No description available for this ngo.")

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "NGO"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('admins:ngo-update', kwargs={'pk': self.pk})


class ProjectType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description available.")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Projects Types"

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('admins:projecttype-detail', kwargs={'pk': self.pk})


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description available.")
    slug = models.SlugField(max_length=100, null=False, blank=True, unique=True)
    project_type = models.ForeignKey('ProjectType', on_delete=models.SET_NULL, null=True, blank=False)
    required_amount = models.FloatField(default=1000)
    donation_amount = models.FloatField(default=0)
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Donation(models.Model):
    PAYMENT_METHOD_CHOICE = (
        ('Stripe', 'Stripe'),
        )
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=False)
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=False)
    payment_method = models.CharField(max_length=10, default='s', choices=PAYMENT_METHOD_CHOICE)
    amount = models.FloatField(default=0,max_length=6)
    transaction_id = models.CharField(
        max_length=1000, null=False, blank=False,
        help_text="Enter transaction id here, transaction id will be provided by your service provider "
                  "i.e EasyPaisa provide you through sms over a successful transaction", unique=True
    )
    stripe_id = models.CharField(max_length=500,null=True,blank=True)
    is_paid = models.BooleanField(default=False)
    is_completed = models.BooleanField(
        default=False, help_text="Make Sure you are careful about this check? If you check this it will mark this "
                                 "transaction as successful verified so if user has paid then you can check this."
    )

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Donations"

    def __str__(self):
        return str(self.pk)
