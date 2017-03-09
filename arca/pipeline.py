from inblensa.models import Profile


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        foto = response['image']['url']
        perfil = Profile.objects.filter(user=user).first()
        if perfil:
            perfil.foto=foto.replace('?sz=50','')
        else:
            perfil, create = Profile.objects.get_or_create(user=user)
            perfil.foto = foto.replace('?sz=50','')
        perfil.save()