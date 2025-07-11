from django.urls import path
from .views import comment_create, comment_list, comment_update, comment_delete
from .views import (
    comment_list_page,
    comment_create_page,
    comment_update_page,
    comment_delete_page,
)

urlpatterns = [
    ### api 용
    path('create/', comment_create, name='comment_create'),  # POST
    path('list/', comment_list, name='comment_list'),        # GET
    path('<int:comment_id>/update/', comment_update, name='comment_update'),  # POST(PUT 기능)
    path('<int:comment_id>/delete/', comment_delete, name='comment_delete'),  # DELETE

    ### 렌더링 용
    path('list-page/', comment_list_page, name='comment_list_page'),
    path('create-page/', comment_create_page, name='comment_create_page'),
    path('<int:comment_id>/update-page/', comment_update_page, name='comment_update_page'),
    path('<int:comment_id>/delete-page/', comment_delete_page, name='comment_delete_page'),

]
