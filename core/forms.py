from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .widgets import CustomPasswordInput
from allauth.account.forms import SignupForm

User = get_user_model()
 
class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=80, label='Nome completo')

    def save(self, request):
        user = super().save(request)
        user.name = self.cleaned_data['name']        
        user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ahora puedes personalizar los widgets
        self.fields['password1'].widget = CustomPasswordInput()
        self.fields['password2'].widget = CustomPasswordInput()

        self.fields['name'].widget.attrs.update({
            'placeholder': 'Seu nome',
        })
        self.fields['password1'].widget.attrs.update({'placeholder': 'Digite sua senha'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repita sua senha'})
    

# class LoginCustomUser(AuthenticationForm):
#     password = forms.CharField(
#         label="Introduce tu Contraseña",
#         widget=CustomPasswordInput
#     ) 
# class EditCustomUserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ["nombre", "apellido", "_profile_image", "telefono"]

# class RegisterCustomUser(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ["email", "username", "password1", "password2"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['password1'].widget = CustomPasswordInput()
#         self.fields['password2'].widget = CustomPasswordInput()

#     def save(self, commit=True):
#         """
#         Agregado temporalmente hasta implementar la validacion por email con SMTP
#         """
#         # instancia en memoria
#         user = super().save(commit=False) 
        
#         # normalizo el dominio del email
#         email = self.cleaned_data["email"]
#         user.email = self.Meta.model.objects.normalize_email(email) 
        
#         # temporalmente activando usuario al crear
#         user.is_active = True 
        
#         user.save() 
#         return user

