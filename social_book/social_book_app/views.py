from django.contrib.auth.hashers import make_password
from social_book_app.models import CustomUser,UploadedFile,fetch_data
from django.views import View
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from social_book_app.forms import UploadFileForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from social_book_app.filter import AuthnSellFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token as AuthToken
from .serializer import UploadedFileSerializer
from djoser.utils import login_user
from .serializer import LoginSerializer
from django.contrib.auth import authenticate, login as django_login
from rest_framework.authtoken.models import Token
from .token import TokenAuthentication




class Register(View):
    
    def get(self,request):
        return render(request,'register.html')
    
    def post(self,request):
        postData=request.POST
        username=postData.get('username')
        email=postData.get('email')
        password=postData.get('password')
        public_visiblity = postData.get('public_visiblity') == 'on'
        
        value={
            'username':username,
            'email':email,
            'password':password,
            'public_visiblity':public_visiblity
          }
        error_message=None
        customer=CustomUser(username=username,email=email,password=password,public_visiblity=public_visiblity)
        error_message=self.validateCustomer(customer)
        
        if not error_message:
          print(username,email,password)
          customer.password=make_password(customer.password)
          customer.register()
          send_mail(
            'Welcome to MyDesk',
            'Thankyou for Registering with MyDesk.',
            'darshanbarde805@gmail.com',
            [customer.email],
            fail_silently=False,
        )
          return redirect('login')
        else:
          data={
                'error':error_message,
                'values':value
             }  
        return render(request,'register.html',data)
    
    def validateCustomer(self,customer):
      error_message=None;
      if(not customer.username):
            error_message="username name is Required"
      elif len(customer.password)<4:
            error_message="password must be 4 char long"
      elif len(customer.email)<5:
            error_message="email must be 5 char long"
      elif customer.isExists():
            error_message="email addresss already registered..!"
      return error_message
    

class Login(View):
    return_url=None
    def get(self,request):
          Login.return_url=request.GET.get('return_url')
          return render(request,'login.html')
    
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        customer = CustomUser.get_customer_by_username(username)
        error_message=None
        if customer:
            flag=check_password(password,customer.password)
            if flag:
                request.session['username'] = username  # Store the username in the session
                request.session['customer']=customer.id
                #return redirect('mybook')
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url=None
                    return redirect('mybook')
            else:
                 error_message="Username or Password Invalid!!!"
        else:
            error_message='Username or passsword Invalid!!!'

        print(username,password)
        return render(request,'login.html',{'error':error_message})
    

def logout(request):
        request.session.clear()
        return redirect('login')


class Home(View):

    def get(self, request):
        form = UploadFileForm()
        files = UploadedFile.objects.all()  # Get all uploaded files
        return render(request, 'home.html', {'form': form, 'files': files})
    
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)  # Don't save yet
            customer_id = request.session.get('customer')
            customer = CustomUser.objects.get(id=customer_id)
            uploaded_file.uploaded_by = customer  # Assign the CustomUser instance to uploaded_by
            uploaded_file.save()  # Now save the file
            messages.success(request, 'File uploaded successfully!')  # Add a success message
            return redirect('mybook')
        return render(request, 'mybook.html', {'form': form})


def uploaded_files(request):
    files = UploadedFile.objects.filter.all()
    if files.exists():
        return render(request, 'home.html', {'files': files})
    else:
        return redirect('home')
    
def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['redirect_from_my_books'] = True
        return context

def authors_and_sellers(request):
    users = CustomUser.objects.all()
    filter = AuthnSellFilter(request.GET, queryset=users)
    return render(request, 'authnsell.html', {'filter': filter})

class MyBooksView(View):
    def get(self, request):
        customer_id = request.session.get('customer')
        customer = CustomUser.objects.get(id=customer_id)
        files = UploadedFile.objects.filter(uploaded_by=customer)
        if files.exists():
            return render(request, 'mybook.html', {'files': files})
        else:
            return redirect('home')
        
class MyView(APIView):
    def get(self, request):
        data = fetch_data()
        return Response(data)
    


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(username=serializer.validated_data['username'])
        django_login(request, user)
        token, created = AuthToken.objects.get_or_create(user=user)
        return Response({'token': token.key})

        

#class FileAPI(APIView):
    #def get(self, request):
        token = request.headers.get('Authorization')
        if token:
            token_obj = Token.objects.filter(key=token).first()
            if token_obj:
                user = token_obj.user
                # Get the files uploaded by the user
                files = user.files.all()
                file_list = []
                for file in files:
                    file_list.append({
                        'filename': file.file.name,
                        'url': file.file.url
                    })
                return Response(file_list)
            else:
                return Response({'error': 'Invalid token'}, status=401)
        else:
            return Response({'error': 'Token not provided'}, status=401)
        

class FileAPI(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        files = UploadedFile.objects.filter(uploaded_by=user)
        file_list = [{'id': file.id, 'title': file.title} for file in files]
        return Response(file_list)