from django.db import models
from django.utils.text import slugify
import uuid
from django.conf import settings
# Create your models here.
class Product(models.Model):
    CATEGORY = (
        ("Electronics","ELECTRONICS"),
        ("Groceries","GROCERIES"),
        ("Clothings","CLOTHING"),
     )
    name=models.CharField(max_length=100)
    slug=models.SlugField(blank=True,null=True)
    image=models.ImageField(upload_to="img")
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.CharField(max_length=15,choices=CATEGORY,blank=True,null=True)
    
    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        
        if not self.slug:
            base_slug=slugify(self.name)
            unique_id=uuid.uuid4().hex[:6]
            self.slug=f'{base_slug}-{unique_id}'
        super().save(*args, **kwargs)
        
        
class Cart(models.Model):
    cart_code=models.CharField(max_length=11,unique=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
    paid=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    modified_at=models.DateTimeField(auto_now=True,blank=True,null=True)
    
    def __str__(self):
        return self.cart_code
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart {self.cart.id}"