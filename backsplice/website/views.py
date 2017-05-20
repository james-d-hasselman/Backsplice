from django.shortcuts import render, render_to_response
from website.util import doubleknot
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse
from website.models import CourseReference
from datetime import datetime
from website.forms import ImportForm

# Create your views here.

def course_catalog(request):
    def view_course_catalog():
        year = datetime.now().year
        course_catalog = CourseReference.objects.all().filter(year=year)
        response = None
        if len(course_catalog) > 0:
            response = render(request, 'course_catalog.html', 
                {'course_catalog' : course_catalog})
        else:
            response = render(request, 'course_catalog.html')

        return response

    if request.method == 'POST':
        form = None
        if 'upload' in request.POST:
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
        elif 'save' in request.POST:
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
        elif 'import' in request.POST:
            form = ImportForm()
            response = render(request, 'import_courses.html', {'form' : form})
        elif 'edit' in request.POST:
            #TODO build the edit page.
            pass
        #TODO think about a separate 'Add' page just for adding new courses.
    else:
        response = view_course_catalog()

    return response

def create_paperwork(request):
    return render(request, 'create_paperwork.html')
    return HttpResponse('HOME')

def scouts(request):
    return HttpResponse('SCOUTS')

def instructors(request):
    return HttpResponse('INSTRUCTORS')

def pending_requests(request):
    pass

def home(request):
    pass
