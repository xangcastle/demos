import datetime
import decimal
from django.db.models.fields.files import ImageFieldFile, FileField
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


class Codec(json.JSONEncoder):
    """
    Codificador json que se usara para evitar el error
    
    THE CLASS X IS NOT A OBJECT SERIALIZABLE  o como sea :/
    
    la idea es que toda clase que se quiera serializar solo se de una definicion de texto o numeros
    que son los valores reconocidos por json
    
    """
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, ImageFieldFile):
            try:
                return obj.url
            except:
                return 'null'
        elif isinstance(obj, FileField):
            try:
                return obj.url
            except:
                return 'null'
        elif obj == None:
            return 'null'
        else:
            return json.JSONEncoder.default(self, obj)


@csrf_exempt
def get_object(request):
    """
    Get Object
    Este webService se consume por POST exclusivamente
    
    :parametros 
        request.app_label: nombre del paquete 
                (normalmente el mismo que va en instaled app en el settings)
        request.model: nombre del modelo
        
        request.id: id o clave primaria de la instancia que se quiere recibir
        
    :retorna: un json con los datos de la instancia solicitada
    
    """
    model = ContentType.objects.get(app_label=request.POST.get('app_label', ''),
                                    model=request.POST.get('model', ''))
    instance = model.get_object_for_this_type(id=int(request.POST.get('id', '')))
    return HttpResponse(json.dumps(instance.to_json(), cls=Codec), content_type='application/json')


@csrf_exempt
def get_collection(request):
    """
    Misma Idea, pero todos los objetos,
    
    queda pendiente agregar filtros para probar
    :param request: 
    :return: 
    """

    model = ContentType.objects.get(app_label=request.POST.get('app_label', ''),
                                    model=request.POST.get('model', ''))
    queryset = model.get_all_objects_for_this_type()
    return HttpResponse(json.dumps([x.to_json() for x in queryset], cls=Codec),
                        content_type='application/json')
