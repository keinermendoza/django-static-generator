from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core.utils import download_avatar

User = get_user_model()

class MyAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        # Si ya existe un usuario con ese email vinculado a un proveedor
        from django.contrib.auth import get_user_model

        try:
            existing_user = User.objects.get(email__iexact=email)
            social = SocialAccount.objects.filter(user=existing_user).first()
            if social:
                # Lanza un error más claro
                raise ValidationError(
                    f"Você já tem uma conta com este e-mail pelo {social.provider.capitalize()}. "
                    f"Entre com o {social.provider.capitalize()} para continuar."
                )
        except User.DoesNotExist:
            pass

        return super().clean_email(email)
    
    def authenticate(self, request, **credentials):
        """
        Intercepta tentativas de login com senha em contas sociais.
        """
        email = credentials.get('email')
        if email:
            try:
                user = User.objects.get(email__iexact=email)
                social = SocialAccount.objects.filter(user=user).first()
                if social and not user.has_usable_password():
                    raise ValidationError(
                        _(f"Esta conta está vinculada ao {social.provider.capitalize()}. "
                          f"Acesse com o {social.provider.capitalize()} em vez de usar senha.")
                    )
            except User.DoesNotExist:
                pass

        return super().authenticate(request, **credentials)
    
class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = None
        email = sociallogin.user.email

        if not email:
            return

        # Verifica si existe ya un usuario con ese email
        try:
            user = User.objects.get(email=email)

            # Busca si ya tiene una cuenta social asociada
            social = SocialAccount.objects.filter(user=user).first()
            if social:
                if social.provider != sociallogin.account.provider:
                    raise ValidationError(
                        f"Você já tem uma conta com este e-mail pelo {social.provider.capitalize()}. "
                        f"Entre com o {social.provider.capitalize()} para continuar."
                    )

            # Vincula el proveedor a la cuenta existente
            else:
                sociallogin.connect(request, user)
            
        except User.DoesNotExist:
            user = sociallogin.user
        
        # retive extra data
        provider = sociallogin.account.provider
        data = sociallogin.account.extra_data

        if provider in ["github", "google"]:
            # retrive profile image
            if not user._profile_image:
                match provider:
                    case "github":
                        avatar_url = data.get("avatar_url")
                        download_avatar(user, avatar_url)

                    case "google":
                        avatar_url = data.get("picture")
                        download_avatar(user, avatar_url)
            
            # retrive user name
            if not user.name:
                match provider:
                    case "github":
                        user.name = data.get("login")
                        print("in github de name was", user.name)
                    case "google":
                        user.name = data.get("email").split("@")[0]
                user.save()