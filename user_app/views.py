import uuid, secrets, random
from pyexpat.errors import messages
import subprocess
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.models import User
from .models import Person, ValidRoom, History
from django.forms.models import inlineformset_factory
#from MailNotification.MailHandler import MailHandler
from .forms import RegistrationForm, AppointCall
from django.views.generic.list import ListView
from faker import Faker


# Create your views here.

class CallList(ListView):
    model = ValidRoom
    template_name = "loged_in_base.html"

    def get_queryset(self):
        person = Person.objects.filter(user_id__exact=self.request.user.id)
        calls = ValidRoom.objects.filter(caller1__iexact=person[0].number)
        lista = ValidRoom.objects.filter(caller2__iexact=person[0].number)
        c = []
        for e in lista:
            c.append(e)
        for e in calls:
            c.append(e)

        return c


@login_required(login_url='/login/')
def call(request):
    return redirect('http://webchat.com:3000')


def base(request):
    print(request.user.id)
    if request.user.is_authenticated:
        return render(request, 'loged_in_base.html')
    return render(request, 'base.html')


@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


@login_required(login_url='/login/')
def video(request):
    if request.method == 'POST':
        faker = Faker()
        form = AppointCall(request.POST)
        print(form.data)
        print(form.is_valid())
        if form.is_valid():
            room = ValidRoom()
            room.room_uuid = uuid.uuid4()
            room.caller1 = Person.objects.filter(user_id__exact=request.user.id)[0].number
            room.caller2 = request.POST.get('caller2')
            room.validation_username = faker.first_name()+faker.last_name()+str(random.randint(0, 1000))
            room.validation_token = secrets.token_urlsafe(32)
            subprocess.run(['turnadmin', '-a', '-u' + room.validation_username.strip(), '-r', 'default', '-p' + room.validation_token.strip()])
            room.save()

            history_record = History()
            history_record.caller1 = room.caller1
            history_record.caller2 = room.caller2
            history_record.save()
    else:
        form = AppointCall()
    return render(request, 'loged_in_call.html', {
        'form' : form
    })


@login_required(login_url='/login/')
def edit_user(request,pk):
    user = User.objects.get(pk=pk)
    user_form = RegistrationForm(instance=user)
    ProfileInlineFormset = inlineformset_factory(User, Person, fields='number')
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = RegistrationForm(request.POST, instance=user)
            formset = ProfileInlineFormset(request.POST, instance=user)
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/')
        return render(request, "account/account_update.html", {
            "noodle": pk,
            "noolde_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionError


def register(request):
    # mh = MailHandler(587, 'smtp.gmail.com', 'noreply.PSN.Checker@gmail.com', 'Psn12345')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            print(username)
            print(user.email)
            # mh.sendInvitation(username, user.email)
            login(request, user)
            return render(request, 'loged_in_base.html')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)


