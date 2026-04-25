from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ml.model import prediction
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from .models import History
from django.contrib.auth.models import User
from .services import ai_brain
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json
# Create your views here.


def launch_system(request):
    if request.user.is_authenticated:
        return redirect(reverse('home') + '#userPrompt')
    else:
        return redirect("/login/")


def home(request):
    # print('Method: ', request.method)

    content = {}
    records = []
    risk = ""
    if request.user.is_authenticated:
        records = History.objects.filter(user=request.user)

    content = {
        'user': request.user,
        'records': records,   # <-- include records here
    }

    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()

        if not user_input:
            messages.error(request, 'You must enter soemthing!!!')
            return render(request, 'home.html', content)
        try:
            data = ai_brain(user_input, 0)
            result = prediction(data['daily_study_hours'],
                                data['sleep_hours'],
                                data['attendance_percentage'],
                                data['screen_time'])

            final_data = ai_brain(user_input, result)

            pass_or_fail = 'Pass' if result >= 40 else 'Fail'

            if result >= 80:
                grade = 'A'
                risk = "Excellent (Stable performance)"
                risk_class = "text-green-500"
            elif result >= 60:
                grade = 'B'
                risk = "Low Risk (Good balance)"
                risk_class = "text-yellow-500"
            elif result >= 40:
                grade = 'C'
                risk = "Medium Risk (Needs improvement)"
                risk_class = "text-orange-500"
            else:
                grade = 'E'
                risk = "High Risk (Poor academic performance)"
                risk_class = "text-red-500"

            if request.user.is_authenticated:
                history_prediction = History(
                    user=request.user,
                    course=final_data['subject'],
                    study_hours=final_data['daily_study_hours'],
                    sleep_hours=final_data['sleep_hours'],
                    attendance_percentage=final_data['attendance_percentage'],
                    screen_time=final_data['screen_time'],
                    prediction=result,
                    grade=grade,
                    pass_or_fail=pass_or_fail,
                    zai_output=final_data,
                    risk=risk,
                    risk_class=risk_class
                )
                history_prediction.save()
                records = History.objects.filter(user=request.user)

            content = {
                'user': request.user,
                'attendance_percentage': final_data['attendance_percentage'],
                'subject': final_data['subject'],
                'sleep_hours': final_data['sleep_hours'],
                'daily_study_hours': final_data['daily_study_hours'],
                'screen_time': final_data['screen_time'],
                'result': result,
                'grade': grade,
                'pass_or_fail': pass_or_fail,
                'zai_output': final_data,
                'records': records,
                'risk': risk,
                'risk_class': risk_class
            }
            print(f'Your exam result is {result}')
        except Exception as e:
            print("ERROR:", e)
            messages.error(request, f"AI ERROR OCCURED {e}")

    else:
        content['records'] = records

    return render(request, 'home.html', content)


def login_forms(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Log In")
            return redirect('home')

        else:
            messages.error(
                request, "There Was An Error Logging In, Please Try Again...")
            return render(request, 'login.html')
    return render(request, 'login.html')


def logout_forms(request):
    logout(request)
    return redirect('home')


def register_form(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, "There Was An Error Registering, Please Try Again...")
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def view_record(request, pk):
    if request.user.is_authenticated:
        record = get_object_or_404(History, id=pk, user=request.user)

        zai_output = record.zai_output
        if isinstance(zai_output, str):
            try:
                zai_output = json.loads(zai_output)
            except Exception as e:
                print("JSON decode error:", e)
        context = {
            'result': record.prediction,
            'daily_study_hours': record.study_hours,
            'sleep_hours': record.sleep_hours,
            'attendance_percentage': record.attendance_percentage,
            'screen_time': record.screen_time,
            'zai_output': zai_output,
            'grade': record.grade,
            'pass_or_fail': record.pass_or_fail,
            'risk': record.risk,
            'risk_class': record.risk_class,
        }
        return render(request, 'record.html', context)
    else:
        return redirect('home')
