import json

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from .models import Phones, PhonesWithOpinions, PhoneComments


def index(request):
    raw_phones = Phones.objects.all()
    phones = PhonesWithOpinions.objects.all()
    # Hacky way to do the join on two models
    for phone in phones:
        phone_url = raw_phones.get(phone_name=phone.phone_name).phone_url
        setattr(phone, 'phone_url', phone_url)
    return render(request, 'index.html', locals())


def phone(request, phone_id):
    phone = PhonesWithOpinions.objects.filter(id=phone_id)[0]
    opinion_array = [
                        ['正面', float(phone.positive)],
                        ['负面', float(phone.negative)]
                    ]
    comments = PhoneComments.objects.filter(phone_name=phone.phone_name)
    return render(request, 'phone.html',
                  {
                    'opinion_data': json.dumps(opinion_array),
                    'phone': phone,
                    'comments': comments
                  },
                  locals())


def search(request):
    if 'comment_keyword' in request.GET:
        kw = request.GET['comment_keyword']
        comments = PhoneComments.objects.filter(comment_content__contains=kw)
        return render(request, 'comments.html', locals())
    elif 'start_date' in request.GET and 'end_date' in request.GET:
        s_date = request.GET['start_date']
        e_date = request.GET['end_date']
        if not s_date or not e_date:
            return HttpResponse('Bad request for search!', status=400)
        comments = PhoneComments.objects.filter(comment_date__gte=s_date,
                                                comment_date__lte=e_date)
        return render(request, 'comments.html', locals())
    else:
        return HttpResponse('Bad request for search!', status=400)

    return HttpResponse('Search request has been received!')
