from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer 
from . models import User


#Because i'm using a custom Model 
class CustomRegistrationSerializer(RegisterSerializer):
    class Meta:
        model = User
        fields = ('email','first_name','last_name','phone_number')


class CustomLoginSerializer(LoginSerializer):
    username = None; 
    
    def _validate_username(self, username,password):    
        pass; 

