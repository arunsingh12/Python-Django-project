from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.shortcuts import render,get_object_or_404
from product.models import *
from .forms import NewForm
from .models import Product
from .models import Ureg

import os
from ecom_store import settings

def index(request):
    template = loader.get_template('index.html')
    context = {'tfmess': 'False'}
    context['cateobj'] = cateobj = Cate.objects.all()
    context['bobj'] = bobj = Product.objects.all()
    context['robj'] = robj = Rating.objects.all()

    c, t = 0, 0
    for b in bobj:
        c, t = 0, 0
        for r in robj:
            if b.Prod_title == r.rtitle:
                c += int(r.rval)
        t = float(c / 5)
        b.Prod_rating = float(t)
        b.save()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

    return HttpResponse(template.render(context,request))

def login(request):
    template = loader.get_template('login.html')
    context = {'tfmess': 'False'}
    request.session.flush()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

    if request.method == 'POST':

        umail = request.POST.get('uemail')
        upass = request.POST.get('upass')

        for x in Ureg.objects.all():
            if x.umail == umail and x.upass == upass:

                request.session['umail'] = umail

                if x.utype == 'customer':

                    return redirect('index')

                if x.utype == 'provider':
                    return redirect('pro_home')

        context['message'] = "Permission denied, your mail didn't approved"

    return HttpResponse(template.render(context,request))

def reg(request):
    template = loader.get_template('register.html')
    context = {'mess': '', 'tfmess': 'False'}
    request.session.flush()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

    if request.method == 'POST':
        uname = request.POST.get('uname')
        umail = request.POST.get('umail')
        upass = request.POST.get('upass')
        upass1 = request.POST.get('upass1')
        ufname = request.POST.get('ufname')
        usname = request.POST.get('usname')
        uaddr = request.POST.get('uaddr')
        uphone = request.POST.get('uphone')

        utype = 'customer'

        if upass != upass1:
            context['mess'] = 'Password Mismatch'

        try:
            if len(uphone) != 10:
                context['mess'] = 'Enter Proper Phone Number'
            uphone = int(uphone)
        except:
            context['mess'] = 'Enter Proper Phone Number'

        if context['mess'] == '':
            for x in Ureg.objects.all():
                if x.umail == umail:
                    context['mess'] = 'mail id is already registered'

            if context['mess'] != 'mail id is already registered':
                ucobj = Ureg.objects.create(
                    uname=uname,
                    umail=umail,
                    upass=upass,
                    ufname=ufname,
                    usname=usname,
                    uaddr=uaddr,
                    uphone=uphone,
                    utype=utype
                )
                ucobj.save()
                context['mess'] = 'Registration Successful'
                return redirect('regack')

    return HttpResponse(template.render(context,request))

def reg_ack(request):
    template = loader.get_template('registration_acknowledgement.html')
    context = {'mess': ''}

    request.session.flush()

    return HttpResponse(template.render(context, request))

def search(request):
    template = loader.get_template('search.html')
    context = {'mess': "",'tfmess': 'False'}
    nnn = ''
    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

    context['cobj'] = cobj = Cate.objects.all()
    context['bobj'] = bobj = Product.objects.all()

    if request.method == 'POST':

        context['sval'] = sval = (request.POST.get('sval')).title()

        if sval == '':
            return redirect('index')

        for x in bobj:
            if x.Prod_manufacture == sval or x.Prod_genre == sval or x.Prod_title == sval or x.Prod_weight == sval:
                nnn = 'True'

        if nnn == '':
            context['mess'] = 'Results not found'

    return HttpResponse(template.render(context, request))

def cate(request, prod_id):
    template = loader.get_template('cate.html')
    context = {'mess': "",'tfmess': 'False'}
    val = 0

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

    context['cn'] = cn = Cate.objects.get(id=prod_id)

    context['cobj'] = cobj = Cate.objects.all()
    context['bobj'] = bobj = Product.objects.all()

    for x in bobj:
        if x.Prod_genre == cn.cate_name:
            val = 1

    if val == 0:
        context['mess'] = 'No Product Available'

    return HttpResponse(template.render(context, request))

def sprod(request, prod_id):
    template = loader.get_template('singleproduct.html')
    context = {'mess': "single",'tfmess': 'False'}
    request.session['bid'] = None
    count = []

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

    context['cn'] = cn = Product.objects.get(id=prod_id)
    request.session['bid'] = cn.id

    context['cobj'] = cobj = Cate.objects.all()
    context['bobj'] = bobj = Product.objects.all()
    context['bcobj'] = bcobj = Prodcomm.objects.all()

    for x in range(1, cn.Prod_no_of_items+1):
        count.append(x)
    context['count'] = count

    if request.method == 'POST':
        if request.session.has_key('umail'):
            ctext = request.POST.get('ctext')
            if ctext != '':
                obj = Prodcomm.objects.create(Prod_title=cn.Prod_title, Prod_com=ctext, Prod_umail=umail)
                obj.save()
        else:
            return redirect('login')

    return HttpResponse(template.render(context, request))

def logout(request):
    template = loader.get_template('logout.html')
    context = {'mess': ''}

    request.session.flush()

    return redirect('index')

#--------------------- provider -------------------

def pro_home(request):
    template = loader.get_template('provider/pro_home.html')
    context = {'mess': ""}

    uobjmail = request.session['umail']
    context['bobj'] = bobj = Product.objects.all()

    return HttpResponse(template.render(context, request))

def pro_add_Product(request):
    template = loader.get_template('provider/pro_add_Product.html')
    context = {'mess': ""}
    context['cateobj'] = cateobj = Cate.objects.all()
    bobj = Product.objects.all()
    uobjmail = request.session['umail']

    if request.method == 'POST':
        context['val'] = 'no'
        title = (request.POST.get('Prod_title')).title()
        genre =(request.POST.get('genre'))
        model_no =(request.POST.get('model_no'))
        manufacture =(request.POST.get('manufacture')).title()
        weight =(request.POST.get('weight')).title()
        items =(request.POST.get('items'))
        price =(request.POST.get('price'))
        year =(request.POST.get('year'))
        desc =(request.POST.get('des'))
        fupload = request.FILES['photo']

        if len(year) != 4:
            context['mess'] = 'enter proper year'

        for x in bobj:
            if x.Prod_title == title:
                context['mess'] = 'Title Already Exist'

        try:
            year = int(year)
        except:
            context['mess'] = 'enter proper year'

        if context['mess'] == '':
            upobj = Product.objects.create(
                Prod_title=title,
                Prod_manufacture=manufacture,
                Prod_no_of_items=items,
                Prod_description=desc,
                Prod_image=fupload,
                Prod_model_no=model_no,
                Prod_pmail=uobjmail,
                Prod_year=year,
                Prod_weight=weight,
                Prod_price=price,
                Prod_genre=genre
            )

            upobj.save()
            context['mess'] = 'Product added Successfully'

    return HttpResponse(template.render(context, request))

def pro_report(request):
    template = loader.get_template('provider/pro_reports.html')
    context = {'mess': "",'dis':''}
    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Product.objects.all()

    for n in cobj:
        for x in bobj:
            if n.c_Prod_id == x.id and n.cstat == 'yes':
                context['dis'] = 'yes'


    return HttpResponse(template.render(context, request))

def pro_add_cate(request):
    template = loader.get_template('provider/pro_add_cate.html')
    context = {'mess': ""}
    context['cobj'] = cobj = Cate.objects.all()

    if request.method == 'POST':
        cate = str(request.POST.get('cate')).title()
        fimg = request.FILES['fimg']

        for x in cobj:
            if x.cate_name.title() == cate:
                context['mess'] = 'Category already exists'

        if context['mess'] == '':

            obj = Cate.objects.create(
                cate_name=cate,
                cate_img=fimg
            )

            obj.save()

            return redirect('pro_add_cate')

    return HttpResponse(template.render(context, request))

def ureg_view(request,):
   slist = Ureg.objects.all()
   MyDict = {'slist':slist}
   return render(request,'provider/ureg_view.html',MyDict)

def ureg_delete(request,id=None):
	instance =get_object_or_404(Ureg,id=id)
	instance.delete()
	return render(request,"provider/delete.html")


#--------------------- customer -------------------

def cart0(request):
    template = loader.get_template('cart0.html')
    context = {'mess': "single", 'tot': '', 'tfmess': 'False'}
    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Product.objects.all()

    tit, c, id = '', 0, 0
    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

        if request.session.has_key('bid'):
            context['bid'] = bid = request.session['bid']
            selno = request.POST.get('selno')
            selno = int(selno)
            obj = Product.objects.get(id=bid)

            for n in cobj:
                if n.c_Prod_mail == umail and obj.Prod_title == n.c_Prod_title and n.cstat == 'no':
                    c = 1
                    n.ccost += int(int(obj.Prod_price) * int(selno))
                    n.cno += selno
                    n.save()

            if c == 0:
                cmobj = Cart.objects.create(
                    c_Prod_id= bid,
                    c_Prod_title= obj.Prod_title,
                    c_Prod_mail= umail,
                    ccost= (int(obj.Prod_price) * int(selno)),
                    cno=selno
                )
                cmobj.save()

            obj.Prod_no_of_items -= int(selno)
            obj.save()
            return redirect('cart')
    else:
        return redirect('login')

def cart(request):
    template = loader.get_template('cart.html')
    context = {'mess': "", 'tot':0, 'tfmess': 'False'}
    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Product.objects.all()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

        context['addr'] = addr = Ureg.objects.get(umail=umail)

        for b in bobj:
            for c in cobj:
                if c.c_Prod_mail == umail and c.c_Prod_title == b.Prod_title and c.cstat == 'no':
                    context['tot'] += c.ccost

        if request.method == 'POST':
            uobj = Ureg.objects.get(umail=umail)
            caddr1 = request.POST.get('caddr1')
            caddr2 = request.POST.get('caddr2')
            rval = request.POST.get('eradio')
            bval = request.POST.get('bradio')
            cardname = request.POST.get('cardname')
            card = request.POST.get('card')
            cvv = request.POST.get('cvv')
            dcardname = request.POST.get('dcardname')
            dcard = request.POST.get('dcard')
            dcvv = request.POST.get('dcvv')

            if rval == 'nval':
                if len(caddr2) > 0:
                    context['mess'] = ''
                else:
                    context['mess'] = 'Enter Proper Address'

            if bval == 'eval':
                if len(card) == 12 and len(cvv) == 3 and len(cardname) > 0:
                    try:
                        cd = int(card)
                        cv = int(cvv)
                    except:
                        context['mess'] = 'enter card details properly'
                else:
                    context['mess'] = 'enter card details properly'

            if bval == 'dval':
                if len(dcard) == 12 and len(dcvv) == 3 and len(dcardname) > 0:
                    try:
                        cd = int(dcard)
                        cv = int(dcvv)
                    except:
                        context['mess'] = 'enter card details properly'
                else:
                    context['mess'] = 'enter card details properly'

            if context['mess'] == '':
                for b in bobj:
                    for c in cobj:
                        if c.c_Prod_title == b.Prod_title and c.cstat == 'no':
                            c.cstat = 'yes'
                            c.save()

                context['tot'] = 0

                if rval == 'eval':
                    uobj.save()
                    context['mess'] = 'Orders placed successfully, please check reports for adding rating'

                if rval == 'nval':
                    if caddr2 != '' or caddr2 != None:
                        uobj.uaddr = caddr2
                        uobj.save()
                        context['mess'] = 'Orders placed successfully, please check for reports'

    return HttpResponse(template.render(context, request))

def orders(request):
    template = loader.get_template('orders.html')
    context = {'mess': "", 'tfmess': 'False','dis':''}

    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Product.objects.all()
    context['robj'] = robj = Rating.objects.all()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

        for n in cobj:
            for x in bobj:
                if n.c_Prod_mail == umail and n.c_Prod_id == x.id and n.cstat == 'yes':
                    context['dis'] = 'yes'

        c, t, ctot = 0, 0, 0
        for b in bobj:
            c, t, ctot = 0, 0, 0
            for r in robj:
                if b.Prod_title == r.rtitle:
                    ctot += 1

            for r in robj:
                if b.Prod_title == r.rtitle:
                    c += int(r.rval)

            if ctot > 0:
                t = float(c / ctot)
                t = round(t, 1)
            b.Prod_rating = float(t)
            b.save()

        for x in cobj:
            if x.c_Prod_mail == umail and x.cstat == 'yes':
                c = 1

        if c == 0:
            context['mess'] = 'No orders to display'

        if context['mess'] == '':
            if request.method == 'POST':
                selid = int(request.POST.get('selid'))
                selrating = int(request.POST.get('selrating'))
                bid = Product.objects.get(id=selid)

                obj = Rating.objects.create(
                    rumail=umail,
                    rtitle=bid.Prod_title,
                    rval=selrating
                )
                obj.save()
                return redirect('orders')
    else:
        return redirect('login')
    return HttpResponse(template.render(context, request))

def account(request):
    template = loader.get_template('account.html')
    context = {'mess': "", 'tfmess': 'False'}
    context['umail'] = umail = request.session['umail']
    context['tfmess'] = 'True'
    context['uobj'] = uobj = Ureg.objects.get(umail=umail)

    if request.method == 'POST':

        uuobj = Ureg.objects.get(id=uobj.id)
        upass = request.POST.get('upass')
        ufname = request.POST.get('ufname')
        usname = request.POST.get('usname')
        uaddr = request.POST.get('uaddr')
        uphone = request.POST.get('uphone')


        try:
            if len(uphone) != 10:
                context['mess'] = 'Enter Proper Phone Number'
            uphone = int(uphone)
        except:
            context['mess'] = 'Enter Proper Phone Number'

        if context['mess'] == '':
            uuobj.upass = upass
            uuobj.ufname = ufname
            uuobj.usname = usname
            uuobj.uaddr = uaddr
            uuobj.uphone = uphone
            uuobj.save()
            context['mess'] = 'Account Details Updated'
            return redirect('account')

    return HttpResponse(template.render(context, request))


