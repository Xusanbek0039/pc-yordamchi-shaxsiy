from django.urls import path
from . import views

urlpatterns = [
    path('command/', views.process_voice_command, name='command'),
    path('status/', views.get_system_status, name='status'),
    path('speech/transcribe/', views.transcribe_audio, name='transcribe'),
    path('commands/quick/', views.get_quick_commands, name='quick-commands'),
    path('code/run/', views.run_code_endpoint, name='run-code'),
    path('suggestions/', views.suggestions_view, name='suggestions'),
]
