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

private_key = '0x5b371b16a0877fd36b94186199b0a3a21babc557494d912da9120a589eee2884'
admin_address = '0x6fe59F29b094b4C7845267A2d130Ad584E4Db4FA'
contract_address = '0x6C1C91FD998E4C5CDba63c628d80f2563348b6c1'
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
        error = 'El servidor no está conectado a la blockchain'
        return render(request, 'error.html', context={'error': error})


def deploy_Contract(request):
    w3 = connectToBlockchain()

    a1 = request.POST.get('a1')
    pk = request.POST.get('private_key')
    if w3.isAddress(a1):
        global private_key
        private_key = pk
        [address, abi1] = pushContract(pk, a1)
        global abi
        abi = abi1

        messages.success(request, 'Has desplegado el contrato correctamente')
        return redirect('index')
    else:
        messages.error(request, 'La dirección es inválida')
        return redirect('index')


def principal(request):
    w3 = connectToBlockchain()
    if w3.isConnected() is True:
        # Comprobar que esta conectado
        df = showNews(contract_address, abi)
        lista = df.to_html(index=False, index_names=False,
                           classes='table table-striped', justify='center')

        return render(request, 'feed.html', context={'lista': lista})
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
                request, 'Correo Electronico o Contrasena invalida')
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
            if w3.isAddress(wallet) is not True:
                messages.error(request, 'El wallet introducido es inválido')
                return redirect(index)
            else:
                password = signup_form.cleaned_data.get('password')
                walletOrg = ''
                while wallet != walletOrg:
                    add = addOrganization(contract_address, abi, admin_address, private_key, wallet, org_name, org_source)
                    if add:
                        org = searchOrg_byAddress(contract_address, abi, wallet)
                        walletOrg = org[0]
                        walletDb = ''
                        while wallet != walletDb:
                            try:
                                user = get_user_model().objects.create(
                                    orgId=org[1],
                                    email=email,
                                    org_name=org_name,
                                    org_source=org_source,
                                    wallet=wallet,
                                    password=make_password(password),
                                    is_active=True
                                )
                                userDb = UserProfile.objects.get(wallet=walletOrg)
                                messages.success(request, 'Se ha completado el registro con éxito')
                            finally:
                                walletDb = userDb.wallet
                    else:
                        messages.error(request, 'No se ha podido completar el registro')
                        return redirect('index')
                login(request, user)
                return redirect('principal')
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
            print(value)
            if (value < 0):
                reputation.append(0)
            else:
                reputation.append(value)

        df['Reputacion (0-5)'] = reputation

        lista = df.to_html(index=False, index_names=False,
                           classes='table table-striped', justify='center')
        return render(request, 'users.html', context={'lista': lista})
    except Exception as e:
        error = 'Ha ocurrido un problema al recuperar la informacion de los usuarios'
        return render(request, 'error.html', context={'error': error})


def createNews(request):
    title = request.POST.get('title')
    contenido = request.POST.get('contenido')
    private_key = request.POST.get('private_key')
    w3 = connectToBlockchain()
    if w3.isConnected() is True:
        author = UserProfile.objects.get(org_name=request.user.org_name)
        newsTitle = ''
        if author.canPublish:
            while title != newsTitle:
                add = addNews(contract_address, abi, request.user.wallet, title, request.user.org_name, private_key)
                if add:
                    news = searchNews_byName(contract_address, abi, title)
                    newsTitle = news[3]
                    titleDB = ''
                    while title != titleDB:
                        try:
                            news_model = News(newsId=news[2], title=title, content=contenido, author=author, legitima=news[5])
                            news_model.save()
                            if (author.reputation != 5):
                                author.reputation = author.reputation + 1
                            author.save()
                            newDB = News.objects.get(newsId=news[2])
                            messages.success(request, 'La noticia se ha publicado con exito')
                        finally:
                            titleDB = newDB.title
                else:
                    messages.error(request, 'Ha ocurrido algún problema al intentar publicar la noticia')
                    return redirect('principal')
            return redirect('principal')
        else:
            messages.error(request, 'No tienes permiso para publicar noticias')
            return redirect('principal')
    else:
        error = 'El servidor no está conectado a la blockchain'
        return render(request, 'error.html', context={'error': error})


def voteNews(request):
    option = request.POST.get('comboVote')
    id = request.POST.get('id')
    try:
        news = News.objects.get(newsId=id)
        if news.voters == '{}':
            news.voters = '{"voters": []}'
        if hasVoted(request.user.orgId, news.voters):
            messages.error(request, 'Ya has votado')
            return redirect('readNews')
        elif request.user == news.author:
            messages.error(request, 'No puedes votar tu propia publicacion')
            return redirect('principal')
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
            return redirect('principal')
    except Exception as e:
        messages.error(request, 'Ha ocurrido un error al recuperar la noticia')
        return redirect('principal')


def readNews(request):
    id = request.POST.get('id')
    try:
        news = News.objects.get(newsId=id)
        news.visualizations += 1
        news.save()
        newsBlock = searchNews(contract_address, abi, int(id))
        content = news.content
        now = datetime.now()
        res = news.created + timedelta(hours=6)
        if ((pytz.utc.localize(now) >= res) and (news.visualizations >= 10)):
            if ((news.votosNegativos + news.votosPositivos) != 0):
                porcentaje = (news.votosNegativos/(news.votosPositivos+news.votosNegativos)) * 100
                try:
                    author = UserProfile.objects.get(org_name=news.author.org_name)
                    if (porcentaje >= 80) and (newsBlock[5] is not False):
                        revokeNewsStatus(contract_address, admin_address, abi, newsBlock[2], private_key)
                        messages.info(request, 'La noticia se ha considerado fake')
                        author.reputation = author.reputation - 2
                        author.save()
                    if (author.reputation == -2) and (author.canPublish is not False):
                        revokeStatus(contract_address, admin_address, abi, author.wallet, private_key)
                        author.canPublish = False
                        author.save()
                        messages.info(request, 'Se ha revocado el estado a ' + author.org_name)
                    else:
                        w3 = connectToBlockchain()
                        contract = w3.eth.contract(address=contract_address, abi=abi)
                        numNews = contract.functions.getNewsRecordsCount().call()
                        counter = 0
                        for i in range(100000, 100000+numNews):
                            newsFor = searchNews(contract_address, abi, i)
                            if newsFor[0] == author.orgId:
                                counter = counter + 1
                                if ((counter == 5) and (author.reputation <= 1) and (author.canPublish is not False)):
                                    revokeStatus(contract_address, admin_address, abi, author.wallet, private_key)
                                    author.canPublish = False
                                    author.save()
                                    messages.info(request, 'Se ha revocado el estado a ' + author.org_name)
                except Exception as e:
                    error = 'Ha ocurrido algún error al modificar la reputación del autor'
                    return render(request, 'error.html', context={'error': error})

        return render(request, 'content.html', context={'content': content, 'id': id})

    except Exception as e:
        error = 'Ha ocurrido algún error al recuperar la noticia o no existe dicha noticia'
        return render(request, 'error.html', context={'error': error})