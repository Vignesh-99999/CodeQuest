from django.urls import path
from .views import *
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    # path('', views.index, name='index'),
    # path('execute', views.execute_code, name='execute_code'),
    path('my-django-view/', views.my_django_view, name='my_django_view'),
    path('codearea/', views.db_get_question, name='index_new'),
    path('', views.LandingPage, name='LandingPage'),
    path('login/',views.Login, name="login"),
    path('signup/',views.StudentSignup, name="signup"),
    path('register',views.register, name="register"),
    path('signup/submit/',views.signupPost, name="SignupPost"),   
    path('login/submit/',views.loginPost, name="LoginPost"), 
    path('userIndex/', views.UserIndex, name='UserIndex'),
    path('submit-code/',views.Check_Input_Output, name='submit-code'),
    path('delete-student/', views.delete_student, name='delete_student'),
    path('delete-teach/', views.delete_teach, name='delete_teach'),
    path('edit_student_data/', views.edit_student_data, name='edit_student_data'),
    path('edit_student_save/', views.edit_stu_save, name='edit_stu_save'),
    path('edit_teach_data/', views.edit_teach_data, name='edit_teach_data'),
    path('edit_teach_save/', views.edit_teach_save, name='edit_teach_save'),
    path('Showstu/',views.Stu_list, name="Showstu"),
    path('superadmin/', views.superadmin, name='superadmin'),
    path('teach_list/',views.teach_list, name="teach_list"),
    path('bulkstu/',views.bulkstu, name="bulkstu"),
    path('practice/',views.practice,name="stu_prac"),
    path('addcourse/',views.addcourse,name="addcourse"),
    path('logout/',views.logout_view,name="logout"),
    path('practice/<str:language>/',views.db_get_question,name='practice'),
    path('prof/',views.prof_main,name='prof'),
    path('prof_test/',views.add_test,name='prof_test'),
    path('/',views.add_test_post,name='add_test_post'),
    path('List/',views.ListQuestions,name='ListQuentions'),
    path('solve/<int:que_id>/<int:exam_id>', views.solve_question, name='solve_question'),
    path('submit/<int:que_id>/', views.SubmitPost, name='SubmitQuestion_post'),
    path('get_notifications/<int:student>/', views.get_notifications, name='get_notifications'),
    path('delete_notifications/<int:student>/', views.delete_notification, name='delete_notification'),
    path('Test/', views.test_list, name='test_list'),
    path('exam_detail/<int:examid>', views.ListQuestions, name='exam_detail'),

    path('prof/add_que',views.add_que,name='AddQue'),

    path('prof/marks',views.show_marks,name='ShowMarks'),

    path('prof/marks/search',views.show_marks_post,name='SearchMarks'),
    path('prof/marks/search_exam',views.search_exam,name='Searchexam'),
    path('prof/marks/dowload_excel',views.download_marks_excel,name="download_marks_excel")
]
