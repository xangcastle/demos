import datetime
import decimal
from django.db.models.fields.files import ImageFieldFile, FileField
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import operator


class Codec(json.JSONEncoder):
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


class Filter(object):
    app_label = None
    model_name = None
    model = None

    def __init__(self, app_label, model_name):
        self.app_label = app_label
        self.model_name = model_name
        self.model = ContentType.objects.get(app_label=app_label, model=model_name).model_class()

    @staticmethod
    def _like(sentence, field_name, separator=" ", filters=[]):
        for word in sentence.split(separator):
            filters.append(('{}__icontains'.format(field_name.replace('__like', '')), word))
        return filters

    def format(self, filters):
        final_filter = []
        for f in filters:
            if f[0].find('__like') > -1:
                final_filter = self._like(f, final_filter)
            else:
                final_filter.append(f)
        return [Q(x) for x in final_filter]

    def filter(self, filters=None):
        if filters:
            final_filter = []
            for k, v in json.loads(str(filters).replace("'", "\"")).items():
                final_filter.append((str(k), str(v)))
            return self.model.objects.filter(reduce(operator.and_, self.format(final_filter)))
        else:
            return self.model.objects.all()


@csrf_exempt
def get_object(request):
    model = ContentType.objects.get(app_label=request.POST.get('app_label', ''),
                                    model=request.POST.get('model', ''))
    instance = model.get_object_for_this_type(id=int(request.POST.get('id', '')))
    return HttpResponse(json.dumps(instance.to_json(), cls=Codec), content_type='application/json')


@csrf_exempt
def get_collection(request):
    queryset = Filter(app_label=request.POST.get('app_label'),
                      model_name=request.POST.get('model')).filter(request.POST.get('filters', None))
    return HttpResponse(json.dumps([x.to_json() for x in queryset], cls=Codec),
                        content_type='application/json')
