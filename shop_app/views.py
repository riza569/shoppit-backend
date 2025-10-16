from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product,Cart,CartItem
from .serializers import ProductSerializer,DetailedProductSerializer,CartItemSerializer,SimpleCartSerializer,CartSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
# Create your views here.

@api_view(["GET"])
def products(request):
    products=Product.objects.all()
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def product_detail(request,slug):
    product=get_object_or_404(Product,slug=slug)
    serializer=DetailedProductSerializer(product)
    return Response(serializer.data)

@api_view(["POST"])
def add_item(request):
    try:
        cart_code=request.data.get("cart_code")
        product_id=request.data.get("product_id")
        
        cart,created=Cart.objects.get_or_create(cart_code=cart_code)
        product=Product.objects.get(id=product_id)
        
        cartitem,created=CartItem.objects.get_or_create(cart=cart,product=product)
        cartitem.quantity=1
        cartitem.save()             
        
        serializer=CartItemSerializer(cartitem)
        return Response({"data":serializer.data,"message":"CartItem Created Succesfully"},status=201)

    except Exception as e:
        return Response({"error":str(e)},status=400)
    
    
@api_view(["GET"])
def product_in_cart(request):
    
    cart_code=request.query_params.get("cart_code")
    product_id=request.query_params.get("product_id")
    
    cart=Cart.objects.get(cart_code=cart_code)
    product=Product.objects.get(id=product_id)
    
    product_exists_in_cart=CartItem.objects.filter(cart=cart,product=product).exists()
    
    return Response({"product_in_cart":product_exists_in_cart})
    
    
@api_view(['GET'])
def get_cart_stat(request):
    """
    Fetches the number of items and total price for a given cart_code.
    Returns 404 if the cart does not exist.
    """
    cart_code = request.GET.get('cart_code')
    
    if not cart_code:
        # Should not happen if frontend is working, but safe practice
        return Response(
            {"detail": "Cart code is required."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Use .get() inside a try-except block, or use get_object_or_404
        cart = Cart.objects.get(cart_code=cart_code)
        
        # Prepare the response data (assuming Cart has these methods/properties)
        data = {
            "num_of_items": cart.items.count(), # Or cart.num_of_items if pre-calculated
            "sum_total": cart.sum_total # Or cart.calculate_total()
        }
        
        return Response(data, status=status.HTTP_200_OK)

    # 💥 CRITICAL FIX: Catch the specific DoesNotExist error
    except Cart.DoesNotExist:
        # Return a graceful 404 response instead of crashing the server
        return Response(
            {"detail": "Cart matching query does not exist."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        # Catch any other unexpected server errors (e.g., database connection issues)
        print(f"Unexpected error in get_cart_stat: {e}")
        return Response(
            {"detail": "An unexpected server error occurred."}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(["GET"])
def get_cart(request):
    cart_code=request.query_params.get('cart_code')
    cart=Cart.objects.get(cart_code=cart_code,paid=False)
    
    serializer=CartSerializer(cart)
    return Response(serializer.data)



@api_view(['PATCH'])
def update_quantity(request):
    
       try:
           cartitem_id=request.data.get("item_id")
           quantity=request.data.get("quantity")
           quantity=int(quantity)
           cartitem=CartItem.objects.get(id=cartitem_id)
           
           cartitem.quantity=quantity
           cartitem.save()
           serializer=CartItemSerializer(cartitem)
           return Response({"data":serializer.data,"message":"Cartitem Updated sucesfully"})
       
       except Exception as e:
           return Response({"error":str(e)},status=400)
           
           
           
@api_view(['DELETE'])
def delete_cart_item(request):
    cartitem_id=request.data.get("item_id")
    cartitem=CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    