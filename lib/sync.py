from django.conf import settings
import pusher as p

pusher = None

def connect():
    global pusher
    if pusher is not None: return
    pusher = p.Pusher(app_id=settings.PUSHER_APP_ID,
                      key=settings.PUSHER_KEY,
                      secret=settings.PUSHER_SECRET)
