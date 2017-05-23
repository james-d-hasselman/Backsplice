import re
import pyexcel
import magic
from website.models import Course, Scout, CourseReference
import datetime

"""
Contains helper functions for working with Doubleknot rosters.
"""

# re to find the period
period_re = re.compile(r'\((?P<period>.*)\)[^$]')

# re to find the camp program
program_re = re.compile(r'^[^\(]*[^\s\(]')

# re to find the troop number
troop_re = re.compile(r'[0-9]{1,4}')

def _get_file_type(doubleknot_roster):
    """Takes a byte buffer representing a doubleknot roster and 
    gets its file format."""
    
    mime_type = magic.from_buffer(doubleknot_roster, mime=True)
    if mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return 'xlsx'
    elif mime_type == 'application/vnd.ms-excel':
        return 'xls'
    else:
        return 'ods'


def create_courses(doubleknot_roster):
    """Takes a byte buffer representing a doubleknot roster and 
    writes the courses and scouts to the Backsplice database.
    
    Supported formats are: .xls, .xlsx, and .ods"""

    # helper function to create a single course
    def create_course():
        # look for a course reference with the course name
        course_reference = CourseReference.objects.filter(name=course_name, 
            period=period, year=str(datetime.date.today().year))
        # if there is a course reference 
        if course_reference.exists():
            # create the last course
            course_reference = course_reference[0]
            course = Course.objects.create(week=1, start_date=start_date, 
                end_date=end_date, course_reference=course_reference)
            # create the scouts and add them to the course
            for scout in scouts:
                last_name = scout['Last Name']
                first_name = scout['First Name']
                unit = troop_re.search(
                    scout['Group Name (Registration)']).group(0)
                course_scout = Scout.objects.create(last_name=last_name,
                    first_name=first_name, unit=unit)
                course_scout.save()
                course_scout.course_set.add(course)
            course.save()

    roster_file_type = _get_file_type(doubleknot_roster)

    # read the scouts/courses from the roster
    records = pyexcel.iget_records(file_type=roster_file_type, 
        file_content=doubleknot_roster)

    scouts = []
    course_name = ''
    period = ''
    course = None
    course_reference = None
    start_date = datetime.date.today()
    end_date = start_date 
    # for each scout 
    for record in records:
        print(record)
        # TODO figure out what to do here. The period line fails on the
        # Rodney Summer Camp Week line because there is no period.
        temp_course_name = program_re.search(record['Description']).group(0)
        period_re_results = period_re.search(
            record['Description'])
        temp_course_period = ''
        if not period_re_results == None:
            temp_course_period = period_re_results.group('period')
        if (temp_course_name == course_name and  
            temp_course_period == period):    
            scouts.append(record)
        else:
            create_course()
            scouts = []
            scouts.append(record)
            course_name = temp_course_name
            period = temp_course_period
    create_course()

def get_courses(doubleknot_roster):

    roster_file_type = _get_file_type(doubleknot_roster)

    # read the scouts/courses from the roster
    records = pyexcel.iget_records(file_type=roster_file_type, 
        file_content=doubleknot_roster)

    courses = []
    for record in records:
        course_name = program_re.search(record['Description']).group(0)
        period_results = period_re.search(record['Description'])
        if not period_results == None:
            period = period_results.group('period')
        else:
            period = ''
        if (not len(courses) == 0 and (not courses[-1]['name'] == course_name 
            or not courses[-1]['period'] == period)):
            course = {'name' : course_name, 'period' : period}
            courses.append(course)
        elif len(courses) == 0:
            course = {'name' : course_name, 'period' : period}
            courses.append(course)

    return courses

