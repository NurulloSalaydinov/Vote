from django.shortcuts import render
from .models import Category,Places,BotUser
from django.http import HttpResponse,JsonResponse
from django.core import serializers
def home(request):
    category = Category.objects.all()
    places = Places.objects.select_related("bind").all()
    arr = []
    res = []
    num = 0
    for i in category:
        for z in places:
            if z.bind == i:
                arr.append(z)
        for d in arr:
            res.append(d.vote)
        for f in arr:
            num += 1
            y = sum(res) / 100
            if y <= 0:
                per = 0
            else:
                per = f.vote / y
            f.percent = round(per, 2)
            f.count = num
            # f.save()
        num = 0
        res = []
        arr = []
    context = {
        "lists":category,
        "lis2":places
    }
    return render(request,'index/index.html',context)

def userspage(request):
    if request.user.is_staff:
        category = Category.objects.all()
        place = Places.objects.select_related("bind").all()
        user = BotUser.objects.select_related('voted').select_related('category').all()
        data = {}
        if request.GET:
            rescategory = request.GET.get('category')
            if rescategory != "-----":
                data['status'] = 200
                if rescategory == "all":
                    data['ref'] = serializers.serialize('json', place)
                else:
                    res = place.filter(bind=category.get(name=rescategory).id)
                    data['ref'] = serializers.serialize('json', res)
                return JsonResponse(data)
            else:
                pass
        else:
            data['status'] = 404
        ################################################
        num = 0
        for i in user:
            num += 1
            i.count = num
        num = 0
        context = {
            "users": user,
            "categories":category,
        }
        return render(request, 'user/users.html', context)
    else:
        return HttpResponse("<h1 style='text-align:center;'>Kechirasiz adminlik huquqiga ko'ra siz bu sahifaga kira olmaysiz </h1>")

def partners(request):
    return render(request,'partner/partners.html')

def getfilteruser(request):
    text = ""
    if request.GET:
        resplaces = request.GET.get('places')
        if resplaces != "-----":
            num = 0
            respl = Places.objects.select_related("bind").get(name=resplaces).id
            result = BotUser.objects.select_related('voted').select_related('category').filter(voted=respl)
            for z in result:
                num +=1
                z.count = num
                text += f"""
                            <tr>
                              <th scope="row">{z.count}</th>
                              <td>{z.name}</td>
                              <td>
                                <a href="tel:+{z.phonenumber}" target="_blank">+{z.phonenumber}</a>
                              </td>
                              <td>
                                <a href="http://t.me/{z.username}" target="_blank">{z.username}</a>
                              </td>
                              <td>{z.voted} ga</td>
                              <td>{z.date} da</td>
                              <td>{z.age} yoshda</td>
                            </tr>
                        """
    return HttpResponse(text)