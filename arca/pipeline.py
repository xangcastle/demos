from arca.crypter import encrypt_val
from arca.models import Usuario as Perfil


def save_profile(backend, user, response, *args, **kwargs):

    if backend.name == 'google-oauth2':
        foto = response['image']['url']
        if user:
            perfil = Perfil.objects.filter(username=user.username).first()
            if perfil:
                perfil.nombre=user.first_name
                perfil.apellido=user.last_name
                perfil.foto = foto.replace('?sz=50', '')
                perfil.email=user.email
            else:
                perfil, create = Perfil.objects.get_or_create(username=user.username)
                perfil.nombre = user.first_name
                perfil.apellido = user.last_name
                perfil.foto = foto.replace('?sz=50', '')
                perfil.email = user.email
            perfil.save()
            backend.strategy.request.COOKIES['auth_usuario'] = encrypt_val(perfil.id)
        else:
            perfil = Perfil.objects.filter(username=kwargs['username']).first()
            if perfil:
                perfil.nombre=response['name']['familyName']
                perfil.apellido = response['name']['givenName']
                perfil.email=response['emails'][0]['value']
                perfil.foto = foto.replace('?sz=50', '')
            else:
                perfil, create = Perfil.objects.get_or_create(username=kwargs['username'])
                perfil.nombre = response['name']['familyName']
                perfil.apellido = response['name']['givenName']
                perfil.email = response['emails'][0]['value']
                perfil.foto = foto.replace('?sz=50', '')
            perfil.save()
            backend.strategy.request.COOKIES['auth_usuario']= encrypt_val(perfil.id)