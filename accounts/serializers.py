from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'confirm_password', 'email', 'phone_number', 'first_name', 'last_name']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if not all(attrs.get(field) for field in ['username', 'email', 'phone_number', 'first_name', 'last_name']):
            raise serializers.ValidationError('All fields are required.')
        
        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user



# class TokenLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')

#         if not username or not password:
#             raise serializers.ValidationError('Both username and password are required.')

#         user = authenticate(username=username, password=password)
#         if not user:
#             raise serializers.ValidationError('Invalid credentials, please try again.')

#         attrs['user'] = user
#         return attrs