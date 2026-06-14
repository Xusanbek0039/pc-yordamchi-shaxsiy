from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

from .uzbek_processor import process_command, get_suggestions
from . import system_controller as sc


@api_view(['POST'])
def process_voice_command(request):
    text = request.data.get('text', '').strip()
    if not text:
        return Response({'error': 'Matn bosh'}, status=400)
    result = process_command(text)
    action_result = execute_action(result.get('action', 'unknown'), result.get('params', {}), request.data)
    return Response({
        'input': text,
        'intent': result.get('intent'),
        'response': result.get('response'),
        'confidence': result.get('confidence', 0),
        'action_result': action_result,
    })


def execute_action(action, params, data):
    try:
        if action == 'system_shutdown':
            return sc.system_shutdown()
        elif action == 'system_restart':
            return sc.system_restart()
        elif action == 'system_sleep':
            return sc.system_sleep()
        elif action == 'system_lock':
            return sc.system_lock()
        elif action == 'volume_up':
            return sc.volume_up(data.get('amount', 10))
        elif action == 'volume_down':
            return sc.volume_down(data.get('amount', 10))
        elif action == 'volume_mute':
            return sc.volume_mute()
        elif action == 'volume_unmute':
            return sc.volume_unmute()
        elif action == 'open_app':
            return sc.open_app(params.get('app', ''))
        elif action == 'open_url':
            return sc.open_url(params.get('url', ''))
        elif action == 'open_folder':
            return sc.open_folder(params.get('folder', 'desktop'))
        elif action == 'file_create_folder':
            return sc.file_create_folder(params.get('name', data.get('name', 'Yangi papka')))
        elif action == 'file_list':
            return sc.file_list(params.get('path', data.get('path', None)))
        elif action == 'get_system_info':
            return sc.get_system_info()
        elif action == 'get_battery':
            return sc.get_battery()
        elif action == 'get_time':
            return sc.get_time()
        elif action == 'take_screenshot':
            return sc.take_screenshot()
        elif action == 'run_code':
            return sc.run_code(params.get('lang', 'python'), data.get('code', ''))
        elif action == 'close_window':
            return sc.close_window()
        elif action in ('greeting', 'thanks', 'unknown'):
            return {'success': True}
        else:
            return {'success': False, 'error': 'Noma\'lum buyruq: ' + action}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@api_view(['GET'])
def get_system_status(request):
    return Response({
        'system': sc.get_system_info(),
        'battery': sc.get_battery(),
        'volume': sc.get_volume(),
        'time': sc.get_time(),
    })


@api_view(['POST'])
def transcribe_audio(request):
    audio_file = request.FILES.get('audio')
    if not audio_file:
        return Response({'error': 'Audio fayl topilmadi'}, status=400)
    media_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
    os.makedirs(media_dir, exist_ok=True)
    audio_path = os.path.join(media_dir, 'temp_audio.wav')
    with open(audio_path, 'wb') as f:
        for chunk in audio_file.chunks():
            f.write(chunk)
    openai_key = settings.OPENAI_API_KEY
    if openai_key:
        try:
            import openai
            client = openai.OpenAI(api_key=openai_key)
            with open(audio_path, 'rb') as f:
                transcription = client.audio.transcriptions.create(
                    model='whisper-1', file=f, language='uz',
                    prompt="O'zbek tilida nutq"
                )
            return Response({'text': transcription.text, 'method': 'whisper'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    else:
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='uz-UZ')
            return Response({'text': text, 'method': 'google'})
        except Exception as e:
            return Response({'error': str(e), 'text': ''}, status=200)


@api_view(['GET'])
def get_quick_commands(request):
    return Response([
        {'id': 'browser', 'icon': '🌐', 'text': 'Brauzer och', 'category': 'app'},
        {'id': 'vscode', 'icon': '💻', 'text': 'VS Code och', 'category': 'app'},
        {'id': 'terminal', 'icon': '⌨️', 'text': 'Terminal och', 'category': 'app'},
        {'id': 'explorer', 'icon': '📁', 'text': 'Fayl menejeri', 'category': 'app'},
        {'id': 'calculator', 'icon': '🧮', 'text': 'Kalkulyator', 'category': 'app'},
        {'id': 'youtube', 'icon': '▶️', 'text': 'YouTube', 'category': 'web'},
        {'id': 'google', 'icon': '🔍', 'text': 'Google', 'category': 'web'},
        {'id': 'github', 'icon': '🐙', 'text': 'GitHub', 'category': 'web'},
        {'id': 'vol_up', 'icon': '🔊', 'text': 'Ovoz oshir', 'category': 'system'},
        {'id': 'vol_down', 'icon': '🔉', 'text': 'Ovoz past', 'category': 'system'},
        {'id': 'mute', 'icon': '🔇', 'text': 'Jim', 'category': 'system'},
        {'id': 'screenshot', 'icon': '📸', 'text': 'Skrinshot', 'category': 'system'},
        {'id': 'lock', 'icon': '🔒', 'text': 'Qulflash', 'category': 'system'},
        {'id': 'sleep', 'icon': '😴', 'text': 'Uxlatish', 'category': 'system'},
        {'id': 'sysinfo', 'icon': '📊', 'text': 'Tizim holati', 'category': 'info'},
    ])


@api_view(['POST'])
def run_code_endpoint(request):
    lang = request.data.get('lang', 'python')
    code = request.data.get('code', '')
    if not code:
        return Response({'error': 'Kod bosh'}, status=400)
    return Response(sc.run_code(lang, code))


@api_view(['GET'])
def suggestions_view(request):
    text = request.GET.get('text', '')
    return Response(get_suggestions(text))
