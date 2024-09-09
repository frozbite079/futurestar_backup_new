import re
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import *
from .models import *
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash


def custom_404_view(request, exception):
    messages.error(request, "The page you're looking for was not found.")
    return redirect('login')

# Login View

class LoginView(View):
    template_name = 'login.html'



    def get(self, request):
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if not form.is_valid():
            # Add a message if the form is not valid due to blank fields
            if not form.cleaned_data.get('username'):
                messages.error(request, 'Username cannot be blank.')
            if not form.cleaned_data.get('password'):
                messages.error(request, 'Password cannot be blank.')
            if form.cleaned_data.get('username') and form.cleaned_data.get('password'):
                messages.error(request, 'Please correct the errors below.')

            return render(request, self.template_name, {'form': form})

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')


        return render(request, self.template_name, {'form': form})

#User Crud
class UserListView(LoginRequiredMixin, View):
    template_name = 'admin/user.html'

    def get(self, request):
        User = get_user_model()  # Get the custom user model
        users = User.objects.all()
        roles = Role.objects.all()
        return render(request, self.template_name,
        {
            'users': users,
            'roles': roles,
            'breadcrumb': {
                'parent': 'Admin',
                'child': 'User List'
        }})


class UserUpdateView(LoginRequiredMixin,View):
    template_name = 'forms/user_form.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} was successfully updated.')
            return redirect('user_list')  # Redirect to the user list after successful update
        else:
            messages.error(request, 'There was an error updating the user.')
        return render(request, self.template_name, {'form': form})


class UserDeleteView(LoginRequiredMixin,View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        messages.success(request, f'User {user.username} was successfully deleted.')
        return redirect('user_list')  # Redirect to the user list after successful deletion

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        messages.success(request, f'User {user.username} was successfully deleted.')
        return redirect('user_list')  # Redirect to the user list after successful deletion



# Role CRUD Views
class RoleCreateView(LoginRequiredMixin,View):
    def get(self, request):
        form = RoleForm()
        return render(request, 'forms/role_form.html', {'form': form})

    def post(self, request):
        form = RoleForm(request.POST)
        if form.is_valid():
            # Check for existing role with the same name
            name = form.cleaned_data.get('name')
            if Role.objects.filter(name=name).exists():
                messages.error(request, 'A role with this name already exists.')
                return redirect('role_list')  # Redirect back to role_list with an error message
            form.save()
            messages.success(request, 'Role was successfully created.')
            return redirect('role_list')
        else:
            messages.error(request, 'There was an error creating the role. Please ensure all fields are filled out correctly.')
        return redirect('role_list')
class RoleUpdateView(LoginRequiredMixin,View):
    template_name = 'forms/role_form.html'

    def get(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        form = RoleForm(instance=role)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            # Check for existing role with the same name but different pk
            name = form.cleaned_data.get('name')
            if Role.objects.filter(name=name).exclude(pk=pk).exists():
                messages.error(request, 'A role with this name already exists.')
                return render(request, self.template_name, {'form': form})
            form.save()
            messages.success(request, 'Role was successfully updated.')
            return redirect('role_list')
        else:
            messages.error(request, 'There was an error updating the role. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})


class RoleDeleteView(LoginRequiredMixin,View):
    def get(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        role.delete()
        messages.success(request, 'Role was successfully deleted.')
        return redirect('role_list')

    def post(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        role.delete()
        messages.success(request, 'Role was successfully deleted.')
        return redirect('role_list')

class RoleListView(LoginRequiredMixin,View):
    template_name = 'admin/role.html'

    def get(self, request):
        roles = Role.objects.all()
        return render(request, self.template_name,
                       {
                            'roles': roles,
                            'breadcrumb': {
                               'parent': 'Admin',
                               'child': 'Role'
                           }

                           })


# Category CRUD Views

class CategoryCreateView(LoginRequiredMixin,View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'forms/category_form.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Check for existing category with the same name
            name = form.cleaned_data.get('name')
            if Category.objects.filter(name=name).exists():
                messages.error(request, 'A category with this name already exists.')
                return redirect('category_list')  # Redirect back to category_list with an error message
            form.save()
            messages.success(request, 'Category was successfully created.')
            return redirect('category_list')
        else:
            messages.error(request, 'There was an error creating the category. Please ensure all fields are filled out correctly.')
        return redirect('category_list')

class CategoryUpdateView(LoginRequiredMixin,View):
    template_name = 'forms/category_form.html'

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category was successfully updated.')
            return redirect('category_list')
        else:
            messages.error(request, 'There was an error updating the category. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})


class CategoryDeleteView(LoginRequiredMixin,View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, 'Category was successfully deleted.')
        return redirect('category_list')

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, 'Category was successfully deleted.')
        return redirect('category_list')

class CategoryListView(LoginRequiredMixin,View):
    template_name = 'admin/category.html'

    def get(self, request):
        categories = Category.objects.all()
        return render(request, self.template_name,
                      {
                        'categories': categories,
                         'breadcrumb': {
                               'parent': 'Admin',
                               'child': 'Category'
                           }

            })


# System Settings View (Assuming there's only one instance)
PHONE_REGEX = re.compile(r'^\+?1?\d{9,15}$')

class System_Settings(LoginRequiredMixin, View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        system_settings = SystemSettings.objects.first()  # Fetch the first record
        return render(request, 'admin/System_Settings.html', {
            'system_settings': system_settings,
            'MEDIA_URL': settings.MEDIA_URL,  # Pass MEDIA_URL to the template

            'breadcrumb': {
                'parent': 'Admin',
                'child': 'System Settings',

        }
        })

    def post(self, request, *args, **kwargs):
        system_settings = SystemSettings.objects.first()
        if not system_settings:
            system_settings = SystemSettings()

        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'System_Settings'))

        # Validation flags
        errors = []

        # Handle fav_icon
        if 'fav_icon' in request.FILES:
            if system_settings.fav_icon:
                old_fav_icon_path = os.path.join(settings.MEDIA_ROOT, system_settings.fav_icon)
                if os.path.isfile(old_fav_icon_path):
                    os.remove(old_fav_icon_path)
            fav_icon_file = request.FILES['fav_icon']
            fav_icon_filename = 'favicon.jpg'
            fs.save(fav_icon_filename, fav_icon_file)
            system_settings.fav_icon = os.path.join('System_Settings', fav_icon_filename)
        else:
            errors.append("Fav Icon is required.")

        # Handle footer_logo
        if 'footer_logo' in request.FILES:
            if system_settings.footer_logo:
                old_footer_logo_path = os.path.join(settings.MEDIA_ROOT, system_settings.footer_logo)
                if os.path.isfile(old_footer_logo_path):
                    os.remove(old_footer_logo_path)
            footer_logo_file = request.FILES['footer_logo']
            footer_logo_filename = 'footer_logo.jpg'
            fs.save(footer_logo_filename, footer_logo_file)
            system_settings.footer_logo = os.path.join('System_Settings', footer_logo_filename)
        else:
            errors.append("Footer Logo is required.")

        # Handle header_logo
        if 'header_logo' in request.FILES:
            if system_settings.header_logo:
                old_header_logo_path = os.path.join(settings.MEDIA_ROOT, system_settings.header_logo)
                if os.path.isfile(old_header_logo_path):
                    os.remove(old_header_logo_path)
            header_logo_file = request.FILES['header_logo']
            header_logo_filename = 'header_logo.jpg'
            fs.save(header_logo_filename, header_logo_file)
            system_settings.header_logo = os.path.join('System_Settings', header_logo_filename)
        else:
            errors.append("Header Logo is required.")

        # Save other fields with validation
        system_settings.website_name_english = request.POST.get('website_name_english')
        system_settings.website_name_arabic = request.POST.get('website_name_arabic')
        system_settings.phone = request.POST.get('phone')
        system_settings.email = request.POST.get('email')
        system_settings.address = request.POST.get('address')
        system_settings.instagram = request.POST.get('instagram')
        system_settings.facebook = request.POST.get('facebook')
        system_settings.snapchat = request.POST.get('snapchat')
        system_settings.linkedin = request.POST.get('linkedin')
        system_settings.youtube = request.POST.get('youtube')

        # Validate email format
        email_validator = EmailValidator()
        try:
            email_validator(system_settings.email)
        except ValidationError:
            errors.append("Invalid email format.")

        # Validate phone number format
        if not PHONE_REGEX.match(system_settings.phone):
            errors.append("Invalid phone number format.")

        # Validate social media URLs
        if not system_settings.instagram:
            errors.append("Instagram URL is required.")
        if not system_settings.facebook:
            errors.append("Facebook URL is required.")
        if not system_settings.snapchat:
            errors.append("Snapchat URL is required.")
        if not system_settings.linkedin:
            errors.append("LinkedIn URL is required.")
        if not system_settings.youtube:
            errors.append("YouTube URL is required.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'admin/system_settings.html', {
                'system_settings': system_settings,
                'MEDIA_URL': settings.MEDIA_URL,  # Pass MEDIA_URL to the template
            })

        system_settings.save()
        messages.success(request, "System settings updated successfully.")
        return redirect('home')

class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "Logout successful.")
        else:
            messages.error(request, "User not authenticated.")

        # Redirect to the login page after logout (or any other desired URL)
        return redirect("/")

# Error 404 html
class ErrorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "error.html")



class Dashboard(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        context = {
            'breadcrumb': {
                'parent': 'Admin',
                'child': 'Home'
        }
        }
        return render(request,'index.html',context)

    def post(self, request, *args, **kwargs):
        return render(request,'index.html')

class ToggleUserStatusView(LoginRequiredMixin,View):
    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        new_status = request.POST.get('status')

        # Check if the user is a superuser
        if user.is_superuser:
            messages.error(request, 'Superuser status cannot be changed.')
            return redirect('user_list')

        # Check if the current user is trying to deactivate their own account
        if user == request.user and new_status == 'deactivate':
            messages.info(request, 'Your account has been deactivated. Please log in again.')
            user.is_active = False
            user.save()
            return redirect(reverse('login'))

        # Update the user's status
        if new_status == 'activate':
            user.is_active = True
            messages.success(request, f'{user.username} has been activated.')
        elif new_status == 'deactivate':
            user.is_active = False
            messages.success(request, f'{user.username} has been deactivated.')

        user.save()

        return redirect('user_list')


#user_profile
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {
            'user': user,
            'breadcrumb': {
                'parent': 'Acccount',
                'child': 'Profile'

            }}

        return render(request, 'forms/user_profile.html', context)

    def post(self, request):
        user = request.user

        return render(request, 'forms/user_profile.html', {'user': user} )


@method_decorator(login_required, name='dispatch')
class UserUpdateProfileView(View):
    def get(self, request, *args, **kwargs):
        form = UserUpdateProfileForm(instance=request.user)
        password_change_form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'forms/edit_profile.html', {
            'form': form,
            'password_change_form': password_change_form,
            'breadcrumb': {
                'parent': 'Acccount',
                'child': 'Edit Profile'
            }



        }

        )

    def post(self, request, *args, **kwargs):
        if 'change_password' in request.POST:
            # Handle password change
            password_change_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_change_form.is_valid():
                user = password_change_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your password has been changed successfully. Please log in again.")
                return redirect('login')
            else:
                for field in password_change_form:
                    for error in field.errors:
                        messages.error(request, error)
                form = UserUpdateProfileForm(instance=request.user)
                return render(request, 'forms/edit_profile.html', {
                    'form': form,
                    'password_change_form': password_change_form
                })
        else:
            # Handle profile update
            user = request.user
            old_profile_picture = user.profile_picture
            old_card_header = user.card_header

            form = UserUpdateProfileForm(request.POST, instance=user, files=request.FILES)
            if form.is_valid():
                # Handle profile picture update
                if 'profile_picture' in request.FILES:
                    if old_profile_picture and os.path.isfile(os.path.join(settings.MEDIA_ROOT, str(old_profile_picture))):
                        os.remove(os.path.join(settings.MEDIA_ROOT, str(old_profile_picture)))
                elif 'profile_picture-clear' in request.POST:
                    user.profile_picture = None

                # Handle card header update
                if 'card_header' in request.FILES:
                    if old_card_header and os.path.isfile(os.path.join(settings.MEDIA_ROOT, str(old_card_header))):
                        os.remove(os.path.join(settings.MEDIA_ROOT, str(old_card_header)))
                elif 'card_header-clear' in request.POST:
                    user.card_header = None

                user = form.save()
                messages.success(request, "Your profile has been updated successfully.")
                return redirect('edit_profile')
            else:
                for field in form:
                    for error in field.errors:
                        messages.error(request, error)
                password_change_form = CustomPasswordChangeForm(user=request.user)
                return render(request, 'forms/edit_profile.html', {
                    'form': form,
                    'password_change_form': password_change_form
                })

# Gender CRUD Views
class GenderCreateView(LoginRequiredMixin,View):
    template_name = 'forms/gender_form.html'

    def get(self, request):
        form = GenderForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = GenderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gender created successfully.')
            return redirect('gender_list')
        messages.error(request, 'There was an error creating the gender. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})

class GenderUpdateView(LoginRequiredMixin,View):
    template_name = 'forms/gender_form.html'

    def get(self, request, pk):
        gender = get_object_or_404(UserGender, pk=pk)
        form = GenderForm(instance=gender)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        gender = get_object_or_404(UserGender, pk=pk)
        form = GenderForm(request.POST, instance=gender)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gender was successfully updated.')
            return redirect('gender_list')
        messages.error(request, 'There was an error updating the gender. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})

class GenderDeleteView(LoginRequiredMixin,View):
    def get(self, request, pk):
        gender = get_object_or_404(UserGender, pk=pk)
        gender.delete()
        messages.success(request, 'Gender was successfully deleted.')
        return redirect('gender_list')

    def post(self, request, pk):
        gender = get_object_or_404(UserGender, pk=pk)
        gender.delete()
        messages.success(request, 'Gender was successfully deleted.')
        return redirect('gender_list')

class GenderListView(LoginRequiredMixin,View):
    template_name = 'admin/General_Settings/Gender.html'

    def get(self, request):
        genders = UserGender.objects.all()
        return render(request, self.template_name,
                      {
                          'genders': genders,
                          'breadcrumb': {
                                          'parent': 'General Settings',
                                          'child': 'Gender'
                                          }

                          })




# GameType CRUD Views
class GameTypeCreateView(LoginRequiredMixin, View):
    template_name = 'forms/gametype_form.html'

    def get(self, request):
        form = GameTypeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = GameTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Game type created successfully.')
            return redirect('gametype_list')
        messages.error(request, 'There was an error creating the game type. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})

class GameTypeUpdateView(LoginRequiredMixin, View):
    template_name = 'forms/gametype_form.html'

    def get(self, request, pk):
        gametype = get_object_or_404(GameType, pk=pk)
        form = GameTypeForm(instance=gametype)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        gametype = get_object_or_404(GameType, pk=pk)
        form = GameTypeForm(request.POST, instance=gametype)
        if form.is_valid():
            form.save()
            messages.success(request, 'Game type was successfully updated.')
            return redirect('gametype_list')
        messages.error(request, 'There was an error updating the game type. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})

class GameTypeDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        gametype = get_object_or_404(GameType, pk=pk)
        gametype.delete()
        messages.success(request, 'Game type was successfully deleted.')
        return redirect('gametype_list')

    def post(self, request, pk):
        gametype = get_object_or_404(GameType, pk=pk)
        gametype.delete()
        messages.success(request, 'Game type was successfully deleted.')
        return redirect('gametype_list')

class GameTypeListView(LoginRequiredMixin, View):
    template_name = 'admin/General_Settings/GameType.html'

    def get(self, request):
        gametypes = GameType.objects.all()
        return render(request, self.template_name,
                      {
                          'gametypes': gametypes,
                          'breadcrumb': {
                                          'parent': 'General Settings',
                                          'child': 'Game Type'
                                          }

                          })



# fieldcapacity CRUD Views
class FieldCapacityCreateView(LoginRequiredMixin, View):
    template_name = 'forms/fieldcapacity_form.html'

    def get(self, request):
        form = FieldCapacityForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FieldCapacityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Field Capacity created successfully.')
            return redirect('fieldcapacity_list')
        messages.error(request, 'There was an error creating the Field Capacity. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})

class FieldCapacityUpdateView(LoginRequiredMixin, View):
    template_name = 'forms/fieldcapacity_form.html'

    def get(self, request, pk):
        fieldcapacity = get_object_or_404(FieldCapacity, pk=pk)
        form = FieldCapacityForm(instance=fieldcapacity)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        fieldcapacity = get_object_or_404(FieldCapacity, pk=pk)
        form = FieldCapacityForm(request.POST, instance=fieldcapacity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Field Capacity updated successfully.')
            return redirect('fieldcapacity_list')
        messages.error(request, 'There was an error updating the game type. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})

class FieldCapacityDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        fieldcapacity = get_object_or_404(FieldCapacity, pk=pk)
        fieldcapacity.delete()
        messages.success(request, 'Field Capacity successfully deleted.')
        return redirect('fieldcapacity_list')

    def post(self, request, pk):
        fieldcapacity = get_object_or_404(FieldCapacity, pk=pk)
        fieldcapacity.delete()
        messages.success(request, 'Field Capacity successfully deleted.')
        return redirect('fieldcapacity_list')

class FieldCapacityListView(LoginRequiredMixin, View):
    template_name = 'admin/General_Settings/FieldCapacity.html'

    def get(self, request):
        fieldcapacitys = FieldCapacity.objects.all()
        return render(request, self.template_name,
                      {
                          'fieldcapacitys': fieldcapacitys,
                          'breadcrumb': {
                                          'parent': 'General Settings',
                                          'child': 'Field Capacity'
                                          }

                          })



# GroundMaterials CRUD Views
class GroundMaterialCreateView(LoginRequiredMixin, View):
    template_name = 'forms/groundmaterial_form.html'

    def get(self, request):
        form = GroundMaterialForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = GroundMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Field Capacity created successfully.')
            return redirect('groundmaterial_list')
        messages.error(request, 'There was an error creating the Field Capacity. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})

class GroundMaterialUpdateView(LoginRequiredMixin, View):
    template_name = 'forms/groundmaterial_form.html'

    def get(self, request, pk):
        groundmaterial = get_object_or_404(GroundMaterial, pk=pk)
        form = GroundMaterialForm(instance=groundmaterial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        groundmaterial = get_object_or_404(GroundMaterial, pk=pk)
        form = GroundMaterialForm(request.POST, instance=groundmaterial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Field Capacity updated successfully.')
            return redirect('groundmaterial_list')
        messages.error(request, 'There was an error updating the game type. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})

class GroundMaterialDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        groundmaterial = get_object_or_404(GroundMaterial, pk=pk)
        groundmaterial.delete()
        messages.success(request, 'Field Capacity successfully deleted.')
        return redirect('groundmaterial_list')

    def post(self, request, pk):
        groundmaterial = get_object_or_404(GroundMaterial, pk=pk)
        groundmaterial.delete()
        messages.success(request, 'Field Capacity successfully deleted.')
        return redirect('groundmaterial_list')

class GroundMaterialListView(LoginRequiredMixin, View):
    template_name = 'admin/General_Settings/GroundMaterial.html'

    def get(self, request):
        groundmaterials = GroundMaterial.objects.all()
        return render(request, self.template_name,
                      {
                          'groundmaterials': groundmaterials,
                          'breadcrumb': {
                                          'parent': 'General Settings',
                                          'child': 'Ground Material'
                                          }

                          })



# Tournament Style CRUD Views
class TournamentStyleCreateView(LoginRequiredMixin, View):
    template_name = 'forms/tournamentstyle_form.html'

    def get(self, request):
        form = TournamentStyleForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TournamentStyleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Field Capacity created successfully.')
            return redirect('tournamentstyle_list')
        messages.error(request, 'There was an error creating the Field Capacity. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})

class TournamentStyleUpdateView(LoginRequiredMixin, View):
    template_name = 'forms/tournamentstyle_form.html'

    def get(self, request, pk):
        tournamentstyle = get_object_or_404(TournamentStyle, pk=pk)
        form = TournamentStyleForm(instance=tournamentstyle)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        tournamentstyle = get_object_or_404(TournamentStyle, pk=pk)
        form = TournamentStyleForm(request.POST, instance=tournamentstyle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Field Capacity updated successfully.')
            return redirect('tournamentstyle_list')
        messages.error(request, 'There was an error updating the game type. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})

class TournamentStyleDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        tournamentstyle = get_object_or_404(TournamentStyle, pk=pk)
        tournamentstyle.delete()
        messages.success(request, 'Field Capacity successfully deleted.')
        return redirect('tournamentstyle_list')

    def post(self, request, pk):
        tournamentstyle = get_object_or_404(TournamentStyle, pk=pk)
        tournamentstyle.delete()
        messages.success(request, 'Field Capacity successfully deleted.')
        return redirect('tournamentstyle_list')

class TournamentStyleListView(LoginRequiredMixin, View):
    template_name = 'admin/General_Settings/TournamentStyle.html'

    def get(self, request):
        tournamentstyles = TournamentStyle.objects.all()
        return render(request, self.template_name,
                      {
                          'tournamentstyles': tournamentstyles,
                          'breadcrumb': {
                                          'parent': 'General Settings',
                                          'child': 'Tournaments'
                                          }
                          })



# Event Type CRUD Views
class EventTypeCreateView(LoginRequiredMixin, View):
    template_name = 'forms/eventtype_form.html'

    def get(self, request):
        form = EventTypeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EventTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Field Capacity created successfully.')
            return redirect('eventtype_list')
        messages.error(request, 'There was an error creating the Field Capacity. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})

class EventTypeUpdateView(LoginRequiredMixin, View):
    template_name = 'forms/eventtype_form.html'

    def get(self, request, pk):
        eventtype = get_object_or_404(EventType, pk=pk)
        form = EventTypeForm(instance=eventtype)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        eventtype = get_object_or_404(EventType, pk=pk)
        form = EventTypeForm(request.POST, instance=eventtype)
        if form.is_valid():
            form.save()
            messages.success(request, 'Field Capacity updated successfully.')
            return redirect('eventtype_list')
        messages.error(request, 'There was an error updating the game type. Please ensure all fields are filled out correctly.')
        return render(request, self.template_name, {'form': form})

class EventTypeDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        eventtype = get_object_or_404(EventType, pk=pk)
        eventtype.delete()
        messages.success(request, 'Field Capacity successfully deleted.')
        return redirect('eventtype_list')

    def post(self, request, pk):
        eventtype = get_object_or_404(EventType, pk=pk)
        eventtype.delete()
        messages.success(request, 'Field Capacity successfully deleted.')
        return redirect('eventtype_list')

class EventTypeListView(LoginRequiredMixin, View):
    template_name = 'admin/General_Settings/EventType.html'

    def get(self, request):
        eventtypes = EventType.objects.all()
        return render(request, self.template_name,
                      {
                          'eventtypes': eventtypes,
                          'breadcrumb': {
                                          'parent': 'General Settings',
                                          'child': 'Event Types'
                                          }
                          })