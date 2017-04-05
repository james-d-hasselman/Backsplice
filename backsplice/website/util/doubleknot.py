import re
import pyexcel
import magic
from website.models import Course, Scout
import datetime

# re to find the period
# m = re.search(r'\((?P<period>.*\d)\)[^$]', <Description>)
# m.group('period')
period_re = re.compile(r'\((?P<period>.*)\)[^$]')

# re to find the camp program
# m = re.search(r'^[^\(]*[^\s\(]', <Description>)
# m.group(0)
program_re = re.compile(r'^[^\(]*[^\s\(]')

# re to find the troop number
# m = re.search(r'[0-9]{1,4}', <Group Name (Registration)>)
troop_re = re.compile(r'[0-9]{1,4}')

def create_courses(doubleknot_roster):
    mime_type = magic.from_buffer(doubleknot_roster, mime=True)
    if mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        roster_file_type = 'xlsx'
    elif mime_type == 'application/vnd.ms-excel':
        roster_file_type = 'xls'
    else:
        roster_file_type = 'ods'

    # read the scouts from the roster
    scouts = pyexcel.iget_records(file_type=roster_file_type, file_content=doubleknot_roster)
    # create the first course
    scout = next(scouts)
    course_name = program_re.search(scout['Description']).group(0)
    period = period_re.search(scout['Description']).group('period')
    # TODO set the start date, end date, week, and instructor
    start_date = datetime.date.today()
    end_date = datetime.date.today()
    course = Course.objects.create(name=course_name, period=period, week=1, 
                                   start_date=start_date, end_date=end_date, 
                                   instructor_id=1)

    # add the scout to the course
    scout_last_name = scout['Last Name']
    scout_first_name = scout['First Name']
    scout_unit = troop_re.search(
                       scout['Group Name (Registration)']).group(0)
    course_scout = Scout.objects.create(last_name=scout_last_name, 
                         first_name=scout_first_name, 
                         unit=scout_unit)
    course_scout.save()
    course_scout.course_set.add(course)

    # for each scout in the roster
    for scout in scouts:
        # read the course name
        course_name = program_re.search(scout['Description']).group(0)
        # read the course period
        period = period_re.search(scout['Description']).group('period')
        # if the course name or period is different from the current course 
        if not course_name == course.name or period == course.period:
            # write the current course out to the database
            course.save()
            # start collecting data for the new course
            # TODO set the start date, end date, week, and instructor
            course = Course.objects.create(name=course_name, period=period, 
                         week=1, start_date=start_date, end_date=end_date, 
                         instructor_id=1)
        # add the scout to the current course
        scout_last_name = scout['Last Name']
        scout_first_name = scout['First Name']
        scout_unit = troop_re.search(
                           scout['Group Name (Registration)']).group(0)
        course_scout = Scout.objects.create(last_name=scout_last_name, 
                             first_name=scout_first_name, 
                             unit=scout_unit)
        course_scout.save()
        course_scout.course_set.add(course)
    course.save()

