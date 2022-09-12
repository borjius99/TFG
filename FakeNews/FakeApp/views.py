from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .functions import *
import pandas as pd
from pandas import json_normalize
import re
import json
import pytz
from datetime import datetime, timedelta

from .forms import UserLoginForm, UserSignUpForm
from .models import *

private_key = ''
admin_address = ''
contract_address = ''
abi = getAbi()


def index(request):
    w3 = connectToBlockchain()
    # Comprobar que esta conectado
    x = w3.isConnected()
    if x is True:
        if w3.eth.get_block_number() == 0:
            not_deploy = True
        else:
            not_deploy = False
            if request.user.is_authenticated:
                return redirect('principal')
        return render(request, 'header.html', context={'not_deploy': not_deploy})
    else:
        messages.error(request, 'El servidor no está conectado a la blockchain')
        return render(request, 'header.html')


def principal(request):
    w3 = connectToBlockchain()
    if w3.isConnected() is True:
        # Comprobar que esta conectado
        try:
            df = showNews(contract_address, abi)
            if not df.empty:
                lista = df.to_html(index=False, index_names=False,
                                   classes='table table-striped', justify='left')

                return render(request, 'feed.html', context={'lista': lista})
            else:
                return render(request, 'feed.html', context={'empty': df.empty})
        except Exception as e:
            error = 'Ha ocurrido algún problema al recuperar las noticias'
            return render(request, 'error.html', context={'error': error})
    else:
        error = 'El servidor no está conectado a la blockchain'
        return render(request, 'error.html', context={'error': error})


def login_view(request):
    login_form = UserLoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Has iniciado sesion correctamente')
            return redirect('principal')
        else:
            messages.warning(
                request, 'Correo Electronico o Contraseña invalida')
            return redirect('index')

    messages.error(request, 'Formulario Invalido')

    return render(request, 'login.html', context={'login_form': login_form})


def signup_view(request):
    signup_form = UserSignUpForm(request.POST or None)
    w3 = connectToBlockchain()
    if w3.isConnected() is True:
        if signup_form.is_valid():
            email = signup_form.cleaned_data.get('email')
            org_name = signup_form.cleaned_data.get('org_name')
            org_source = signup_form.cleaned_data.get('org_source')
            wallet = signup_form.cleaned_data.get('wallet')
            private = signup_form.cleaned_data.get('private')
            if UserProfile.objects.filter(email=email).exists() is True:
                messages.error(request, 'Hay una cuenta existente con ese email')
                return redirect('index')
            if UserProfile.objects.filter(wallet=wallet).exists() is True:
                messages.error(request, 'Hay una cuenta existente con esa Wallet')
                return redirect('index')
            if w3.isAddress(wallet) is not True:
                messages.error(request, 'El wallet introducido es inválido')
                return redirect('index')
            else:
                password = signup_form.cleaned_data.get('password')
                count = getOrgCount(contract_address, abi)
                try:
                    user = get_user_model().objects.create(
                        orgId=count,
                        email=email,
                        org_name=org_name,
                        org_source=org_source,
                        wallet=wallet,
                        password=make_password(password),
                        is_active=True
                    )
                    userDb = UserProfile.objects.get(wallet=wallet)
                    if userDb.wallet is not None:
                        add = addOrganization(contract_address, abi, private, wallet, org_name, org_source)
                        if add:
                            org = searchOrg_byAddress(contract_address, abi, wallet)
                        else:
                            userDb.delete()
                            raise
                except Exception as e:
                    messages.error(request, 'Se ha producido un problema en el registro')
                    return redirect('index')

            login(request, user)
            messages.success(request, 'Registro completado con éxito')
            return redirect('principal')
        else:
            messages.error(request, 'Se ha producido un problema en el registro')
            return redirect('index')
    else:
        error = 'El servidor no está conectado a la blockchain'
        return render(request, 'error.html', context={'error': error})


def logout_view(request):
    logout(request)
    return redirect('index')


def search_user(request):
    try:
        [df, numUsers] = searchUsers(contract_address, abi)
        reputation = []
        for i in range(1, numUsers+1):
            x = UserProfile.objects.all()
            value = x.values()[i]['reputation']
            if (value < 0):
                reputation.append(0)
            else:
                reputation.append(value)

        df['Reputacion (0-5)'] = reputation

        lista = df.to_html(index=False, index_names=False,
                           classes='table table-striped', justify='left')
        return render(request, 'users.html', context={'lista': lista})
    except Exception as e:
        error = 'Ha ocurrido un problema al recuperar la informacion de los usuarios'
        return render(request, 'error.html', context={'error': error})


def createNews(request):
    title = request.POST.get('title')
    contenido = request.POST.get('contenido')
    url = request.POST.get('url')
    editor = request.POST.get('editor')
    private_key = request.POST.get('private_key')
    w3 = connectToBlockchain()
    if w3.isConnected() is True:
        aux = searchNews_byName(contract_address, abi, title)
        if aux is None:
            author = UserProfile.objects.get(org_name=request.user.org_name)
            if author.canPublish:
                count = getNewsCount(contract_address, abi)
                try:
                    news_model = News(newsId=100000+count, title=title, content=contenido, url=url, author=author, legitima=True)
                    news_model.save()
                    newDB = News.objects.get(title=title)
                    if newDB.title is not None:
                        add = addNews(contract_address, abi, request.user.wallet, title, editor, private_key)
                        if add:
                            if author.reputation >= 5:
                                author.reputation = author.reputation
                            else:
                                author.reputation = author.reputation + 1
                            author.save()
                            news = searchNews_byName(contract_address, abi, title)
                            newsTitle = news[3]
                        else:
                            newDB.delete()
                            raise
                except Exception as e:
                    messages.error(request, 'Ha ocurrido algún problema al intentar publicar la noticia')
                    return redirect('principal')

                messages.success(request, 'La noticia se ha creado con éxito')
                return redirect('principal')
            else:
                messages.error(request, 'No tienes permiso para publicar noticias')
                return redirect('principal')
        else:
            messages.error(request, 'Ya existe una noticia con ese nombre')
            return redirect('principal')
    else:
        error = 'El servidor no está conectado a la blockchain'
        return render(request, 'error.html', context={'error': error})


def voteNews(request):
    option = request.POST.get('comboVote')
    id = request.POST.get('id')
    request.session['id'] = int(id)
    try:
        news = News.objects.get(newsId=id)
        if request.user.canPublish:
            if news.voters == '{}':
                news.voters = '{"voters": []}'
            if hasVoted(request.user.orgId, news.voters):
                messages.error(request, 'Ya has votado')
                return redirect('read')
            elif request.user == news.author:
                messages.error(request, 'No puedes votar tu propia publicacion')
                return redirect('read')
            else:
                if (option == "0"):
                    news.votosNegativos += 1
                else:
                    news.votosPositivos += 1
                votes = json.loads(news.voters)
                votes["voters"].append(request.user.orgId)
                votes_json = json.dumps(votes)
                news.voters = votes_json
                news.save()
                messages.success(request, 'Has votado correctamente')
                return redirect('principal')
        else:
            messages.error(request, 'No tienes permiso para votar')
            return redirect('principal')
    except Exception as e:
        messages.error(request, 'Ha ocurrido un error al recuperar la noticia')
        return redirect('principal')


def readNews(request):
    id = request.POST.get('id')
    if id is None:
        id = request.session['id']
    w3 = connectToBlockchain()
    if w3.isConnected() is True:
        try:
            newsBlock = searchNews(contract_address, abi, int(id))
            news = News.objects.get(newsId=id)
            news.visualizations += 1
            news.save()
            content = news.content
            title = news.title
            url = news.url
            orgName = news.author
            now = datetime.now()
            res = news.created + timedelta(hours=6)
            if ((pytz.utc.localize(now) >= res) and (news.visualizations >= 10)):
                if ((news.votosNegativos + news.votosPositivos) != 0):
                    porcentaje = (news.votosNegativos/(news.votosPositivos+news.votosNegativos)) * 100
                    try:
                        author = UserProfile.objects.get(org_name=news.author.org_name)
                        if (porcentaje >= 80) and (newsBlock[5] is not False):
                            if revokeNewsStatus(contract_address, admin_address, abi, newsBlock[2], private_key):
                                news.legitima = False
                                news.save()
                                messages.info(request, 'La noticia se ha considerado fake')
                                author.reputation = author.reputation - 2
                                author.save()
                            else:
                                messages, error(request, 'Se ha producido un error al cambiar el estado de la noticia')
                                return redirect('principal')
                        if (author.reputation == -2) and (author.canPublish is not False):
                            revokeStatus(contract_address, admin_address, abi, author.wallet, private_key)
                            author.canPublish = False
                            author.save()
                            messages.info(request, 'Se ha revocado el estado a ' + author.org_name)
                        elif (author.canPublish is not False):
                            newsList = getListNewsOrg(contract_address, abi, author.orgId)
                            counter = len(newsList)
                            if ((counter >= 5) and (author.reputation <= 1) and (author.canPublish is not False)):
                                revokeStatus(contract_address, admin_address, abi, author.wallet, private_key)
                                author.canPublish = False
                                author.save()
                                messages.info(request, 'Se ha revocado el estado a la Organización "' + author.org_name + '"')
                    except Exception as e:
                        error = 'Ha ocurrido algún error al modificar la reputación del autor'
                        return render(request, 'error.html', context={'error': error})

            return render(request, 'content.html', context={'content': content, 'url': url, 'org_name': orgName, 'id': id, 'title': title, 'estado': news.legitima})

        except Exception as e:
            error = 'Ha ocurrido algún error al recuperar la noticia o no existe dicha noticia'
            return render(request, 'error.html', context={'error': error})
    error = 'El servidor no está conectado a la blockchain'
    return render(request, 'error.html', context={'error': error})


def profile(request):
    id = request.POST.get('id')
    w3 = connectToBlockchain()
    if w3.isConnected() is True:
        try:
            author = UserProfile.objects.get(orgId=int(id))
            df = searchOrgNews(contract_address, abi, int(id))
            lista = df.to_html(index=False, index_names=False,
                               classes='table table-striped', justify='left')
            return render(request, 'profile.html', context={'lista': lista,
                                                            'source': author.org_source,
                                                            'name': author.org_name})
        except Exception as e:
            messages.error(request, 'No existe usuario con ese ID')
            return redirect('search_user')
    else:
        error = 'El servidor no está conectado a la blockchain'
        return render(request, 'error.html', context={'error': error})
