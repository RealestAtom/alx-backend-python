from django.urls import path
from messaging import views

app_name = "messaging"

urlpatterns = [
    path("", views.conversation_list, name="conversation_list"),
    path("inbox/unread/", views.inbox_unread, name="inbox_unread"),
    path("inbox/all/", views.inbox_all, name="inbox_all"),
    path("inbox/unread/cbv/", InboxUnreadListView.as_view(), name="inbox_unread_cbv"),
    path("thread/<int:message_id>/", views.conversation_thread, name="conversation_thread"),
    path("reply/<int:parent_id>/", views.reply_to_message, name="reply"),
    path("account/delete/", views.delete_user, name="delete_user"),
]
