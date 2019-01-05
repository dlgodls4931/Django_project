from django.urls import path

from . import views
app_name='visual'
urlpatterns = [
    path('', views.list),  
    path('write',views.write),  
    #글 저장 메소드
    path('insert', views.insert),  
    path('detail', views.detail),  
    path('update', views.update),
    path('delete', views.delete),
    path('download', views.download),
    path('reply_insert', views.reply_insert),
]