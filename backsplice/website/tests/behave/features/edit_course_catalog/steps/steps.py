#from django.test.client import Client
from website.models import CourseReference, Instructor
from lxml import html
#from aloe_django import django_url
#from aloe import world, step, before
from nose.tools import assert_equals, assert_not_equals
from datetime import datetime
from behave_django import *
from django.http.response import HttpResponseRedirect

INPUT_NAME_XPATH_FORMAT = ".//input[@name='{}']"

#@before.all
#def set_browser():
#    world.browser = Client()

@when(r'there are courses in the course catalog')
def populate_catalog(context):
    year = datetime.now().year
    
    archery = CourseReference(name='Archery',
                              period='period 3',
                              year=year)
    archery.save()

    rifle = CourseReference(name='Rifle Shooting',
                            period='period 2',
                            year=year)
    rifle.save()

    cooking = CourseReference(name='Cooking',
                              period='period 2 & lunch',
                              year=year)
    cooking.save()

@when(r'the user navigates to the "{url}" page')
def navigate_to_edit_page(context, url):
    #url = django_url(step, url)
#    print(url)
    response = context.test.client.get(url)
#    print(response)
#    print(response.url)
    response = context.test.client.get(response.url)
#    print(response)
#    print(response.content)
    context.response = html.fromstring(response.content)

@then(r'the courses are displayed one course per line with a text box containing the name of the course')
def course_names_displayed(context):
    course_catalog = CourseReference.objects.all()
#    print(len(course_catalog))
    for course in course_catalog:
        field_name = 'n' + str(course.id)
#        print(html.tostring(context.response))
#        print(field_name)
        xpath = INPUT_NAME_XPATH_FORMAT.format(field_name)
#        print(xpath)
        catalog_course_field = context.response.find(xpath)
#        print(str(catalog_course_field))
        course_name = catalog_course_field.attrib['value']
        assert_equals(course_name, course.name)

@then(r'a textbox containing the period')
def course_periods_displayed(context):
    course_catalog = CourseReference.objects.all()
    for course in course_catalog:
        field_name = 'p' + str(course.id)
        xpath = INPUT_NAME_XPATH_FORMAT.format(field_name)
        catalog_period_field = context.response.find(xpath)
        period = catalog_period_field.value
        assert_equals(period, course.period)

@when(r'there are no courses in the course catalog')
def clear_catalog(context):
    CourseReference.objects.all().delete()

@then(r'a message is displayed indicating "{message}"')
def message_displayed(context, message):
    message_span = context.response.get_element_by_id('message')
    assert_equals(message_span.text_content(), message)

@when(r'the user clicks "Add" without providing a course name')
def click_add_no_course_name(context):
    xpath = INPUT_NAME_XPATH_FORMAT.format('course')
    course_name_field = context.response.find(xpath)
    xpath = INPUT_NAME_XPATH_FORMAT.format('course-period')
    course_period_field = context.response.find(xpath)
    course_name_field.value = None
    course_period_field.value = 'period 1'
    click_button(context, 'Add')

@then(r'an error message is displayed that says "{message}"')
def error_displayed(context, message):
    error_span = context.response.get_element_by_id('error_message')
    assert_equals(error_span.text_content(), message)

@when(r'the user clicks "Add" without providing a period')
def click_add_no_period(context):
    xpath = INPUT_NAME_XPATH_FORMAT.format('course')
    course_name_field = context.response.find(xpath)
    xpath = INPUT_NAME_XPATH_FORMAT.format('course-period')
    course_period_field = context.response.find(xpath)
    course_name_field.value = 'Rifle Shooting'
    course_period_field.value = None
    click_button(context, 'Add')

@when(r'the course name of any course in the course catalog is made blank')
def catalog_course_name_made_blank(context):
    course_catalog = CourseReference.objects.all()
    course = course_catalog[0]
    field_name = 'n' + str(course.id)
    xpath = INPUT_NAME_XPATH_FORMAT.format(field_name)
    course_name_field = context.response.find(xpath)
    course_name_field.value = None
 
@when(r'the user clicks "{button_text}"')
def click_button(context, button_text):
    print("Button Text: " + str(button_text))
    button_name = button_text.lower()
    xpath = INPUT_NAME_XPATH_FORMAT.format(button_name)
    button = context.response.find(xpath)
    url = '/course_catalog/edit/'
    form = button.getparent()
    post_values = {}
    for html_input in form.findall(".//input"):
        if not html_input.type == 'submit':
            post_values[html_input.name] = html_input.value
    print("Post Values: " + str(post_values))
    print("Button: " + str(button))
    post_values[button.name] = button.value
    response = context.test.client.post(url, post_values)
    if type(response) == HttpResponseRedirect:
        response = context.test.client.get(response.url)
    context.response = html.fromstring(response.content)

@then(r'the "{url}" page is displayed again with the previous course name restored')
def restore_previous_course_name(context, url):
    title = context.response.find('head/title')
    assert_equals('Backsplice - Edit Course Catalog', title.text)
    course_catalog = CourseReference.objects.all()
    course = course_catalog[0]
    field_name = 'n' + str(course.id)
    xpath = INPUT_NAME_XPATH_FORMAT.format(field_name)
    course_name_field = context.response.find(xpath)
    assert_equals(course.name, course_name_field.value)
 
@when(r'the user is on the "{url}" page')
def on_edit_page(context, url):
    navigate_to_edit_page(context, url)

@when(r'the period of any course in the course catalog is made blank')
def catalog_period_name_made_blank(context):
    course_catalog = CourseReference.objects.all()
    course = course_catalog[0]
    field_name = 'p' + str(course.id)
    xpath = INPUT_NAME_XPATH_FORMAT.format(field_name)
    course_period_field = context.response.find(xpath)
    course_period_field.value = None

@then(r'the "{url}" page is displayed again with the previous period restored')
def restore_previous_period(context, url):
    title = context.response.find('head/title')
    assert_equals('Backsplice - Edit Course Catalog', title.text)
    course_catalog = CourseReference.objects.all()
    course = course_catalog[0]
    field_name = 'p' + str(course.id)
    xpath = INPUT_NAME_XPATH_FORMAT.format(field_name)
    course_period_field = context.response.find(xpath)
    assert_equals(course.period, course_period_field.value)

@when(r'the provided course name and period name match those of an existing course in the course catalog')
def add_produces_duplicate_course(context):
    course_name_xpath = INPUT_NAME_XPATH_FORMAT.format('course')
    course_name_field = context.response.find(course_name_xpath)
    course_name_field.value = 'Archery'
    course_period_xpath = INPUT_NAME_XPATH_FORMAT.format('course-period')
    course_period_field = context.response.find(course_period_xpath)
    course_period_field.value = 'period 3'

def get_course_fields(course, context):
    course_name_field_name = 'n' + str(course.id)
    course_name_xpath = INPUT_NAME_XPATH_FORMAT.format(course_name_field_name)
    course_name = context.response.find(course_name_xpath)
    course_period_field_name = 'p' + str(course.id)
    course_period_xpath = INPUT_NAME_XPATH_FORMAT.format(course_period_field_name)
    course_period = context.response.find(course_period_xpath)

    return (course_name, course_period)


@when(r'two or more courses in the course catalog have matching names and periods')
def edit_duplicate_course(context):
    courses = CourseReference.objects.all()
    course1_name, course1_period = get_course_fields(courses[0], context)
    course2_name, course2_period = get_course_fields(courses[1], context)
    course1_name.value = 'Shotgun Shooting'
    course1_period.value = 'period 1'
    course2_name.value = 'Shotgun Shooting'
    course2_period.value = 'period 1'
 
@then(r'the "{url}" page is displayed again with the offending change(s) reverted')
def revert_offending_changes(context, url):
    title = context.response.find('head/title')
    assert_equals('Backsplice - Edit Course Catalog', title.text)
    courses = CourseReference.objects.all()
    course1_name, course1_period = get_course_fields(courses[0], context)
    course2_name, course2_period = get_course_fields(courses[1], context)
    assert_not_equals('Shotgun Shooting', courses[0].name)
    assert_not_equals('period 1', courses[0].period)
    assert_not_equals('Shotgun Shooting', courses[1].name)
    assert_not_equals('period 1', courses[1].period)
    assert_equals(courses[0].name, course1_name.value)
    assert_equals(courses[0].period, course1_period.value)
    assert_equals(courses[1].name, course2_name.value)
    assert_equals(courses[1].period, course2_period.value)

@when(r'the user has provided a valid course name and period')
def add_valid_data(context):
    course_xpath = INPUT_NAME_XPATH_FORMAT.format('course')
    course = context.response.find(course_xpath)
    course.value = 'Shotgun Shooting'
    course_period_xpath = INPUT_NAME_XPATH_FORMAT.format('course-period')
    course_period = context.response.find(course_period_xpath)
    course_period.value = 'period 1'

#@then(r'the course is added to the course catalog')
#def course_added_to_catalog(context):
#    shotgun_shooting = CourseReference.objects.get(name='Shotgun Shooting')
#    course_name_xpath = 'n' + str(shotgun_shooting.id)
#    course_name_field = context.response.find(course_name_xpath)
#    course_period_xpath = 'p' + str(shotgun_shooting.id)
#    course_period_field = context.response.find(course_period_xpath)
#    assert_equals('Shotgun Shooting', course_name_field.value)
#    assert_equals('period 1', course_period_field.value)

@then(r'the "{url}" page is displayed again with the new course included in the course catalog section')
def new_course_displayed_in_catalog(context, url):
    title = context.response.find('head/title')
    assert_equals('Backsplice - Edit Course Catalog', title.text)
    shotgun_shooting = CourseReference.objects.get(name='Shotgun Shooting')
    print('ID: {}'.format(shotgun_shooting.id))
    course_name_xpath = INPUT_NAME_XPATH_FORMAT.format('n' + str(shotgun_shooting.id))
    print('Course Name ID: {}'.format(course_name_xpath))
    course_name_field = context.response.find(course_name_xpath)
    course_period_xpath = INPUT_NAME_XPATH_FORMAT.format('p' + str(shotgun_shooting.id))
    course_period_field = context.response.find(course_period_xpath)
    assert_equals('Shotgun Shooting', course_name_field.value)
    assert_equals('period 1', course_period_field.value)
 
@when(r'the edited courses have valid names and periods')
def save_valid_edits(context):
    courses = CourseReference.objects.all()
    course1_name, course1_period = get_course_fields(courses[0], context)
    course2_name, course2_period = get_course_fields(courses[1], context)
    course3_name, course3_period = get_course_fields(courses[2], context)
    course1_name.value = 'Shotgun Shooting'
    course1_period.value = 'period 1'
    course2_name.value = 'Swimming'
    course2_period.value = 'period 2'
    course3_name.value = 'Nature'
    course3_period.value = 'period 3'
 
@then(r'the changes are saved to the course catalog')
def edits_saved(context):
    courses = CourseReference.objects.all()
    assert_equals('Shotgun Shooting', courses[0].name)
    assert_equals('period 1', courses[0].period)
    assert_equals('Swimming', courses[1].name)
    assert_equals('period 2', courses[1].period)
    assert_equals('Nature', courses[2].name)
    assert_equals('period 3', courses[2].period)

@then(r'the user is returned to the "{url}" page which displays the changed course catalog')
def on_view_catalog_page(context, url):
    title = context.response.find('head/title')
    assert_equals('Backsplice - Course Catalog', title.text)
    catalog = context.response.get_element_by_id('catalog')
    assert_not_equals(catalog.xpath('li[text()="Shotgun Shooting: period 1"]'), [])
    assert_not_equals(catalog.xpath('li[text()="Swimming: period 2"]'), [])
    assert_not_equals(catalog.xpath('li[text()="Nature: period 3"]'), [])

@when(r'there is a valid course name and period in the add course fields')
def add_fields_valid_data(context):
    add_valid_data(context)

@when(r'there are unsaved changes to the existing course catalog')
def edit_unsaved_changes(context):
    courses = CourseReference.objects.all()
    course1_name, course1_period = get_course_fields(courses[0], context)
    course1_name.value = 'Wood Carving'
    course1_period.value = 'period 4'

@then(r'the unsaved changes discarded')
def unsaved_changes_discarded(context):
    title = context.response.find('head/title')
    assert_equals('Backsplice - Edit Course Catalog', title.text)
    wood_carving = CourseReference.objects.all().filter(name='Wood Carving', period='period 4')
    assert_equals(len(wood_carving), 0)

@then(r'the new course included in the course catalog section')
def new_course_included(context):
    new_course_displayed_in_catalog(context) 

@when(r'the user has provided a course name and period in the fields used to add a course to the course catalog')
def add_fields_populated(context):
    add_valid_data(context)

@then(r'the values in the course name and period fields used for adding a course to the catalog are discarded')
def discard_add_field_values(context):
    course_name_xpath = INPUT_NAME_XPATH_FORMAT.format('course')
    course_name_field = context.response.find(course_name_xpath)
    assert_equals(course_name_field.value, '')
    course_period_xpath = INPUT_NAME_XPATH_FORMAT.format('course-period')
    course_name_field = context.response.find(course_period_xpath)
    assert_equals(course_period_field.value, '')
    shotgun_shooting = CourseReference.objects.get(name__exact='Shotgun Shooting', period__exact='period 1')
    assert_equals(shotgun_shooting, None)

@then(r'the user is returned to the "{url}" page')
def return_to_view(context, url):
    title = context.response.find('head/title')
    assert_equals('Backsplice - Course Catalog', title.text)

@then(r'the course name and period are discarded')
def discard_course_name_and_period(context):
    catalog = context.response.get_element_by_id('catalog')
    assert_not_equals(catalog.xpath('li[text()="Shotgun Shooting: period 1"]'), [])
    assert_not_equals(catalog.xpath('li[text()="Swimming: period 2"]'), [])
    assert_not_equals(catalog.xpath('li[text()="Nature: period 3"]'), [])

