"""
SpeechBloom AI - Django Context Processor
Passes user, children, and login state to all Jinja2/Django templates.
"""
from core.models import ParentUser, ChildProfile

def speechbloom_context(request):
    user_id = request.session.get('user_id')
    user = None
    children = []

    if user_id:
        try:
            user_obj = ParentUser.objects.get(id=user_id)
            user = user_obj.to_dict()
            children = [c.to_dict() for c in user_obj.children.all()]
        except ParentUser.DoesNotExist:
            request.session.pop('user_id', None)

    return {
        'user': user,
        'children': children,
        'is_logged_in': user is not None,
        'role': user.get('role') if user else None,
    }
