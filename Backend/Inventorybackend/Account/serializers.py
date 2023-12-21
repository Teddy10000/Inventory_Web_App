from dj_rest_auth.registration.serializers import RegisterSerializer 
from . models import User


#Because i'm using a custom Model 
class CustomRegistrationSerializer(RegisterSerializer):
    class Meta:
        model = User
        fields = ('email','first_name','last_name','phone_number')



