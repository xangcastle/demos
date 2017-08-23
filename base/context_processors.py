
from .models import TC, Categoria

def current_tc(request):
    try:
        tc = TC.objects.all().order_by('-tc')[0]
    except:
        tc = 30
    return {'tc': tc}

def context_categorias(request):
    categotias = Categoria.objects.all()
    return {'categotias_sistema': categotias}
