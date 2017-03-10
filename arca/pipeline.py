from arca.models import Usuario as Perfil


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        foto = response['image']['url']
        perfil = Perfil.objects.filter(user=user).first()
        if perfil:
            perfil.foto=foto.replace('?sz=50','')
        else:
            perfil, create = Perfil.objects.get_or_create(user=user)
            perfil.foto = foto.replace('?sz=50','')
        perfil.save()
