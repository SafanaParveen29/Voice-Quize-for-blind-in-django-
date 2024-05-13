from django.urls import path
from . import views
urlpatterns = [
path('',views.home,name="home"),
path('student_login/',views.student_login,name="student_login"),
path('student_dashboard/',views.student_dashboard,name="student_dashboard"),
path('logout/',views.logout,name="logout"),
path('exam/',views.exam,name="exam"),
path('result_exam_data/',views.result_exam_data,name="result_exam_data"),
path('answer_view/<int:num>/',views.answer_view,name="answer_view")
]


