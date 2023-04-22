from django.urls import path
from .import views
app_name='learning_logs'
urlpatterns=[
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    #Сторінка теми
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    #Додавання теми
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    #Редагування
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    #Видалення
    path('delete_topic/<int:topic_id>/', views.delete_topic, name="delete_topic"),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name="delete_entry"),
]