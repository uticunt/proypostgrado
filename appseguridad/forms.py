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

# ------------------------- Formulario para Envio de Credenciales  ----------------------------
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        if name in files:
            return files.getlist(name)
        return []

class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        return data

class CorreoForm(forms.Form):
    asunto = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}),
        initial='ACCESO AL MODULO DE EVALUACIÓN CURRICULAR PROCESO DE ADMISIÓN 2024-I',
        label='Asunto')
    encabezado = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}),
        initial='¡Bienvenido al Modulo de Evaluacion curricular de la Escuela de Posgrado del proceso de admisión 2024-I!',
        label='Titulo')
    nombre = forms.CharField(label='Nombre')   
    contenido = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 40}),
        initial=' Se ha remitido a todos los Jurados Evaluadores para el proceso de Admisión 2024 - I; el cual ha sido dirigido y registrado en el sistema de evaluación curricular por parte del comité de admisión de la Escuela de Posgrado. En el siguiente enlace podrá registrar y evaluar la calificación según los rangos e indicadores registrados en el reglamento de admisión 2024-I.',
        label='Contenido')

