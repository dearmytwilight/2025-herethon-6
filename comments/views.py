import json
from django.views.decorators.csrf import csrf_exempt
from comments.models import Comment
from moments.models import Moment
from oopsie.utils import response_success, response_error
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse

User = get_user_model()

######## 댓글 렌더링용 함수 ########
from django.shortcuts import render, get_object_or_404

# 댓글 작성 화면 렌더링
def comment_create_page(request, moment_id):
    moment = get_object_or_404(Moment, moment_id=moment_id)
    return render(request, 'moment_detail.html', {
        'moment': moment
    })

# 글별 댓글 목록 조회 (화면 렌더링)
def comment_list_page(request, moment_id):
    moment = get_object_or_404(Moment, moment_id=moment_id)
    comments = Comment.objects.filter(moment_id=moment).order_by('-created_date')
    return render(request, 'moment_detail.html', {
        'moment': moment,
        'comments': comments
    })


# 댓글 수정 화면 렌더링
def comment_update_page(request, moment_id, comment_id):
    moment = get_object_or_404(Moment, moment_id=moment_id)
    comment = get_object_or_404(Comment, comment_id=comment_id, moment_id=moment)
    return render(request, 'moment_detail.html', {
        'moment': moment,
        'comment': comment
    })


# 댓글 삭제 확인 화면 렌더링
def comment_delete_page(request, moment_id, comment_id):
    moment = get_object_or_404(Moment, moment_id=moment_id)
    comment = get_object_or_404(Comment, comment_id=comment_id, moment_id=moment)
    return render(request, 'moment_detail.html', {
        'moment': moment,
        'comment': comment
    })







###############################################
'''
# POST, GET 메서드 분기
@csrf_exempt
def comment_root(request, moment_id):
    if request.method == 'GET':
        return comment_list(request, moment_id)
    elif request.method == 'POST':
        return comment_create(request, moment_id)
    else:
        return response_error("허용되지 않은 메서드입니다", code=405)
    
# PUT, DELETE 메서드 분기
@csrf_exempt
def comment_detail_root(request, moment_id, comment_id):
    if request.method == 'POST': 
        return comment_update(request, moment_id, comment_id)
    elif request.method == 'DELETE':
        return comment_delete(request, moment_id, comment_id)
    else:
        return response_error("허용되지 않은 메서드입니다", code=405)
'''

####################################################
# 댓글 생성 (POST)

@csrf_exempt
def comment_create(request, moment_id):
    # 임시 로그인 우회 (테스트 전용)
    #from users.models import CustomUser
    #request.user = CustomUser.objects.first()  # 가장 첫 번째 유저
    if request.method != 'POST':
        return response_error("POST 요청만 허용됩니다", code=405)
    if not request.user.is_authenticated:
        return redirect('login')

    print("🔧 POST 요청 들어옴")
    content = request.POST.get('content')
    if not content:
        return redirect(f'/pages/moments/{moment_id}/detail/')

    try:
        moment = Moment.objects.get(moment_id=moment_id)

        Comment.objects.create(
            moment_id=moment,
            user_id=request.user,
            content=content
        )

        print("✅ 댓글 저장 성공")
        return redirect(f'/pages/moments/{moment_id}/detail/')

    except Exception as e:
        print("❌ 댓글 저장 실패:", e)
        return response_error(f"댓글 작성 오류: {str(e)}", code=500)


# 특정 게시글의 댓글 목록 조회 (GET)
def comment_list(request, moment_id):
    try:
        # moment_id에 해당하는 게시글이 존재하는지 확인
        moment = Moment.objects.get(moment_id=moment_id)

        # 해당 게시글의 댓글 모두 조회 (최신순)
        comments = Comment.objects.filter(moment_id=moment).order_by('-created_date')

        # 댓글 리스트 직렬화
        comment_data = [
            {
                "comment_id": comment.comment_id,
                "user_nickname": comment.user_id.nickname,
                "content": comment.content,
                "created_date": comment.created_date,
                "modified_date": comment.modified_date
            }
            for comment in comments
        ]

        return redirect(f'/pages/moments/{moment_id}/detail/')

    except Moment.DoesNotExist:
        return response_error("해당 게시글이 존재하지 않습니다", code=404)

    except Exception as e:
        return response_error(f"서버 오류: {str(e)}", code=500)
    

# 댓글 수정 (POST)
@csrf_exempt
def comment_update(request, moment_id, comment_id):
    if request.method != 'POST':
        return response_error("POST 요청만 허용됩니다", code=405)

    if not request.user.is_authenticated:
        return redirect('login')

    content = request.POST.get('content')
    user_id = request.POST.get('user_id')

    try:
        moment = Moment.objects.get(moment_id=moment_id)
        comment = Comment.objects.get(comment_id=comment_id, moment_id=moment)

        if str(comment.user_id.id) != str(user_id):
            return response_error("댓글 수정 권한이 없습니다", code=403)

        comment.content = content
        comment.modified_date = now()
        comment.save()

        return redirect(f'/pages/moments/{moment_id}/detail/')

    except Exception as e:
        return response_error(f"댓글 수정 오류: {str(e)}", code=500)

    

# 댓글 삭제 (DELETE)
@csrf_exempt
def comment_delete(request, moment_id, comment_id):
    if request.method != 'POST':
        return response_error("POST 요청만 허용됩니다", code=405)

    if not request.user.is_authenticated:
        return redirect('login')

    user_id = request.POST.get('user_id')

    try:
        moment = Moment.objects.get(moment_id=moment_id)
        comment = Comment.objects.get(comment_id=comment_id, moment_id=moment)

        if str(comment.user_id.id) != str(user_id):
            return response_error("댓글 삭제 권한이 없습니다", code=403)

        comment.delete()

        return redirect(f'/pages/moments/{moment_id}/detail/')

    except Exception as e:
        return response_error(f"댓글 삭제 오류: {str(e)}", code=500)