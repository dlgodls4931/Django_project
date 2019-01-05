from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View
from visual.models import Board,Comment 
from django.urls import reverse
import math
import os
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils.http import urlquote
# 파일이 업로드될 데렉토리 저장

UPLOAD_DIR="바탕 화면"
# Create your views here
@csrf_exempt
def list(request):
   
    #검색옵션
    try:
        search_option=request.POST["search_option"]
    except:
        try:
            search_option=request.GET["search_option"]
        except:
            search_option="writer"
    #검색키워드
    try:
        search=request.POST["search"]
    except:
        try:
            search=request.GET["search"]
        except:
            search=""
    #키워드가 포함된 레코드를 찾음
    #필드 __ 키워드를 찾음
    if search_option=="all":
        boardCount = Board.objects.filter(\
        Q(writer__contains=search) | Q(title__contains=search) | Q(content__contains=search)
        ).count()
    elif search_option=="writer":
        boardCount = Board.objects.filter(writer__contains = search).count()
    elif search_option=="title":
        boardCount = Board.objects.filter(title__contains = search).count()
    elif search_option=="content":
        boardCount = Board.objects.filter(content__contains = search).count()

    try:
        start=int(request.GET['start'])
    except:
        start = 0    
    page_size = 10 #페이지당 게시물수
    page_list_size = 10 #한 화면에 표실할 페이지의 갯수
    end=start+page_size
    total_page = math.ceil(boardCount/page_size)
    current_page = math.ceil((start+1)/page_size)
    start_page = math.floor((current_page-1)/page_list_size)*page_list_size+1
    end_page = start_page + page_list_size -1

    if total_page < end_page:
        end_page=total_page
    if start_page >= page_list_size:
        prev_list=(start_page-2) * page_size
    else :
        prev_list=0
    if total_page > end_page:
        next_list = end_page * page_size
    else:
         next_list = 0
    
    if search_option=="all":
        boardList = Board.objects.filter(\
        Q(writer__contains=search)|Q(title__contains=search)|\
        Q(content__contains=search)).order_by("-idx")[start:end]
    elif search_option=="writer":
        boardList = Board.objects.filter(writer__contains = search).order_by("-idx")[start:end]
    elif search_option=="title":
        boardList = Board.objects.filter(title__contains = search).order_by("-idx")[start:end]
    elif search_option=="content":
        boardList = Board.objects.filter(content__contains = search).order_by("-idx")[start:end]
    
    #boardCount =Board.objects.count()
    #boardList=Board.objects.all().order_by("-idx") 
    
    print("start_page:",start_page)
    print("end_page:",end_page)
    print("page_list_size:",page_list_size)
    print("total_page:",total_page)
    print("prev_list",prev_list)
    print("next_list",next_list)

    links=[]
    for i in range(start_page,end_page+1):
        page = (i-1) * page_size
        links.append(\
 "<a href='?search_option="+search_option+"&search="+search\
 +"&start="+str(page)+"'>"+str(i)+"</a>")
        print("links:",links)
    
    
    return render_to_response('list.html',{'boardList':boardList,"boardCount":boardCount,
    "search_option":search_option,"search":search,
    "range":range(start_page-1,end_page),
    "start_page":start_page,
    "end_page":end_page,
    "page_list_size":page_list_size,
    "total_page":total_page,
    "prev_list":prev_list,
    "next_list":next_list,
    "links":links,})  

def write(request):
    return render_to_response("write.html")
@csrf_exempt
def insert(request):
    #파일 업로드 작업
    fname=""
    fsize=0
    if"file"in request.FILES:
        file=request.FILES["file"]
        fname=file._name
        fp=open("%s%s" % (UPLOAD_DIR, fname),"wb")    
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()


        fsize=os.path.getsize(UPLOAD_DIR+fname)
    dto=Board(writer=request.POST["writer"],
              title=request.POST["title"],
              content=request.POST["content"],
              filename=fname,
              filesize=fsize)
    dto.save()
    print(dto)
    return redirect("/visual")

def download(request):
    id=request.GET["idx"]
    dto=Board.objects.get(idx=id)
    #첨부파일의 전체경로
    path=UPLOAD_DIR+dto.filename
    print("path:",path)
    #디렉토리를 제외한 파일의 이름
    filename=os.path.basename(path)
    #특수문자 처리
    filename=urlquote(filename)
    print("pfilename:",os.path.basename(path))
    with open(path,'rb') as file:
        # 파일의 이름이 다양하니깐 octet-stream으로 선언
        response=HttpResponse(file.read(),content_type="application/octet-stream")
        response["Content-Dispositon"]="attachment; filename*=UTF-8''{0}".format(filename)
        dto.down_up()
        dto.save() 
        return response

def detail(request):
    try:
        search_option=request.POST["search_option"]
    except:
        try:
            search_option=request.GET["search_option"]
        except:
            search_option="writer"
    #검색키워드
    try:
        search=request.POST["search"]
    except:
        try:
            search=request.GET["search"]
        except:
            search=""
    id=request.GET["idx"]
    dto=Board.objects.get(idx=id)
    dto.hitup()
    dto.save
    #첨부파일의 크기는 소수이하 2번째자리 까지만
    filesize="%.2f" %(dto.filesize /1024)

    #댓글 목록
    commentList=Comment.objects.filter(board_idx=id).order_by("idx")
    return render_to_response("detail.html",{"dto":dto,"filesize":filesize,"commentList":commentList,
    "search_option":search_option,"search":search})
@csrf_exempt
def reply_insert(request):
    id=request.POST["idx"]
    dto=Comment(board_idx=id,writer=request.POST["writer"],content=request.POST["content"])
    dto.save()
    return HttpResponseRedirect("detail?idx="+id)
@csrf_exempt
def update(request):
    id=request.POST['idx']
    dto_src=Board.objects.get(idx=id)
    fname = dto_src.filename
    fsize = dto_src.filesize

    if"file" in request.FILES:
        file=request.FILES["file"]
        fname=file._name
        fp=open("%s%s" % (UPLOAD_DIR, fname),"wb")    
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

        fsize=os.path.getsize(UPLOAD_DIR+fname)
    
    dto_new=Board(writer=request.POST["writer"],
              title=request.POST["title"],
              content=request.POST["content"],
              filename=fname,
              filesize=fsize)
    dto_new.save()
    return redirect("/visual")
#글삭제
@csrf_exempt 
def delete(request):
    id=request.POST["idx"]
    Board.objects.get(idx=id).delete()
    return redirect("/visual")
