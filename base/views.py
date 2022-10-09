import itertools
from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django import views
from django.views.generic.base import TemplateView
from django.views import generic
from django import http
from django.core.paginator import Paginator
from django.db.models import Sum,Q
from django import forms as django_forms
from django.urls import reverse_lazy

from . import forms
from . import models

class HomeView(views.View):
    def get(self,request):
        return render(request,"components/home.html")
    def post(self,request):
        pass

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name ="pages/dashboard/statistics_dashboard.html"

    def sponsors(self):
        sponsors_list_org = list(models.OrgApplication.objects.all())
        sponsors_list_physical = list(models.PhysicalApplication.objects.all())
        sponsors_list_all = sponsors_list_org + sponsors_list_physical
        months = {}
        for i in range(1,13):
            months[i] = 0
        for sponsor in sponsors_list_all:
            months[sponsor.created_at.month] += 1

        return [item for item in months.values()]

    def students(self):
        students_list = list(models.Student.objects.all())
        months = {}
        for i in range(1,13):
            months[i] = 0
        for student in students_list:
            months[student.created_at.month] +=  1

        return [item for item in months.values()]

    def paid_fees(self):
        total_tution_fees = models.Student.objects.aggregate(tution_fees_sum=Sum("tution_fee"))
        unpaid_fees = models.Student.objects.aggregate(unpaid_fees_sum=Sum("unpaid_tution_fee"))

        return total_tution_fees["tution_fees_sum"] - unpaid_fees["unpaid_fees_sum"]

    def total_fees(self):
        total_tution_fees = models.Student.objects.aggregate(tution_fees_sum=Sum("tution_fee"))
        return total_tution_fees["tution_fees_sum"]

    def unpaid_fees(self):
        unpaid_fees = models.Student.objects.aggregate(unpaid_fees_sum=Sum("unpaid_tution_fee"))
        return unpaid_fees["unpaid_fees_sum"]

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        context["sponsors"] = self.sponsors()
        context["students"] = self.students()
        context["paid_fees"] = self.paid_fees()
        context["total_fees"] = self.total_fees()
        context["unpaid_fees"] = self.unpaid_fees()
        return context
    
class DashboardOrgSponsorView(views.View):
    def get(self,request):
        page_number = request.GET.get('page')
        sponsor_list = models.OrgApplication.objects.all().order_by("-created_at")
        paginator = Paginator(sponsor_list,5)
        page_obj = paginator.get_page(page_number)
        filter_form = forms.OrgSponsorFilterForm()
        
        context = {
            "page_obj": page_obj,
            "filter_form": filter_form,
        }
        
        return render(request,"pages/dashboard/org_sponsor_dashboard.html",context)

    def post(self,request):
        results = models.OrgApplication.objects.filter(
            Q(fullname__icontains=request.POST.get("fullname")) | 
            Q(payment_amount=request.POST.get("payment_amount")) |
            Q(status__exact=request.POST.get("status")))

        filter_form = forms.OrgSponsorFilterForm()
        
        context = {
            "page_obj": results,
            "filter_form": filter_form,
        }
        return render(request,"pages/dashboard/org_sponsor_dashboard.html",context)

class DashboardPhysicalSponsorView(LoginRequiredMixin,views.View):
    def get(self,request):
        page_number = request.GET.get('page')
        sponsor_list = models.PhysicalApplication.objects.all().order_by("-created_at")
        paginator = Paginator(sponsor_list,5)
        page_obj = paginator.get_page(page_number)
        
        filter_form = forms.PhysicalSponsorFilterForm()
        
        context = {
            "page_obj": page_obj,
            "filter_form": filter_form,
        }
        
        return render(request,"pages/dashboard/physical_sponsor_dashboard.html",context)

    def post(self,request):
        results = models.PhysicalApplication.objects.filter(
            Q(fullname__icontains=request.POST.get("fullname")) | 
            Q(payment_amount=request.POST.get("payment_amount")) |
            Q(status__exact=request.POST.get("status")))

        filter_form = forms.PhysicalSponsorFilterForm()
        
        context = {
            "page_obj": results,
            "filter_form": filter_form,
        }
        return render(request,"pages/dashboard/physical_sponsor_dashboard.html",context)

class DashboardStudentsView(LoginRequiredMixin,views.View):
    def get(self,request):
        page_number = request.GET.get('page')
        sponsor_list = models.Student.objects.all().order_by("-created_at")
        paginator = Paginator(sponsor_list,5)
        page_obj = paginator.get_page(page_number)
        
        filter_form = forms.StudentFilterForm()

        context = {
            "page_obj": page_obj,
            "filter_form": filter_form,
        }
        
        return render(request,"pages/dashboard/students_dashboard.html",context)

    def post(self,request):
        results = models.Student.objects.filter(
            Q(fullname__icontains=request.POST.get("fullname")) | 
            Q(tution_fee=request.POST.get("tution_fee")) |
            Q(phone__exact=request.POST.get("phone")))

        filter_form = forms.StudentFilterForm()
        
        context = {
            "page_obj": results,
            "filter_form": filter_form,
        }
        return render(request,"pages/dashboard/students_dashboard.html",context)


class StudentCreationView(LoginRequiredMixin,generic.CreateView):
    model = models.Student
    fields = ["fullname","phone","degree","college","tution_fee"]
    template_name = "pages/dashboard/students/student_creation.html"
    success_url = "/dashboard/"

    def form_valid(self,form):
        form.cleaned_data["unpaid_tution_fee"] = form.cleaned_data["tution_fee"]
        models.Student.objects.create(**form.cleaned_data)
        return http.HttpResponseRedirect(self.success_url)

class StudentDetailView(LoginRequiredMixin,generic.DetailView):
    model = models.Student
    fields = ["fullname","phone","degree","college","tution_fee"]
    template_name = "pages/dashboard/students/student_detail.html"
    context_object_name = "student"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object().__dict__
        del student["_state"]
        student_id = student.pop("id")
        context["change_form"] = forms.StudentChangeForm(initial=student)
        # context["sponsors"] = models.TransactionTracker.get_sponsors(student_id=student_id)
        context["transactions"] = models.TransactionTracker.objects.filter(
                    student__id=student_id)
        return context

class StudentEditView(LoginRequiredMixin,generic.UpdateView):
    model = models.Student
    fields = ["fullname","phone","degree","college","tution_fee"]
    template_name = "pages/dashboard/students/student_edit.html"
    
    def get_success_url(self):
        student = self.get_object()
        return reverse_lazy("dashboard-student-detail",args=(student.pk,))


class AddSponsorView(LoginRequiredMixin,generic.CreateView):
    form_class = forms.AddSponsorForm
    template_name = "pages/dashboard/students/add_sponsor.html"

    def form_valid(self,form):
        referer = self.request.META.get("HTTP_REFERER")
        transaction = models.TransactionTracker(**form.cleaned_data).init()
        if transaction is None:
            messages.error(self.request,"Something went wrong")
            return redirect(self.request.path)
        if transaction.is_valid():
            transaction.do_transaction()

            if referer is None:
                return redirect("/dashboard/")
            return redirect(referer)
        messages.error(self.request,"You cannot allocate money from this user.")
        return self.form_invalid(form)


class SponsorDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "pages/dashboard/sponsors/detail.html"
    context_object_name = "sponsor"

    def get_object(self):
        obj_type = self.kwargs.get("obj_type")
        obj_id = self.kwargs.get("obj_id")
        if int(obj_type) == 1:
            self.object = models.OrgApplication.objects.get(id=obj_id)
        elif int(obj_type) == 2:
            self.object = models.PhysicalApplication.objects.get(id=obj_id)
        return self.object

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        context["change_form"] = forms.SponsorEditForm(initial={"status": self.object.status})

        if self.object.is_org:
            context["transactions"] = models.TransactionTracker.objects.filter(
                    org_sponsor=self.object)
        elif self.object.is_physical:
            context["transactions"] = models.TransactionTracker.objects.filter(
                    physical_sponsor=self.object)
        return context

    def post(self,request,*args,**kwargs):
        form = forms.SponsorEditForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data.get("status")
            obj = self.get_object()
            if status != obj.status:
                obj.status = status
                obj.save()
        
        context = self.get_context_data()
        return render(request,self.template_name,context)