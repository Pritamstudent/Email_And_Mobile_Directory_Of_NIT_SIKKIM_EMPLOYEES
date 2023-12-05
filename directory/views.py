from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib import messages
from .models import LoginTable, TeacherModel
from django.conf import settings

from django.contrib.auth.decorators import login_required
def LoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('username')
        pswd = request.POST.get('password')
        try:
            check = LoginTable.objects.get(username=loginid, password=pswd)
            request.session['username'] = check.username
            if check.username != None or check.username != '':
                return render(request, 'apphome.html', {})
            else:
                messages.success(request, 'invalid Credential')
                return render(request, 'index.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')

    return render(request, 'index.html', {})


def apphome(request):
    return render(request, 'apphome.html', {})


def importedForm(request):
    return render(request, 'importerform.html', {})


def checkData():
    # plen = len(Profilepicture)
    import os
    # pic = 'default.JPG'
    li = []
    # dir_file = os.listdir()
    for x in os.listdir(settings.MEDIA_ROOT + "\\" + "profilepic"):
        if x.endswith(".JPG") or x.endswith(".jpg"):
            li.append(x)
    return li


def importBulk(request):
    TeacherModel.objects.all().delete()
    path = settings.MEDIA_ROOT + "\\" + "Teachers.csv"
    import pandas as pd
    df = pd.read_csv(path, encoding='utf-8')
    li = checkData()
    print(li)
    print()
    for i in df.index:
        FirstName = df['First Name'][i]
        LastName = df['Last Name'][i]
        Profilepicture = df['Profile picture'][i]
        EmailAddress = df['Email Address'][i]
        PhoneNumber = df['Phone Number'][i]
        RoomNumber = df['Room Number'][i]
        Subjectstaught = df['Subjects taught'][i]

        pic = 'default.jpg'
        if Profilepicture not in li:
            Profilepicture = pic

        # l2 = len(FirstName)
        sub = Subjectstaught.split(',')
        sub = len(sub)
        if sub <= 5:
            TeacherModel.objects.create(FirstName=FirstName, LastName=LastName, Profilepicture=Profilepicture,
                                        EmailAddress=EmailAddress, PhoneNumber=PhoneNumber, RoomNumber=RoomNumber,
                                        Subjectstaught=Subjectstaught)
        print('First Name', Profilepicture)

    messages.success(request, 'Data Imported')
    return render(request, 'importerform.html', {})


def DataView(request):
    qs = TeacherModel.objects.all()
    return render(request, 'AllData.html', {'data': qs})

def DeleteTeacher(request, id):
    try:
        teacher = TeacherModel.objects.get(id=id)
        if request.method == 'POST':
            teacher.delete()
            messages.success(request, f'Record for {teacher.FirstName} {teacher.LastName} has been deleted.')
            return redirect('apphome')
        return render(request, 'delete_confirmation.html', {'teacher': teacher})
    except TeacherModel.DoesNotExist:
        messages.error(request, 'Record not found.')
        return redirect('apphome')

def TeacherDirectoryForm(request):
    return render(request, 'FilterForm.html', {})


def FilterTeacherProfile(request):
    from django.db.models import Q
    if request.method == 'POST':
        filtertxt = request.POST.get('filtertext')
        data = TeacherModel.objects.filter(Q(FirstName__icontains=filtertxt) | Q(LastName__icontains=filtertxt))
        return render(request, 'FilterForm.html', {'data': data})



def GetProfilePage(request):
    if request.method == 'GET':
        id = int(request.GET.get('uid'))
        data = TeacherModel.objects.get(id=id)
        return render(request, 'ProfilePage.html', {'data': data})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TeacherModelForm  # Import your TeacherModelForm

def AddTeacherData(request):
    if request.method == 'POST':
        form = TeacherModelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher profile added successfully.')
            return redirect('DataView')
        else:
            messages.error(request, 'Error in the form submission. Please check the data and try again.')

    else:
        form = TeacherModelForm()

    return render(request, 'AddTeacherData.html', {'form': form})

'''
def AddTeacherData(request):
    if request.method == 'GET':
        return render(request, 'AddTeacherData.html', {})
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        roomnumber = request.POST.get('roomnumber')
        subjects = request.POST.get('subjects')
        TeacherModel.objects.create(FirstName=firstName, LastName=lastName, Profilepicture='default.jpg',
                                    EmailAddress=email, PhoneNumber=mobile, RoomNumber=roomnumber,
                                    Subjectstaught=subjects)
        qs = TeacherModel.objects.all()
        return render(request, 'AllData.html', {'data': qs})
  

        '''



  
def get_profile(request, id):
    try:
        teacher = TeacherModel.objects.get(id=id)
        return render(request, 'loginProfilePage.html', {'data': teacher})
    except TeacherModel.DoesNotExist:
        # Handle the case when the teacher is not found, you can redirect or show an error message
        messages.error(request, 'Teacher not found.')
        return redirect('apphome')
       
def EditTeacher(request, id):
    teacher = get_object_or_404(TeacherModel, id=id)

    if request.method == 'POST':
        form_data = request.POST
        # Validate the form data and handle any errors

        # Update the teacher's information
        teacher.FirstName = form_data['firstName']
        teacher.LastName = form_data['lastName']
        teacher.EmailAddress = form_data['email']
        teacher.PhoneNumber = form_data['mobile']
        teacher.RoomNumber = form_data['roomnumber']
        teacher.Subjectstaught = form_data['subjects']

        # Check if a new image has been provided
        if 'profilepicture' in request.FILES:
            teacher.Profilepicture = request.FILES['profilepicture']

        teacher.save()
        qs = TeacherModel.objects.all()
        return render(request, 'AllData.html', {'data': qs})  # Redirect to the teacher directory page after updating

    return render(request, 'update_teacher.html', {'teacher': teacher})