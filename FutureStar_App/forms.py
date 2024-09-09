from django import forms
from .models import *
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import password_validation


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))



# User Form
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'role', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'role': forms.Select(attrs={'placeholder': 'Select role'}),
            'is_active': forms.CheckboxInput(),
            'is_staff': forms.CheckboxInput(),
        }
        
 
# Role Form
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter role name'}),
        }

# User Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name'}),
        }

# System Settings Form
class SystemSettingsForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = [
            'fav_icon', 'footer_logo', 'header_logo', 'website_name_english',
            'website_name_arabic', 'phone', 'email', 'address',
            'instagram', 'facebook', 'snapchat', 'linkedin', 'youtube'
        ]
        widgets = {
            'website_name_english': forms.TextInput(attrs={'placeholder': 'Website Name in English'}),
            'website_name_arabic': forms.TextInput(attrs={'placeholder': 'Website Name in Arabic'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter physical address', 'rows': 3}),
            'fav_icon': forms.TextInput(attrs={'placeholder': 'Favicon URL'}),
            'footer_logo': forms.TextInput(attrs={'placeholder': 'Footer logo URL'}),
            'header_logo': forms.TextInput(attrs={'placeholder': 'Header logo URL'}),
            'instagram': forms.URLInput(attrs={'placeholder': 'Instagram URL'}),
            'facebook': forms.URLInput(attrs={'placeholder': 'Facebook URL'}),
            'snapchat': forms.URLInput(attrs={'placeholder': 'Snapchat URL'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'LinkedIn URL'}),
            'youtube': forms.URLInput(attrs={'placeholder': 'YouTube URL'}),
        }
#user_profile
class UserUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'role', 'profile_picture', 'card_header']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            field.required = False


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control",
            }
        ),
    )
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),  # type: ignore
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )
    



# Gender Form
class GenderForm(forms.ModelForm):
    class Meta:
        model = UserGender
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter UserGender'}),
        }


# GameType Form
class GameTypeForm(forms.ModelForm):
    class Meta:
        model = GameType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter GameType'}),
        }


# Field Capacity Form
class FieldCapacityForm(forms.ModelForm):
    class Meta:
        model = FieldCapacity
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Field Capacity'}),
        }


# Ground Material Form
class GroundMaterialForm(forms.ModelForm):
    class Meta:
        model = GroundMaterial
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Ground Material'}),
        }

# Tournament Style Form
class TournamentStyleForm(forms.ModelForm):
    class Meta:
        model = TournamentStyle
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Tournament Style'}),
        }

# Event Type Style Form
class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Event Type'}),
        }