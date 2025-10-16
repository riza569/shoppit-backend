from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom Serializer to extend the default JWT payload 
    with the user's username and email.
    """
    @classmethod
    def get_token(cls, user):
        # Call the parent method to get the default token (contains user_id, exp, etc.)
        token = super().get_token(user)

        # CRITICAL: ADD 'username' AND 'email' TO THE PAYLOAD
        # Access the token's claims dictionary and add custom data
        token['username'] = user.username
        token['email'] = user.email
        
        return token
