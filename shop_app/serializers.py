from rest_framework import serializers
from .models import Product,Cart,CartItem
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','slug','image','description','category','price']
        

class DetailedProductSerializer(serializers.ModelSerializer):
    similar_products=serializers.SerializerMethodField(method_name='get_similar_products')
    class Meta:
        model=Product
        fields=['id','name','slug','image','description','price','similar_products']
        
    def get_similar_products(self,product:Product):
        products=Product.objects.filter(category=product.category).exclude(id=product.id)
        serializer=ProductSerializer(products,many=True)
        return serializer.data
    
    

class CartItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    total=serializers.SerializerMethodField(method_name='get_total')
    class Meta:
        model=CartItem
        fields=['id',"quantity","product","cart","total"]
        
    def get_total(self,cartitem):
        price=cartitem.product.price*cartitem.quantity
        return price
    
    
    
class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(read_only=True,many=True)
    num_of_items=serializers.SerializerMethodField(method_name='get_number_of_items')
    sum_total=serializers.SerializerMethodField(method_name='get_sum_total')
    class Meta:
        model=Cart
        fields=['id','cart_code','sum_total','created_at','modified_at','items','num_of_items']
    
    def get_sum_total(self,cart:Cart):
        
        items=cart.items.all()
        total=sum([item.product.price*item.quantity for item in items])
        return total
    
    def get_number_of_items(self,cart:Cart):
        items=cart.items.all()
        total=sum([item.quantity for item in items])
        return total
        
class SimpleCartSerializer(serializers.ModelSerializer):
    num_of_items=serializers.SerializerMethodField(method_name='get_number_of_items')
    class Meta:
        model=Cart
        fields=['id',"cart_code","num_of_items"]
        
    def get_number_of_items(self,cart:Cart):
        num_of_items=sum([item.quantity for item in cart.items.all()])
        return num_of_items