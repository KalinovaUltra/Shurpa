from shurpa.views import menu

def get_shurpa_context(request):
    return {'mainmenu': menu}