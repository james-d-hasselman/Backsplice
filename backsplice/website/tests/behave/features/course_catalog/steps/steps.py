#from aloe import step, world, before
#from django.test import Client
#from aloe_django import django_url
from behave_django import *
from nose.tools import assert_equals
from website.models import CourseReference, Instructor
from lxml import html
import datetime

#@before.all
#def set_browser():
#    world.browser = Client()

@when(r'the user navigates to the url "{url}"')
def navigate_to_url(context, url):
    #url = django_url(step, url)
    response = context.test.client.get(url)
    response = context.test.client.get(response.url)
    context.response = html.fromstring(response.content)

@when(r'there are courses in the catalog')
def courses_in_the_catalog(context):
    empty_course_catalog(step)
    rifle_instructor = Instructor(first_name='Ron', last_name='Lenkiewicz', 
                           email='cooldipr@gmail.com')
    rifle_instructor.save()
    year = str(datetime.date.today().year)
    rifle_shooting_reference = CourseReference(name='Rifle Shooting',
                                   period='period 1',
                                   instructor=rifle_instructor,
                                   year=year)
    rifle_shooting_reference.save()
    archery_instructor = Instructor(first_name='Mary', last_name='Yanos',
                            email='mary.yanos@gmail.com')
    archery_instructor.save()
    archery_reference = CourseReference(name='Archery',
                            period='2',
                            instructor=archery_instructor,
                            year=year)
    cooking_instructor = Instructor(first_name='Bill', last_name='Waters', 
                            email='muddy.waters@gmail.com')
    cooking_instructor.save()
    cooking_reference = CourseReference(name='Cooking',
                            period='periods 1 & 2',
                            instructor=cooking_instructor, year=year)
    cooking_reference.save()
    brownsea_instructor = Instructor(first_name='Dan', last_name='Massey',
                              email='dan.massey@gmail.com')
    brownsea_instructor.save()
    brownsea_reference = CourseReference(name='Brownsea',
                             period='all periods',
                             instructor=brownsea_instructor, year=year)
    brownsea_reference.save()

@then(r'the courses are displayed')
def courses_displayed(context):
    course_catalog = CourseReference.objects.all()
    catalog_list = context.response.get_element_by_id('catalog')
    for i in range(0, len(course_catalog)):
        course_catalog_record = course_catalog[i]
        course_catalog_display = catalog_list.getchildren()[i].text_content() 
        display_parts = course_catalog_display.split(': ')
        name = display_parts[0]
        period = display_parts[1]
        assert_equals(name, course_catalog_record.name)
        assert_equals(period, course_catalog_record.period)

@then(r'a message is displayed indicating "{message}"')
def message_displayed(context, message):
    body = context.response.body
    message_span = body.get_element_by_id('message')
    assert_equals(message_span.text, message)

@when(r'there are no courses in the catalog')
def empty_course_catalog(context):
    CourseReference.objects.all().delete()
    Instructor.objects.all().delete()

@when(r'the user is on the "{url}" page')
def on_page(context, url):
    navigate_to_url(context, url)

@when(r'the user clicks "{link_name}"')
def click_link(context, link_name):
    body = context.response.body
    link = body.get_element_by_id(link_name.lower())
    href = link.attrib.get('href')
    #url = django_url(step, href)
    response = context.test.client.get(href)
    context.response = html.fromstring(response.content)

@then(r'the course catalog edit page is displayed')
def edit_page_displayed(context):
    head = context.response.head
    title = head.getchildren()[0].text_content()
    assert_equals(title, 'Backsplice - Edit Course Catalog')

@then(r'the import courses page is displayed')
def import_page_displayed(context):
    head = context.response.head
    title = head.getchildren()[0].text_content()
    assert_equals(title, 'Backsplice - Import Courses')
