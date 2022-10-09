from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django import views
from django.views.generic.base import TemplateView

from . import forms

class LoginView(views.View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.error(request,"To login you should logout.")
            return redirect("dashboard")

        context = {}
        context["form"] = forms.UserLoginForm
        return render(request, "auth/login.html", context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = forms.UserLoginForm(request.POST)
        print("Form is valid ",form.is_valid())
        if form.is_valid():
            try:
                user = auth.authenticate(
                    request, 
                    username=form.cleaned_data["username"], 
                    password=form.cleaned_data["password"])
                auth.login(request, user)
                return redirect("dashboard")
            except Exception as e:
                print("error: ", e)
                messages.info(request, str(e))

        context = {
            "form": form
        }
        return render(request, "auth/login.html", context)
    

class RegisterView(TemplateView):
    template_name = "auth/register.html"
    
    def post(self,request):
        org_name = request.POST.get("org_name")
        if org_name is not None:
            org_form = forms.OrgAppForm(request.POST)
            if org_form.is_valid():
                org_form.save()
                messages.success(request, "Form is successfuly sent.")
            else:
                messages.error(request, "Form is not a valid")
        else:
            physical_form = forms.PhysicalAppForm(request.POST)
            if physical_form.is_valid():
                physical_form.save()
                messages.success(request, "Form is successfuly sent.")
            else:
                messages.error(request, "Form is not a valid")
        
        context = self.get_context_data()
        return render(request,"auth/register.html",context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org_form"] = forms.OrgAppForm()
        context["physical_form"] = forms.PhysicalAppForm()
        return context
    
def logout(request):
    auth.logout(request)
    return redirect("dashboard")