from django.contrib import admin
from . models import Board
# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    list_display=("writer","title","content")

#관리자가 사이트 테이블 등록
admin.site.register(Board,BoardAdmin)