from django.shortcuts import render, HttpResponse, redirect
import requests
# from time import gmtime, strftime
from datetime import datetime
from .models import users, quotes
from django.contrib import messages
import bcrypt

def index(request):
    if 'initial' in request.session: #allows me to do things on initialization
        request.session['initial'] = False
        if request.session['user_id'] != -1: #user is here
            messages.error(request,'you are logged in')
            return redirect('/users/'+str(request.session['user_id'])) #keeps them logged in
        #print(request.session)
    else:
        request.session['initial'] = True #initialize default values for session to avoid checking if they are in later
        request.session['user_id'] = -1 #on login makes a different user id
        request.session['create'] = False #turns true on successful registration
    return render(request, "django_app/code.html")

def login_page(request):
    if 'initial' in request.session: #reinitializes on login redirect. clearing the cookie will end up here again
        request.session['initial'] = False
        if request.session['user_id'] != -1: #user is here
            messages.error(request,'you are logged in')
            return redirect('/users/'+str(request.session['user_id'])) #keeps them logged in
        #print(request.session)
    else:
        request.session['initial'] = True #initialize default values for session to avoid checking if they are in later
        request.session['user_id'] = -1 #on login makes a different user id
        request.session['create'] = False #turns true on successful registration
    return render(request,"django_app/login.html")

def login(request):
    if request.method == 'POST':
        errors = users.objects.login_validator(request.POST)
        category = 0
        key_prev = 'j'
        if len(errors):
            for key,value in errors.items():
                if key_prev != key: #allows for multiple errors to display over one box
                    key_prev = key
                    category += 1               
                print(key,value,category)
                messages.set_level(request,category) #otherwise will ignore add message
                messages.add_message(request, category, value)    
            print('ERROR::',errors)
            return redirect('/users/login_page')
        else: #no errors passed credentials true
            userID = users.objects.get(email = request.POST['email']).id
            request.session['user_id'] = userID
            return redirect("/users/"+str(userID))            
    else:
        return redirect('/users/login_page')
        
def create(request): #user registration
    if request.method == "POST":
        errors = users.objects.user_validator(request.POST)
        category=0
        key_prev = 'j'
        if len(errors):
            for key,value in errors.items():
                messages.set_level(request,category) #otherwise will ignore add message
                if key_prev != key: #allows for multiple errors to display over one box
                    key_prev = key
                    category += 1
                print(key,value,category)
                messages.add_message(request, category, value)    
            print('ERROR::',errors)
            return redirect('/')
        else: #create user
            hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = users.objects.create(fname = request.POST['first_name'], lname = request.POST['last_name'], email = request.POST['email'], pw_hash = hash_pw)
            user_id = user.id
            request.session['create'] = True
            request.session['user_id'] = user_id
            print('CREATED::', user)
            return redirect("/quotes")
    else:
        return redirect('/')

def show(request, id): #success page
    if request.session['user_id'] != -1: #user is here
        this_user = users.objects.get(id = str(id))
        print('SHOW::',this_user)
        context = {'ID' : this_user.id,
                    'full_name' : (this_user.fname + ' ' + this_user.lname),
                    'email' : this_user.email,
                    'created_at' : this_user.created_at,
                    'quotes' : this_user.quotes.all() 
                   }
        request.session['first_name'] = this_user.fname
        return render(request,"django_app/user.html", context)
    else: #user is not here
        messages.add_message(request, 0, 'you must log in')
        return redirect('/users/login_page')

def edit_page(request, id): #edit page
    if request.session['user_id'] != -1: #user is here
        this_user = users.objects.get(id = str(id))
        print('SHOW::',this_user)
        context = {'ID' : this_user.id,
                    'first_name' : this_user.fname,
                    'last_name' : this_user.lname,
                    'email' : this_user.email,
                    'created_at' : this_user.created_at}
        request.session['first_name'] = this_user.fname
        return render(request,"django_app/user_edit.html", context)
    else: #user is not here
        messages.add_message(request, 0, 'you must log in')
        return redirect('/users/login_page')

def edit_user(request):
    if request.session['user_id'] != -1:
        user_id = request.session['user_id']
    else:
        messages.add_message(request, 0, 'you must log in')
        return redirect('/users/login_page')
    if request.method == "POST":
        errors = users.objects.edit_validator(request.POST)
        category=0
        key_prev = 'j'
        if len(errors):
            for key,value in errors.items():
                messages.set_level(request,category) #otherwise will ignore add message
                if key_prev != key: #allows for multiple errors to display over one box
                    key_prev = key
                    category += 1
                print(key,value,category)
                messages.add_message(request, category, value)    
            print('ERROR::',errors)
            return redirect("/users/"+str(user_id)+'/edit')
        else: #update user
            this_user = users.objects.get(id = str(user_id))
            this_user.fname = request.POST['first_name']
            this_user.lname = request.POST['last_name']
            this_user.email = request.POST['email']
            this_user.save() #put into DB
            return redirect("/users/"+str(user_id))
    else:
        return redirect('/')

def dashboard(request):
    if request.session['user_id'] != -1:
        user_id = request.session['user_id']
    else:
        messages.add_message(request, 0, 'you must log in')
        return redirect('/users/login_page')
    context = {
        'allquotes' : quotes.objects.all(),
        'user' : users.objects.get(id = str(user_id))
    }
    return render(request, "django_app/quote_dashboard.html", context)

def addquote(request,user_id):
    if request.method == "POST":
        errors = quotes.objects.quote_validator(request.POST)
        category=0
        key_prev = 'j'
        if len(errors):
            for key,value in errors.items():
                messages.set_level(request,category) #otherwise will ignore add message
                if key_prev != key: #allows for multiple errors to display over one box
                    key_prev = key
                    category += 1
                print(key,value,category)
                messages.add_message(request, category, value)
            print('ERROR::',errors)
            return redirect('/quotes')
        else: #create quote
            poster = users.objects.get(id = user_id)
            print(poster)
            this_quote = quotes.objects.create(quotee = request.POST['quotee'], quote = request.POST['quote'], poster = poster) #poster likes his own posts automatically
            return redirect('/quotes')
    else:
        return redirect('/quotes')

def delquote(request,quote_id):
    if request.method == 'POST':
        kill_quote = quotes.objects.get(id = quote_id)
        kill_quote.delete()
        return redirect('/quotes')
    else:
        return redirect('/quotes')

def like(request,user_id,quote_id):
    if request.method == 'POST':
        this_user = users.objects.get(id = user_id)
        print('USER::', this_user)
        this_quote = quotes.objects.get(id = quote_id)
        print('QUOTE::', this_quote)
        if len(this_user.likes.filter(id = quote_id))> 0:
            #user has liked this post already
            return redirect('/quotes')
        else:
            #add the post to likes
            print('BEFORE::',this_quote.users_liked)
            this_quote.users_liked.add(this_user)
            print('AFTER::',this_quote.users_liked)
            #redirect to quote poster page
            return redirect('/users/'+str(this_quote.poster.id))
        return redirect('/quotes')
    else:
        return redirect('/quotes')
# This page will render the coin page
def coin(request):
    # API endpoint
    URL = "https://api.coinmarketcap.com/v2/ticker/1"
    URL2 = "https://graphs2.coinmarketcap.com/currencies/bitcoin/"
    # Create GET request to API
    response2 = requests.get(URL2)
    response = requests.get(URL)
    # Translate to JSON
    data = response.json()
    mark = response2.json()
    # Storing date and price into variables
    datePrice = []
    for i in range(10,20):
        time = datetime.fromtimestamp(int((mark['price_usd'][i][0])/1000)).strftime('%Y-%m-%d')
        price = mark['price_usd'][i][1]
        datePrice.append({'time': time,'price': price})
        context = {
                "pric": datePrice
        }
    # pass data through return
    print (datePrice[0]['price'])
    return render(request, "django_app/coin_page.html", context)

def logout(request):
    request.session.clear()
    return redirect('/users')

# def destroy(request, id):
#     this_user = users.objects.get(id = str(id))
#     print('DESTROY::',this_user)
#     this_user.delete()
#     return redirect('/users')

# def update(request,id):
#     if request.method == "POST":
#         errors = users.objects.basic_validator(request.POST)
#         if len(errors):
#             for error in errors:
#                 messages.add_message(request, messages.INFO, error)
#         else:
#             this_user = users.objects.get(id = str(id))
#             this_user.fname = request.POST['first_name']
#             this_user.lname = request.POST['last_name']
#             this_user.email = request.POST['email']
#         return redirect(("/users/"+id))
#     else:
#         return redirect(("/users/"+id))
