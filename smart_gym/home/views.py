from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import os, json


BASE_DIR = os.getcwd()

runcmd = True

def home(request):
    return render(request, 'control.html')


def newuser(request, profession, name):
    print("DIRECTORY", BASE_DIR)
    if request.method == 'POST':
            command = 'python {}/home/facerecognition/main.py --mode "input" --profession "{}" --name "{}"'.format(BASE_DIR, BASE_DIR, profession, name)
            os.system('open -a Terminal ' + command)

            return HttpResponse("")
    else:
        return render(request, 'adduser.html', {'profession': profession, 'name': name})


def list(request):
    f = json.loads(open('{}/home/facerecognition/facerec_128D.txt'.format(BASE_DIR), 'r').read())
    users = {}
    for name, value in f.items():
        profession = value[0]
        users[name] = profession

    print(users)
    return render(request, 'users.html', {'user_list': json.dumps(users)})

