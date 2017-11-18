from django.shortcuts import render, render_to_response, redirect
from website.util import doubleknot
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse
from website.models import CourseReference
from datetime import datetime
from website.forms import ImportForm, ReviewUploadForm

# Create your views here.

def course_catalog(request):
    year = datetime.now().year
    course_catalog = CourseReference.objects.all().filter(year=year)
    response = None
    if len(course_catalog) > 0:
        response = render(request, 'course_catalog.html', 
            {'course_catalog' : course_catalog})
    else:
        response = render(request, 'course_catalog.html')

    return response



    
def edit_course_catalog(request):
    def add_course():
        year = datetime.now().year
        course_reference = CourseReference()
        course_reference.name = request.POST['course']
        course_reference.period = request.POST['course-period']
        course_reference.year = year
        course_reference.save()

    def save_edited_course_catalog():
        year = datetime.now().year
        course_catalog = CourseReference.objects.all().filter(year=year)
        for course in course_catalog:
            edited_name = request.POST['n' + str(course.id)]
            edited_period = request.POST['p' + str(course.id)]
            course.name = edited_name
            course.period = edited_period
            course.save()

    response = None
    if request.method == 'POST':
        if 'add' in request.POST:
            # TODO keep the courses in the session until the user hits save
            add_course()
            response = redirect('edit_course_catalog')
        if 'save-edit' in request.POST:
            save_edited_course_catalog()
            response = redirect('course_catalog')
    else:
        year = datetime.now().year
        course_catalog = CourseReference.objects.all().filter(year=year)
        if len(course_catalog) > 0:
            response = render(request, 'edit_course_catalog.html', 
                {'course_catalog' : course_catalog})
        else:
            print('HERE')
            response = render(request, 'edit_course_catalog.html')
            print(response)
    return response

def import_course_catalog(request):
    response = None

    if request.method == 'POST':
        if 'doubleknot_roster' in request.FILES:
            doubleknot_roster = request.FILES['doubleknot_roster']
            courses = doubleknot.get_courses(doubleknot_roster.read())
            request.session['courses'] = courses

            response = redirect('review_course_catalog')
        else:
            form = ImportForm(request.POST)
            response = render(request, 'import_courses.html', {'form' : form, 
                'error_message' : 'Please select a file.'}) 
    else:
        form = ImportForm()
        response = render(request, 'import_courses.html', {'form' : form})

    return response

def review_course_catalog(request):
    def save_course_catalog(request):
        year = datetime.now().year
        CourseReference.objects.filter(year=year).delete()
        print(request.POST.getlist('courses'))
        if 'courses' in request.POST:
            selected_courses = request.POST.getlist('courses')
            print(selected_courses)
            for course in selected_courses:
                print(course)
                course_parts = course.split(': ')
                course_reference = CourseReference(name=course_parts[0], 
                    period=course_parts[1], year=datetime.now().year)
                course_reference.save()
      
    response = None
    if request.method == 'POST':
        save_course_catalog(request)
        response = redirect('course_catalog')
    else:
        if 'courses' in request.session:
            courses = request.session['courses'] 
            display_courses = []
            for course in courses:
                display_name = course['name'] + ': ' + course['period']
                display_courses.append((display_name, display_name))
            form = ReviewUploadForm(course_choices=tuple(display_courses))
            year = datetime.now().year
            course_catalog = CourseReference.objects.all().filter(year=year)
            if len(course_catalog) == 0:
                response = render(request, 'review_upload.html', 
                    {'form' : form })
            else:
                # warn the user that their current course catalog will 
                # be replaced.
                warning_message = ('The existing course catalog will be ' 
                    'replaced if these selections are saved.')
                response = render(request, 'review_upload.html', 
                    {'form' : form, 'warning_message' : warning_message})
        else:
            # error message telling the user to choose a file.
            response = redirect('import_course_catalog')

    return response

"""def view_course_catalog(request):
    year = datetime.now().year
    course_catalog = CourseReference.objects.all().filter(year=year)
    response = None

    if len(course_catalog) > 0:
        response = render(request, 'course_catalog.html', 
            {'course_catalog' : course_catalog})
    else:
        response = render(request, 'course_catalog.html')

    return response

def import_course_catalog(request):
    form = ImportForm()
    response = render(request, 'import_courses.html', {'form' : form})

    return response

def edit_course_catalog(request):
    pass

def review_course_catalog(request):
    if 'doubleknot_roster' in request.FILES:
        doubleknot_roster = request.FILES['doubleknot_roster']
        courses = doubleknot.get_courses(doubleknot_roster.read())
        display_courses = []
        for course in courses:
            display_name = course['name'] + ': ' + course['period']
            display_courses.append((display_name, display_name))
        form = ImportForm(display_courses)
        year = datetime.now().year
        course_catalog = CourseReference.objects.all().filter(year=year)
        if len(course_catalog) == 0:
            response = render(request, 'import_courses.html', 
                {'form' : form })
        else:
            # warn the user that their current course catalog will 
            # be replaced.
            warning_message = ('The existing course catalog will be ' 
                              'replaced if these selections are saved.')
            response = render(request, 'import_courses.html', 
                        {'form' : form, 'warning_message' : warning_message})
    else:
        # error message telling the user to choose a file.
        form = ImportForm()
        error_message = "Please choose a Doubleknot roster to upload."
        response = render(request, 'import_courses.html', 
                    {'form' : form, 'error_message' : error_message})

    return response

def save_course_catalog(request):
    year = datetime.now().year
    CourseReference.objects.filter(year=year).delete()
    print(request.POST.getlist('courses'))
    if 'courses' in request.POST:
        selected_courses = request.POST.getlist('courses')
        print(selected_courses)
        for course in selected_courses:
            print(course)
            course_parts = course.split(': ')
            course_reference = CourseReference(name=course_parts[0], 
                period=course_parts[1], year=datetime.now().year)
            course_reference.save()
    response = view_course_catalog()

    return response
"""

def create_paperwork(request):
    response = None
    if request.method == 'POST':
        if 'doubleknot_roster' in request.FILES:
            doubleknot_roster = request.FILES['doubleknot_roster']
            doubleknot.create_courses(doubleknot_roster.read())
    else:
        response = render(request, 'create_paperwork.html')

    return response

def scouts(request):
    return HttpResponse(request.POST['HTTP_REFERER'])

def instructors(request):
    return HttpResponse('INSTRUCTORS')

def pending_requests(request):
    pass

def home(request):
    pass

def course_overview(request):
    pass

def course_home(request):
    pass

def course_attendence(request):
    pass

def course_requirements_signoff_checklist(request):
    pass

def course_requirements_signoff_scouts(request):
    pass

def scout_course_overview(request):
    pass

