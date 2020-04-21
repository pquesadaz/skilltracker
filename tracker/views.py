from django.shortcuts import render
from django.http import HttpResponse, request
from tracker.models import Users, Skills, SkillMap
from tracker.forms import NewUserForm, EditUserForm, NewSkillForm, EditSkillForm, EditSkillProfile
import csv, xlwt


def index(request):

    skills_list = Skills.objects.all()
    users_list = Users.objects.all()
    print(skills_list)
    print(users_list)
    for user in users_list:
        print(user.user_name)
        print(user.user_email)

    user = Users.objects.filter(user_email='user01@mydomain.com').count()
    print(user)

    my_data = {
        'variable': 'This is the value of my variable',
        'skills': skills_list,
    }

    return render(request, 'tracker/index.html', context=my_data)


def newuser(request):

    form = NewUserForm()

    data = {
        'form': form,
    }

    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            form.save()
            batch = []
            user_id = Users.objects.latest('user_id')

            for skill in Skills.objects.all():
                batch.append(SkillMap(skillmap_user_id=user_id, skillmap_skill_id_id=skill.skill_id, skillmap_level=1))
            SkillMap.objects.bulk_create(batch)

            data['message'] = 'User added successfully!'
        else:
            data['message'] = 'Error found during process. Make sure this email is unique and does not exist already in the database.'

    return render(request, 'tracker/newuser.html', context=data)


def users(request):

    if 'id' in request.GET:

        form = EditUserForm()

        user = Users.objects.filter(user_id=request.GET['id'])[0]

        form.initial = {
            'user_name': user.user_name,
            'user_email': user.user_email,
            'user_date_created': user.user_date_created
        }

        data = {
            'form': form,
        }

    else:

        users = Users.objects.all()

        data = {
            'users': users,
        }

    if request.method == "POST":

        form = EditUserForm(request.POST or None, instance=user)

        if form.is_valid():
            user = form.save(commit=True)
            data['message'] = 'User information updated!'
            user = Users.objects.filter(user_id=request.GET['id'])[0]

        else:
            data['message'] = 'Error found during process.'

        data['form'] = form

    return render(request, 'tracker/user.html', context=data)


def newskill(request):

    form = NewSkillForm()

    data = {
        'form': form,
    }

    if request.method == "POST":

        form = NewSkillForm(request.POST)
        if form.is_valid():
            form.save()
            batch = []
            skill_id = Skills.objects.latest('skill_id')
            print(skill_id)

            for user in Users.objects.all():
                print(user.user_id)
                batch.append(SkillMap(skillmap_user_id_id = user.user_id, skillmap_skill_id = skill_id, skillmap_level = 1))

            SkillMap.objects.bulk_create(batch)

            data['message'] = 'Skill added successfully!'
        else:
            data['message'] = 'Error found during process.'

    return render(request, 'tracker/newskill.html', context=data)


def skills(request):

    data = {}

    if 'id' in request.GET:

        form = EditSkillForm()
        skill = Skills.objects.filter(skill_id=request.GET['id'])[0]

        form.initial = {
            'skill_name': skill.skill_name,
            'skill_description': skill.skill_description,
            'skill_date_created': skill.skill_date_created,
        }

        data['form'] = form

    else:

        skills = Skills.objects.all()

        data = {
            'skills': skills,
        }



    if request.method == "POST":

        form = EditSkillForm(request.POST or None, instance=skill)

        if form.is_valid():
            skill = form.save(commit=True)
            data['message'] = 'Skill information updated!'
            skill = Skills.objects.filter(skill_id=request.GET['id'])[0]

        else:
            data['message'] = 'Error found during process.'

        data['form'] = form

    return render(request, 'tracker/skill.html', context=data)


def profile(request):

    form = EditSkillProfile()
    data = {}

    skills = Skills.objects.all()
    user = Users.objects.filter(user_id=request.GET['id'])[0]


    if 'id' in request.GET:
        # print(request.GET['id'])
        user = Users.objects.filter(user_id=request.GET['id'])[0]
        profile = SkillMap.objects.filter(skillmap_user_id=request.GET['id'])
        skills = Skills.objects.all()

        data['user'] = user
        data['user_name'] = user.user_name
        data['profile'] = profile
        data['skills'] = skills
        data['user_id'] = user.user_id

        level_perc = {
            '1': '0%',
            '2': '25%',
            '3': '50%',
            '4': '75%',
            '5': '100%',
        }
        data['level_perc'] = level_perc

        if 'action' in request.GET and request.GET['action'] == 'edit':
            data['action'] = "edit";

    if request.method == "POST":

        for skill in skills:

            skill_key = 'skill_' + str(skill.skill_id)
            entry, created = SkillMap.objects.get_or_create(skillmap_user_id_id = user.user_id, skillmap_skill_id_id = skill.skill_id)
            entry.skillmap_level = request.POST[skill_key]

            try:
                entry.save()
                data['message'] = 'Profile updated successfully!'
            except Exception as e:
                data['message'] = 'Error found during processing!'
                print(e)

    data['form'] = form

    return render(request, 'tracker/profile.html', context=data)


def download_users_csv(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook('users.xlsx')
    ws = wb.add_sheet('dict_data')

    bold_font_style = xlwt.easyxf('border: left thin, top thin, bottom thin, right thin; font: bold 1')
    normal_style = xlwt.easyxf('border: left thin, top thin, bottom thin, right thin;')

    ws.write(0, 0, 'Name', style=bold_font_style)
    ws.write(0, 1, 'Email', style=bold_font_style)

    users = Users.objects.all()

    col = 0
    row = 1
    for user in users:
        ws.write(row,0,user.user_name, style=normal_style)
        ws.write(row,1,user.user_email, style=normal_style)
        row += 1

    wb.save(response)

    return response
