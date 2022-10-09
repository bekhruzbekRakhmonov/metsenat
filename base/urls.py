from django.urls import path
from . import views
from .auth import views as auth_views

urlpatterns = [
	path("",views.HomeView.as_view(),name="home"),
 
	# dashboard
	path("dashboard/",
		views.DashboardView.as_view(),
		name="dashboard"),
	path("dashboard/org-sponsor/",
		views.DashboardOrgSponsorView.as_view(),
		name="dashboard-org-sponsor"),
 	path("dashboard/physical-sponsor/",
 		views.DashboardPhysicalSponsorView.as_view(),
 		name="dashboard-physical-sponsor"),

 	# sponsors
 	path("dashboard/sponsors/<int:obj_type>/detail/<int:obj_id>/",
 		views.SponsorDetailView.as_view(),
 		name="sponsor-detail"),

 	# students
 	path("dashboard/students/",
 		views.DashboardStudentsView.as_view(),
 		name="dashboard-students"),
 	path("dashboard/students/create/",
 		views.StudentCreationView.as_view(),
 		name="dashboard-student-creation"),
 	path("dashboard/students/detail/<int:pk>/",
 		views.StudentDetailView.as_view(),
 		name="dashboard-student-detail"),
 	path("dashboard/students/edit/<int:pk>/",
 		views.StudentEditView.as_view(),
 		name="dashboard-student-edit"),
 	path("dashboard/students/add-sponsor/",
 		views.AddSponsorView.as_view(),
 		name="dashboard-student-add-sponsor"),

	# auth
	path("login/",auth_views.LoginView.as_view(),name="login"),
	path("register/",auth_views.RegisterView.as_view(),name="register"),
	path("logout/",auth_views.logout,name="logout"),
]