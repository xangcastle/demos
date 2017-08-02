from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.forms import modelform_factory


def imprimir(request):
    model = ContentType.objects.get(app_label=request.GET.get('app', ''), model=request.GET.get('model', ''))
    instance = request.GET.get('instance', '')
    template_name = request.GET.get('template', None)
    obj = model.get_object_for_this_type(id=int(instance))
    obj.impreso = True
    obj.save()
    if not template_name:
        template_name = obj.__class__.__name__
    fields = (f.name for f in obj._meta.get_fields())
    form = modelform_factory(model.model_class(), fields=fields)
    data = {'model': model, 'instance': instance, 'obj': obj, 'form': form(obj)}
    return render(request, "print/%s.html" % template_name, data)
