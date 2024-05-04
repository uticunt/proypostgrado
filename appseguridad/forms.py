from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from django.contrib.auth.forms import UserCreationForm

#-------------------------------------- Formulario para Crear Uusario-------------------------------------
class CrearUserForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Nombres (opcional)', required=False)
    last_name = forms.CharField(label='Apellidos (opcional)', required=False)
    email = forms.EmailField(label='Correo Electrónico (opcional)', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_active']
        help_texts = {
            'is_active': ('Indica si este usuario debe ser tratado como activo. Desactive esto en lugar de eliminar cuentas.'),
            'is_superuser': ('Designa que este usuario tiene todos los permisos sin asignarlos explícitamente.'),
        }

    def __init__(self, *args, **kwargs):
        super(CrearUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
#-------------------------------Formulario para Editar Uusario----------------------------------
class EditarUserForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_active']
        help_texts = {
            'is_active': ('Indica si este usuario debe ser tratado como activo. Desactive esto en lugar de eliminar cuentas.'),
            'is_superuser': ('Designa que este usuario tiene todos los permisos sin asignarlos explícitamente.'),
        }

# ------------------------- Formulario para Perfil del Usuario----------------------------
class PerfilrUserForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',]
        widgets = {              
            'username': forms.TextInput(attrs={'readonly': True}),       
        }
        help_texts = {
            'email': ('Proporcione el correo electronico al cual desea que le lleguen sus credenciales.'),
        }
       
              
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('password', css_class='passwordinput form-control'),
                Div(
                    Field('password', placeholder="Contraseña", css_class='form-control'),
                    css_class='input-group'
                ),
                Div(
                    Div(
                        Field('password', css_class='passwordinput form-control'),
                        css_class='input-group-prepend'
                    ),
                    css_class='input-group'
                ),
            )
        )