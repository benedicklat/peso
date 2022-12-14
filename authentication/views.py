
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import *
from .forms import *
from .utils import *
from .reset_password import *
# Create your views here.


def accounts(request):
    template_name = "user_accounts/accounts.html"
    users = User.objects.all()
    accounts = User.objects.all()
    context = {
        "accounts": accounts,
        "users": users,
    }
    return render(request, template_name, context)


def viewprofile(request):
    template_name = "profile/profile.html"
    return render(request, template_name)


def user_update(request, pk):
    template_name = "user_accounts/update_account.html"
    user = get_object_or_404(User, pk=pk)
    form = AdminSignUpForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect("/")
    context = {
        "form": form
    }
    return render(request, template_name, context)


def user_delete(request, pk):
    user = User.objects.filter(id=pk).update(status=False)
    return redirect("/")


class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.role = "superadmin"
        user.save()
        return redirect('/')


class EmployerSignUpView(CreateView):
    model = Employer
    form_class = EmployerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = 'employer'
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        full_name = user.first_name
        email = encrypt_email(user.email)
        link = f"https://pesomalvar.herokuapp.com/verify-email/{email}"
        send_email(user.email, full_name, link)
        employer = Employer.objects.create(
            user_id=user.id, 
            company_name=form.cleaned_data['company_name'], 
            company_address=form.cleaned_data['company_address'], 
            business_nature=form.cleaned_data['business_nature'],
            status = "Active",
            business_permit = form.cleaned_data['business_permit']
            )
        print(send_email(user.email, full_name, link))
        
        return redirect('email_sent')

def employer_profile(request):
    template_name = "employer_profile.html"
    profile = Employer.objects.get(user__id = request.user.id)
    context = {
        "profile" : profile
    }
    return render(request, template_name,context)

def employer_update(request, pk):
    template_name = "employer_update.html"
    profile = get_object_or_404(Employer, pk=pk)
    user_data = get_object_or_404(User, pk=request.user.id)
    form = EmployerUpdateForm(request.POST or None, request.FILES or None, instance=profile )
    user = EmployerUserUpdateForm(request.POST or None, request.FILES or None, instance=user_data )
    if form.is_valid() and user.is_valid():
        form.save(commit=False)
        form.instance.user_id=request.user.id
        form.save()
        user.save()
        return redirect("employer_profile")
    context = {
        "form" : form,
        "user" : user
    }
    return render(request, template_name,context)

class ApplicantSignUpView(CreateView):
    model = Applicant
    form_class = ApplicantSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'applicant'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = 'applicant'
        user.is_verified = True
        user.save()
        print("USER ID", user.id)
        full_name = user.first_name
        email = encrypt_email(user.email)
        link = f"https://pesomalvar.herokuapp.com/verify-email/{email}"
        send_email(user.email, full_name, link)
        employer = Applicant.objects.create(
            user_id=user.id, 
            middle_name=form.cleaned_data['middle_name'], 
            house_no=form.cleaned_data['house_no'], 
            barangay=form.cleaned_data['barangay'], 
            municipality=form.cleaned_data['municipality'], 
            province=form.cleaned_data['province'], 
            height=form.cleaned_data['height'], 
            religion=form.cleaned_data['religion'], 
            tin_number=form.cleaned_data['tin_number'], 
            employment_status=form.cleaned_data['employment_status'], 
            employed=form.cleaned_data['employed'], 
            currently_in_school=form.cleaned_data['currently_in_school'], 
            educational_attainment=form.cleaned_data['educational_attainment'], 
            working_exp=form.cleaned_data['working_exp'], 
            prev_employer=form.cleaned_data['prev_employer'],
            birthdate=form.cleaned_data['birthdate'],
            age=form.cleaned_data['age'],
            status = "Active",
            contact=form.cleaned_data['contact']
            )
        return redirect('email_sent')

def applicant_profile(request):
    template_name = "applicant_profile.html"
    profile = Applicant.objects.get(user__id = request.user.id)
    context = {
        "profile" : profile
    }
    return render(request, template_name,context)

def applicantprofile_update(request, pk):
    template_name = "applicant_update.html"
    profile = get_object_or_404(Applicant, pk=pk)
    user_data = get_object_or_404(User, pk=request.user.id)
    form = ApplicantUpdateForm(request.POST or None, request.FILES or None, instance=profile)
    user = ApplicantUserUpdateForm(request.POST or None, request.FILES or None, instance=user_data)
    if form.is_valid() and user.is_valid():
        applicant = form.save(commit=False)
        applicant.user_id=request.user.id
        user.save()
        applicant.save()
        return redirect("applicant_profile")
    context = {
        "form": form,
        "user" : user
    }
    return render(request, template_name, context)


def login_page(request):
    admin_email = ["admin@gmail.com", "admin2@gmail.com"]
    admin_password = ["admin123...", "password..."]
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            check_verified = User.objects.filter(email=form.cleaned_data['email'])
            check_status = Employer.objects.filter(user__email=form.cleaned_data['email'])
            for check in check_verified:
                for status in check_status:
                    if status.accepted == True: 
                        if check.is_verified:
                            if user is not None:
                                login(request, user)
                                return redirect('/')
                            else:
                                messages.error(request, 'Invalid email address or password')
                                return redirect('login')
                        else:
                            messages.error(request, 'Email not verified')
                            return redirect('login')
                    else:
                        messages.error(request, 'Account not yet accepted')
                        return redirect('login')

                if check.is_verified:
                    if user is not None:
                        login(request, user)
                        if user.is_staff and user.role == "superadmin":
                            return redirect('main_dashboard')
                        else:
                            return redirect('/')
                    
                else:
                        messages.error(request, 'Account not yet accepted')
                        return redirect('login')
    return render(
        request, 'registration/login.html', context={'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')

def reset_password_emai(request):
    email = request.POST['email']
    reset_email = encrypt_email(email)
    link = f"https://pesomalvar.herokuapp.com/reset-password/{reset_email}"
    send_reset_email(email, link)
    return redirect('password_reset_email_sent')

def reset_password(request, str):
    template_name = "registration/password_reset.html"
    form = ResetPasswordForm(request.POST or None)
    email = decrypt_email(str)
    if form.is_valid():
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']

        if password1 == password2:
            user = User.objects.get(email=email)
            user.set_password(password1)
            user.save()
            return redirect('login')
        else:
            messages.error(request, "Password doesnt't match")
            return redirect('reset-password', str)
    
    context = {"form" : form}
    return render(request,template_name, context)

def verify_email(request, str):
    email = decrypt_email(str)
    print(email)
    user = User.objects.filter(email=email).update(is_verified=True)
    return redirect('login')


def email_sent(request):
    template_name = "email_sent.html"

    return render(request, template_name)

def password_reset_email_sent(request):
    template_name = "password_reset_email_sent.html"

    return render(request, template_name)