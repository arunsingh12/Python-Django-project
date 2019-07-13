from django.db import models
from django.urls import reverse

class Ureg(models.Model):

    ufname = models.CharField(max_length=20)
    usname = models.CharField(max_length=20)
    uname = models.CharField(max_length=20)
    umail = models.EmailField()
    upass = models.CharField(max_length=20)
    uphone = models.CharField(max_length=10)
    uaddr = models.TextField()
    utype = models.CharField(max_length=10, default='costumer')

    def __str__(self):
        return self.uname

class Product(models.Model):

    Prod_title = models.CharField(max_length=100)
    Prod_pmail = models.EmailField()
    Prod_model_no = models.CharField(max_length=10)
    Prod_manufacture = models.CharField(max_length=20)
    Prod_weight = models.CharField(max_length=20)
    Prod_no_of_items = models.IntegerField()
    Prod_price = models.IntegerField()
    Prod_description = models.TextField()
    Prod_year = models.CharField(max_length=4)
    Prod_image = models.ImageField(upload_to='', blank=True)
    Prod_genre = models.TextField(max_length=50)
    Prod_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.Prod_title

    def get_absolute_url(self):
        return reverse('retrive', kwargs={"id": self.id})

class Cate(models.Model):
    cate_name = models.CharField(max_length=100)
    cate_img = models.ImageField(upload_to='')

    def __str__(self):
        return self.cate_name

class Prodcomm(models.Model):
    Prod_title = models.CharField(max_length=100)
    Prod_umail = models.EmailField(blank=True,null=True)
    Prod_com = models.TextField()

    def __str__(self):
        return self.Prod_title

class Rating(models.Model):
    rumail = models.CharField(max_length=30)
    rtitle = models.CharField(max_length=100)
    rval = models.IntegerField(default=0)

    def __str__(self):
        return self.rtitle


class Cart(models.Model):
    c_Prod_id = models.IntegerField()
    c_Prod_title = models.CharField(max_length=100)
    c_Prod_mail = models.EmailField()
    cno = models.IntegerField(default=1)
    ccost = models.IntegerField(default=0)
    cstat = models.CharField(default='no',max_length=3)
    cdeli = models.CharField(default='no',max_length=3)

    def __str__(self):
        return self.c_Prod_title






