from django.urls import include,path
from .views import *

urlpatterns = [
    path('', home,name='lib'),
    path('admin1/', admin,name='lib'),
    path('student/', student,name='lib'),
    path('stusign/', stusign,name='lib'),
    path('adsign/', adsign,name='lib'),
    path('stulog/', stulog,name='lib'),
    path('adlog/', adlog,name='lib'),
    path('addbook/', addbook,name='lib'),
    path('viewbook/', view_book,name='lib'),
    path('issuebook/', issue_book,name='lib'),
    path('viewissuedbook/', view_issuedbook,name='lib'),
    path('viewissuedbookstud/', viewissuedbookstud,name='lib'),
    path('viewstudent/', view_student,name='lib'),
]
