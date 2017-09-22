from .utils import json, Codec, Filter
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_object(request):
    instance = Filter(app_label=request.POST.get('app_label'),
                      model_name=request.POST.get('model')
                      ).get_instance(int(request.POST.get('id')))
    return HttpResponse(json.dumps(instance.to_json(), cls=Codec), content_type='application/json')


@csrf_exempt
def get_collection(request):
    queryset = Filter(app_label=request.POST.get('app_label'),
                      model_name=request.POST.get('model')).filter_by_json(request.POST.get('filters', None))
    return HttpResponse(json.dumps([x.to_json() for x in queryset], cls=Codec),
                        content_type='application/json')


@csrf_exempt
def autocomplete(request):
    result = []
    column = request.GET.get('column_name')
    queryset = Filter(app_label=request.GET.get('app_label'),
                      model_name=request.GET.get('model')
                      ).filter_by_list(
        [('{}__like'.format(column),
          request.GET.get('term')), ])
    for q in queryset:
        result.append({'obj': q.to_json(),
                       'label': str(q),
                       'value': q.to_json()[column]})
    return HttpResponse(json.dumps(result, cls=Codec), content_type="application/json")


@csrf_exempt
def object_execute(request):
    instance = Filter(app_label=request.POST.get('app_label'),
                      model_name=request.POST.get('model')
                      ).get_instance(int(request.POST.get('id')))
    try:
        result = getattr(instance, request.POST.get('method'))(request)
    except:
        try:
            result = getattr(instance, request.POST.get('method'))()
        except:
            result = str(getattr(instance, request.POST.get('method')))
    return HttpResponse(json.dumps({'result': result}, cls=Codec), content_type='application/json')
