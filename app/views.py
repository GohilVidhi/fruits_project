# from django.conf import settings
from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse 
from .models import*
from django.core.mail import send_mail
import random
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.paginator import Paginator
import razorpay



# Create your views here.
def index(request):
    
    uid=User.objects.get(email=request.session['email'])
    w_count=Add_Whishlist.objects.filter(user_id=uid).count()
    
    count=addcart.objects.filter(user=uid).count()
    pp=product.objects.all().order_by("-id")
    con={'count':count,"pp":pp,"w_count":w_count}
    return render(request,"index.html",con)


def cart(request):
    uid = User.objects.get(email=request.session['email'])
    count = addcart.objects.filter(user=uid).count()
    w_count=Add_Whishlist.objects.filter(user_id=uid).count()
    
    mid = main_category.objects.all()
    ct = addcart.objects.filter(user=uid)

    print(ct)
    
    sub_total = 0
    charge = 50
    l1 = []
    t_price = 0  

    for i in ct:
        a = i.t_price
        l1.append(a)
        sub_total = sum(l1)
        t_price = sub_total + charge

    contaxt = {'mid': mid,
               'ct': ct,
               'sub_total': sub_total,
               'charge': charge,
               't_price': t_price,
               'count': count,
               "w_count":w_count}

    return render(request, "cart.html", contaxt)



def add_to_cart(request,id):
    uid=User.objects.get(email=request.session['email'])
    pid=product.objects.get(id=id)
    aid=addcart.objects.filter(products=pid,user=uid).exists()
        
    if aid:

        messages.info(request,"Product Is Already Exists")
        return redirect ('shop')

    else:
        addcart.objects.create(user=uid,
                            products=pid,
                            price=pid.price,
                            name=pid.name,
                            quantity=1,  
                            img=pid.img,
                            t_price=pid.price)

    return redirect ('cart')


def shop_add_to_card(request,id):

    pp=addcart.objects.get(id=id)
    
    contaxt={
        'pp':pp,
      
    }
    return render(request,"detail.html",contaxt)


def cart_plus(request,id):
    cart=addcart.objects.get(id=id)
    if cart:
        cart.quantity +=1
        cart.t_price=cart.quantity*cart.price
        cart.save()
        return redirect("cart")
    else:
        return redirect("cart")

def cart_mines(request,id):
    cart=addcart.objects.get(id=id)
    if cart:
        if(cart.quantity==1):
            addcart.objects.get(id=id).delete()
        else:
            cart.quantity-=1
            cart.t_price=cart.quantity*cart.price
            cart.save()
        return redirect("cart")
    else:
         
        return redirect("cart")


def delete1(request,id):
    dell=addcart.objects.filter(id=id)
    dell.delete()
    return redirect("cart")

def order_delete(request,id):
    dell=Order.objects.filter(id=id)
    dell.delete()
    return redirect("order1")

# def checkout(request):
#     uid=User.objects.get(email=request.session['email'])
#     count=addcart.objects.filter(user=uid).count()
#     pro=addcart.objects.filter(user=uid)

#     list1=[]
#     sub_total=0
#     t_price = 1
#     charge=0
#     for i in pro:
#         m = i.price*i.quantity
#         list1.append(m)
#         sub_total =sum(list1)
#         charge=50
#         t_price = sub_total  + charge
    
#     if request.POST:
#         f_name=request.POST['f_name']
#         l_name=request.POST['l_name']
#         company_name=request.POST['company_name']
#         address=request.POST['address']
#         city=request.POST['city']
#         country=request.POST['country']
#         zip_code=request.POST['zip_code']
#         mobile=request.POST['mobile']
#         email=request.POST['email']
        
        
#         billing_address.objects.create(user=uid,
#                                        f_name=f_name,
#                                        l_name=l_name,
#                                        company_name=company_name,
#                                        address=address,
#                                        city=city,
#                                        country=country,
#                                        zip_code=zip_code,
#                                        mobile=mobile,
#                                        email=email,)


#     amount = t_price*100 #100 here means 1 dollar,1 rupree if currency INR
#     client = razorpay.Client(auth=('rzp_test_uqhoYnBzHjbvGF','jEhBs6Qp9hMeGfq5FyU45cVi'))
#     response = client.order.create({'amount':amount,'currency':'INR','payment_capture':1})
#     print(response,"****************")      
    
#     contaxt={


#     'uid':uid,
#     'count':count,
#     'pro':pro,
#     't_price':t_price,
#     'sub_total':sub_total,
#     'charge':charge,
#     'response':response,


# }
#     return render(request,"checkout.html",contaxt)
import razorpay
def checkout(request):

    uid=User.objects.get(email=request.session['email'])
    aid=addcart.objects.filter(user=uid)
    count=addcart.objects.filter(user=uid).count()
    w_count=Add_Whishlist.objects.filter(user_id=uid).count()
    
    l1=[]
    sub_total=0
    charge=50
    dis=0
    t_price = 0
    for i in aid:
        l1.append(i.t_price)
        sub_total=sum(l1)
        print(sub_total)
        discount=0
        dis=None
        t_price=sub_total+charge
        
        if sub_total==0:
            charge=0
            t_price=0
        else:
            charge=50
        if "discount" in request.session:
            dis=request.session.get('discount')
            t_price=sub_total+charge-dis
            print(dis)
        else:
            dis=0
            t_price=sub_total+charge
        if t_price==0:
            con={"aid":aid,
                 "sub_total":sub_total,
                 "charge":charge,
                 "t_price":t_price,
                 "uid":uid,
                 "discount":dis,
                 'count':count,
                 "w_count":w_count}
            return render(request,"checkout.html",con)
    else:
        # Now, t_price is guaranteed to be defined
        # amount = t_price*100 #100 here means 1 dollar,1 rupree if currency INR
        # client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
        # response = client.order.create({'amount':amount,'currency':'INR','payment_capture':1})

            
        
        amount = max(t_price, 1) * 100
        client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
        response = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': 1})
            
        print(response,"**************")
        contaxt={
            "aid":aid,
            "sub_total":sub_total,
            "charge":charge,
            "t_price":t_price,
            "uid":uid,
            "response":response,
            "discount":dis,
            'count':count,
        }
        return render(request,"checkout.html",contaxt)


# def order1(request):
#     uid=User.objects.get(email=request.session['email'])
#     prod=addcart.objects.filter(user=uid).order_by('id')
#     pro=addcart.objects.filter(user=uid)

#     ord=Order.objects.filter(user_id=uid)
#     price(ord)
#     aid=addcart.objects.filter(user=uid)
    
    
    
    
    
#     if request.POST:
#         f_name=request.POST['f_name']
#         l_name=request.POST['l_name']
#         company_name=request.POST['company_name']
#         address=request.POST['address']
#         city=request.POST['city']
#         country=request.POST['country']
#         zip_code=request.POST['zip_code']
#         mobile=request.POST['mobile']
#         email=request.POST['email']
        
        
#         billing_address.objects.create(user=uid,
#                                        f_name=f_name,
#                                        l_name=l_name,
#                                        company_name=company_name,
#                                        address=address,
#                                        city=city,
#                                        country=country,
#                                        zip_code=zip_code,
#                                        mobile=mobile,
#                                        email=email,)

#     total=0
#     l1=[]
    
#     for i in aid:
#         a=i.t_price
#         l1.append(a)
#         total=sum(l1)

#     sub_total2 = sum([i.t_price for i in pro])
#     total2 = sub_total2 + 50

#     sub_total = sum([i.t_price for i in pro])
#     total = sub_total + 50
 
#     discount_amount = 0

#     total = sub_total + 50
#     main_total = total - discount_amount    
    
#     amount = total * 100
#     if amount < 100:
#         amount = 100


#     client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
#     response = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': 0})
#     order_id = response['id']
#     print(order_id)
    
    
    
    
#     for i in pro:
#         t_price=0
#         Order.objects.create(user=uid,img=i.img,product_name=i.name,price=i.price,
#                              qtn=i.quantity,product_total=i.price*i.quantity,t_price=t_price)
#         i.delete()
 
#     con={'uid':uid,
#          'prod':prod,
#          'pro':pro,
#          'ord':ord,
#          }    
                                                
#     return render(request,"order.html",con)



def billing_view(request):
    uid=User.objects.get(email=request.session['email'])
    aid=addcart.objects.filter(user=uid)
    a_count=addcart.objects.filter(user=uid).count()
    w_count=Add_Whishlist.objects.filter(user_id=uid).count()
            
    count=addcart.objects.filter(user=uid).count()
    if 'discount' in request.session:
        del request.session['discount']

    for i in aid:
        Order.objects.create(user=uid,
                             product_name=i.name,
                             img=i.img,
                             price=i.price,
                             qtn=i.quantity,
                             t_price=i.t_price)
        i.delete()
    if request.POST:
        f_name=request.POST['f_name']
        l_name=request.POST['l_name']
        company_name=request.POST['company_name']
        
        country=request.POST['country']
        address=request.POST['address']
        city=request.POST['city']

        zip_code=request.POST['zip_code']
        mobile=request.POST['mobile']

        
        billing_address.objects.create(user=uid,f_name=f_name,l_name=l_name,company_name=company_name,country=country,address=address,city=city,zip_code=zip_code,mobile=mobile,email=uid.email)
        con={'count':count,"w_count":w_count}
        return render(request,"checkout.html",con)
    else:
        con={'count':count}
        return render(request,"checkout.html",con)




def apply_coupon(request):
    uid=User.objects.get(email=request.session['email'])
    aid=addcart.objects.filter(user=uid)
    a_count=addcart.objects.filter(user=uid).count()        
    w_count=Add_Whishlist.objects.filter(user_id=uid).count()
    
    l1=[]
    sub_total=0
    charge=50
    for i in aid:
        l1.append(i.t_price)
    print(l1)
    sub_total=sum(l1)
    print(sub_total)
    t_price=sub_total+charge
    discount=0
    if request.POST:
        coupon=request.POST['code']
        print(coupon)
        caid=coupon_code.objects.filter(code=coupon).exists()
        print(caid)
        if caid:
            cid=coupon_code.objects.get(code=coupon)
            t_price-=cid.discount
            discount=cid.discount
            request.session['discount']=discount
            contaxt={
            "uid":uid,
            "aid":aid,
            "a_count":a_count,
            "sub_total":sub_total,
            "t_price":t_price,
            "charge":charge,
            "discount":discount,
            "w_count":w_count}
            
            messages.info(request,"Coupon Code Apply Successfully")
            return render(request,"cart.html",contaxt)

        else:
            contaxt={
            "uid":uid,
            "aid":aid,
            "a_count":a_count,
            "sub_total":sub_total,
            "t_price":t_price,
            "charge":charge,
            "discount":0,
            }
            messages.info(request,"No Coupons")
            return render(request,"cart.html",contaxt)
            
    else:   
        
        return render(request,"cart.html")



def error404(request):
    return render(request,"error404.html")


def shop_detail(request):
    uid=User.objects.get(email=request.session['email'])
    count=category.objects.filter(name1=uid).count()
    count=addcart.objects.filter(user=uid).count()
    w_count=Add_Whishlist.objects.filter(user_id=uid).count()
    
    con={'count':count,
         'count':count,
         "w_count":w_count}
    return render(request,"shop_detail.html",con)

def shop_detail1(request,id):
    uid=User.objects.get(email=request.session['email'])
    count=category.objects.filter(name1=uid).count()
    count=addcart.objects.filter(user=uid).count()
    cat=category.objects.all()
    cat2=request.GET.get("cat2") 
    pp=product.objects.get(id=id)
    mid=main_category.objects.all()
    w_count=Add_Whishlist.objects.filter(user_id=uid).count()

    
    contaxt={'pp':pp,
            'mid':mid,
            'cat':cat,
            'cat2':cat2,
            'count':count,
            'count':count,"w_count":w_count}
    return render(request,"shop_detail.html",contaxt)

def shop(request):
    if 'email' in request.session:
        uid=User.objects.get(email=request.session['email'])
        count=category.objects.filter(name1=uid).count()
        count=addcart.objects.filter(user=uid).count()
        pp=product.objects.all().order_by("-id")
        w_count=Add_Whishlist.objects.filter(user_id=uid).count()
        whishlist_product=Add_Whishlist.objects.filter(user_id=uid)
        l1=[]
        for i in whishlist_product:
            l1.append(i.product_id.id)
    
        mid=main_category.objects.all()
        cid=request.GET.get("cid")
        
        piz=price.objects.all()
        piz2=request.GET.get("piz2")

        cat=category.objects.all()
        cat2=request.GET.get("cat2") 
        
        S=request.GET.get("sort")
        
        if cid:
            pp=product.objects.filter(sub_category=cid)
        elif piz2:
            pp=product.objects.filter(price1=piz2)
        elif cat2:
            pp=product.objects.filter(name1=cat2)
        elif S=="lth":
            pp=product.objects.all().order_by("price") 
        elif S=="htl":
            pp=product.objects.all().order_by("-price")  
        elif S=="atz":
            pp=product.objects.all().order_by("name")
        elif S=="zta":
            pp=product.objects.all().order_by("-name")
        else:
            pp=product.objects.all().order_by("-id")
        
        paginator=Paginator(pp,9)  
        page_number=request.GET.get("page")  
        pp=paginator.get_page(page_number)

        con={'pp':pp,
            'mid':mid,
            'cat':cat,
            'piz':piz,
            "min1":0,
            'count':count,
            'count':count,
            "w_count":w_count,
            "whishlist_product":whishlist_product,"l1":l1}
        return render(request,"shop.html",con)
    else:
        return render(request,"login.html")


def filter_price(request):
    if request.POST:
        max1=request.POST['max1']
        print(max1)
        pp=product.objects.filter(price__lte=max1) 
        print(pp)
        contaxt={
            "pp":pp,
            "max1":max1,

                
        }
        return render(request,"shop.html",contaxt)
    else:
        contaxt={
        
            "min1":None
            
        }
        return render(request,"shop.html",contaxt)



def price1(request):
    price=request.GET.get("price")
    print(price)
    pid=product.objects.filter(price__lte=price)
    print(pid)
    contaxt={
        "pid":pid
    }
    return render(request,"shop.html",contaxt)
    


def testimonial(request):
    return render(request,"testimonial.html")


def logout(request):
    
    if 'email' in request.session:
        del request.session['email']
        return render(request,'login.html')
    else:
        return render(request,'login.html')

# def login(request):
    
#     if 'email' in request.session:
       
#         uid = User.objects.get(email=request.session['email'])
#         count = addcart.objects.filter(user=uid).count()
#         context = {
#             'count': count,
#         }
#         return render(request, "index.html", context)
#     try:
#         if request.POST:
#             email=request.POST['email']
#             password=request.POST['password']
#             uid=User.objects.get(email=email)
#             if uid.email==email:
#                 request.session['email']=uid.email
#                 if uid.password==password:
#                     return render(request,"index.html")
                                        
#                 else:
#                     con={
#                         'emsg': "Invalid Password",
#                     }
#                     return render(request,"login.html",con)
#             else:
#                 con={           
#                 'e_msg': "Enter Valid Email ID",
#                     }


#                 return render(request,"login.html",con)
#         else:
            
#             return render(request,"login.html")
#     except:
       
#         return render(request,"login.html")






def login(request):
    if 'email' in request.session:
        uid = User.objects.get(email=request.session['email'])
        count = addcart.objects.filter(user=uid).count()
        context = {
            'count': count,
        }
        return render(request, "index.html", context)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if user.password == password:
                request.session['email'] = user.email
                return render(request, "index.html")
            else:
                context = {'emsg': "Invalid Password"}
                return render(request, "login.html", context)
        except User.DoesNotExist:
            context = {'e_msg': "Invalid Email ID"}
            return render(request, "login.html", context)

    return render(request, "login.html")






# def confirm_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         otp = request.POST.get('otp')
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')
#         print(email, otp)
#         try:
#             uid = User.objects.get(email=email)
#             if str(uid.otp) == otp:
#                 print(otp)
#                 if new_password == confirm_password:
#                     uid.password = new_password
#                     uid.save()
#                     print("Password Successfully Changed")
#                     context = {
#                         'email': email,
#                         'uid': uid,
#                         'emsg': 'Login Password Changed Successfully'}
#                     return render(request, "index.html", context)
#                 else:
#                     print("Passwords do not match")
#                     context = {
#                         "email": email,
#                         'emsg': "Passwords do not match",}
#                     return render(request, "confirm_password.html", context)
#             else:
#                 print("Invalid OTP")
#                 context = {
#                     "email": email,
#                     'emsg': "Invalid OTP"}
#                 return render(request, "confirm_password.html", context)
#         except:
#             print("User not found")
#             context = {
#                 "email": email,
#                 'emsg': "User not found",}
#             return render(request, "confirm_password.html", context)
#     return render(request, "confirm_password.html")
 
def confirm_password(request):
    if request.POST:
        email=request.POST.get('email')
        otp=request.POST.get('otp')
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')
        
        print(email,otp)
        try:
            uid=User.objects.get(email=email)
            if str(uid.otp)==otp:
                print(otp)
                if new_password==confirm_password:
                   uid.password==new_password
                   uid.save()
                   con={'email':email,'uid':uid,'emsg':'password change successfully'}
                   return render(request,"login.html",con)
                else:
                    con={'email':email,
                         'emsg':'password do not match'}
                    return render(request,"confirm_password.html",con)
            else:
                con={'email':email,
                     'emsg':'Invalid OTP'}
                return render(request,"confirm_password.html",con)
        except:
            con={'email':email,
             'emsg':'user not found'}
            return render(request,"confirm_password.html",con)
              
    return render(request,"confirm_password.html")     

#===============================================================    




def forget(request):
    if request.POST:
        email=request.POST['email']
        otp=random.randint(1000,9999)
        try:
            uid=User.objects.get(email=email)
        
            uid.otp=otp
            uid.save()
            send_mail("django",f"your otp is - {otp}",'gohiljayb10@gmail.com',[email])
            contaxt={
                "email":email
            }
            return render(request,"confirm_password.html",contaxt)
        except:
            print("Invalid Email")       
            return render(request,"forget.html")    
    return render(request,"forget.html")



        
#===============================================================
# def register(request):
#     if request.POST:
#         name=request.POST['name']
#         email=request.POST['email']
#         password=request.POST['password']
#         c_password=request.POST['c_password']
        
#         try:
#             uid=User.objects.get(email=email)
#             if uid.email==email:
#                 con={"e_msg":"This Email ID is Already Login Add Another Email"}
#                 return render(request,"register.html",con)
#         except:
#             if password==c_password:
#                 User.objects.create(name=name,email=email,password=password)
#                 return render(request,"login.html")
#             else:
#                 return render(request,"register.html")
            
#     else:
#         return render(request,"register.html")
    
def register(request):

    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        c_password=request.POST['c_password']
        
        try:
            uid=User.objects.get(email=email)
            if uid.email==email:
                con={"e_msg":"This Email ID is Already Login Add Another Email"}
                return render(request,"register.html",con)
        except:
            if password==c_password:
                User.objects.create(name=name,email=email,password=password)
                
                return render(request,"login.html")
            else:
                con={'e_msg': "Passwords do not match",}
                return render(request,"register.html",con)
            
    else:
        return render(request,"register.html")    

def contact(request):
    uid = User.objects.get(email=request.session['email'])
    count=addcart.objects.filter(user=uid).count()
    w_count=Add_Whishlist.objects.filter(user_id=uid).count()
    
    if request.POST:
        name=request.POST['name']
                
        email=request.POST['email']  
              
        message=request.POST['message']  
        
        Contact.objects.create(name=name,email=email,message=message) 
    con={"count":count,
         "uid":uid,"w_count":w_count}
    return render(request,"contact.html",con)        

                

def Whishlist(request):
    uid=User.objects.get(email=request.session['email'])
    w_count=Add_Whishlist.objects.filter(user_id=uid).count()
    count = addcart.objects.filter(user=uid).count()
    
    whish=Add_Whishlist.objects.filter(user_id=uid)
    con={"uid":uid,"whish":whish,"w_count":w_count,"count":count}
    return render(request,"whishlist.html",con)



# def add_whishlist(request,id):
#     uid=User.objects.get(email=request.session['email'])
#     pp=product.objects.get(id=id)
#     w_id=Add_Whishlist.objects.filter(product_id=pp,user_id=uid).exists()
    
#     if w_id:
        
#         w_id=Add_Whishlist.objects.filter(product_id=pp,user_id=uid).exists()
#         w_id.delete()
#         messages.info(request,"Item Remove From Your WhishList")
        
#         return redirect("shop")
#     else:
#         Add_Whishlist.objects.create(user_id=uid,
#                                      product_id=pp,
#                                      price=pp.price,
#                                      name=pp.name,
#                                      image=pp.img,)
#         messages.info(request,"Item Saved In Your WhishList")
        
#         return redirect("shop")
  
  
  

def add_whishlist(request, id):
    uid = User.objects.get(email=request.session['email'])
    pp = product.objects.get(id=id)
    w_id = Add_Whishlist.objects.filter(product_id=pp, user_id=uid).first()
    
    if w_id:
        w_id.delete()
        messages.info(request, "Item Removed From Your Wishlist")
    else:
        Add_Whishlist.objects.create(
            user_id=uid,
            product_id=pp,
            price=pp.price,
            name=pp.name,
            image=pp.img,)
        messages.info(request, "Item Saved In Your Wishlist")
        
    return redirect("shop")



def remove_whishlist(request, id):
    
    
    c=Add_Whishlist.objects.get(id=id)
    c.delete()
    return redirect('Whishlist')


