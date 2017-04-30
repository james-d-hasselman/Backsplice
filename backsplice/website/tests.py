from django.test import TestCase
from website.util import doubleknot
from website.models import Course, Scout, Instructor, CourseReference
import pyexcel
import csv
import io
import datetime

# Create your tests here.
class DoubleknotTests(TestCase):

    def setUp(self):
        """
        Setup function that prepares data used by the other tests.
        """

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

        archery_reference = CourseReference(name='Archery MB', period='period 2', 
                                instructor=archery_instructor, year=year)
        archery_reference.save()

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

        test_data = io.StringIO()
        test_data_writer = csv.writer(test_data)
        
        test_data_writer.writerow(['Last Name',
            'First Name',
            'Group Name (Registration)',
            'Description'])
        test_data_writer.writerow(['Hasselman',
            'James',
            'Troop 144 Havertown PA',
            'Rifle Shooting (period 1) Jul 26 2017 10:30 AM (333434)'])
        test_data_writer.writerow(['Jackrabbit',
            'Jazzy',
            'T34,-Someplace,',
            'Archery MB (period 2) Jul 26 2017 9:00 AM (3343234)'])
        test_data_writer.writerow(['Raynor',
            'Jim',
            'Troop #99, Galaxy',
            'Cooking (periods 1 & 2) Jul 26 2017 9:00 AM (32423)'])
        test_data_writer.writerow(['Odinson',
            'Thor',
            'Troop-44,asdf',
            'Brownsea (all periods) Jul 26 2017 8:00 AM (999345)'])
        
        sheet = pyexcel.Sheet()
        sheet.csv = test_data

        self.test_doubleknot_roster = sheet.get_xlsx()
 
    def test_period_re(self):
        """
        Given the Description field from a doubleknot roster 
        the period_re regular expression will extract the course period 
        number.
        """

        scouts = list(pyexcel.iget_records(file_type='xlsx', 
                                    file_content=self.test_doubleknot_roster))
        james = scouts[0]
        period = doubleknot.period_re.search(
                     james['Description']).group('period')
        self.assertEquals(period, 'period 1')
        jazzy = scouts[1]
        period = doubleknot.period_re.search(
                     jazzy['Description']).group('period')
        self.assertEquals(period, 'period 2')
        jim = scouts[2]
        period = doubleknot.period_re.search(
                     jim['Description']).group('period')
        self.assertEquals(period, 'periods 1 & 2')
        thor = scouts[3]
        period = doubleknot.period_re.search(
                     thor['Description']).group('period')
        self.assertEquals(period, 'all periods')

    def test_create_courses(self):
        """
        Given a doubleknot roster in the standard Rodney format: 
        (Last Name, First Name, Group Name (Registration), 
        Description), create_courses() will populate the database with 
        the information from the spreadsheet.
        """
       
        doubleknot.create_courses(self.test_doubleknot_roster)

        courses = Course.objects.all()
        rifle_shooting = courses[0]
        archery = courses[1]
        cooking = courses[2]
        brownsea = courses[3]

        rifle_shooting_ref = rifle_shooting.course_reference
        archery_ref = archery.course_reference
        cooking_ref = cooking.course_reference
        brownsea_ref = brownsea.course_reference

        # check that the courses were created appropriately
        self.assertEqual(rifle_shooting_ref.name, 'Rifle Shooting')
        self.assertEqual(rifle_shooting_ref.period, 'period 1')

        archery = courses[1]
        self.assertEqual(archery_ref.name, 'Archery MB')
        self.assertEqual(archery_ref.period, 'period 2')

        cooking = courses[2]
        self.assertEqual(cooking_ref.name, 'Cooking')
        self.assertEqual(cooking_ref.period, 'periods 1 & 2') 

        brownsea = courses[3]
        self.assertEqual(brownsea_ref.name, 'Brownsea')
        self.assertEqual(brownsea_ref.period, 'all periods') 

        # check that each course has the correct instructor
        self.assertEquals(
            rifle_shooting_ref.instructor.last_name, 'Lenkiewicz')

        archery_ref = archery.course_reference
        self.assertEquals(archery_ref.instructor.last_name, 'Yanos')

        cooking_ref = cooking.course_reference
        self.assertEquals(cooking_ref.instructor.last_name, 'Waters')

        brownsea_ref = brownsea.course_reference
        self.assertEquals(brownsea_ref.instructor.last_name, 'Massey')

        # check that all the scouts were created
        scouts = Scout.objects.all()
        self.assertEqual(len(scouts), 4)

        james = Scout.objects.filter(first_name='James')[0]
        self.assertEqual(james.first_name, 'James')
        self.assertEqual(james.last_name, 'Hasselman')
        self.assertEqual(james.unit, 144)

        jazzy = scouts[1]
        self.assertEqual(jazzy.first_name, 'Jazzy')
        self.assertEqual(jazzy.last_name, 'Jackrabbit')
        self.assertEqual(jazzy.unit, 34)

        jim = scouts[2]
        self.assertEqual(jim.first_name, 'Jim')
        self.assertEqual(jim.last_name, 'Raynor')
        self.assertEqual(jim.unit, 99)

        thor = scouts[3]
        self.assertEqual(thor.first_name, 'Thor')
        self.assertEqual(thor.last_name, 'Odinson')
        self.assertEqual(thor.unit, 44)

        # check that each scout is in the correct course
        rifle_shooting_scout = rifle_shooting.scouts.all()[0]
        self.assertEquals(rifle_shooting_scout.last_name, 'Hasselman')

        archery_scout = archery.scouts.all()[0]
        self.assertEquals(archery_scout.last_name, 'Jackrabbit')
     
        cooking_scout = cooking.scouts.all()[0]
        self.assertEquals(cooking_scout.last_name, 'Raynor')

        brownsea_scout = brownsea.scouts.all()[0]
        self.assertEquals(brownsea_scout.last_name, 'Odinson')

        
