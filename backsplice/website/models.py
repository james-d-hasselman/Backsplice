from django.db import models

# The field sizes are based on those recommended by the Government Data 
# Standards Catalogue created by the U.K. where applicable.
# 
# The standard can be found here: 
# http://webarchive.nationalarchives.gov.uk/+/http://www.cabinetoffice.gov.uk/media/254290/GDS%20Catalogue%20Vol%202.pdf

class Instructor(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35)
    email = models.EmailField()

# The course catalog according to Doubleknot. Used as a reference table 
# for assigning instructor permissions.
class CourseReference(models.Model):
    name = models.CharField(max_length=70)
    period = models.CharField(max_length=15)
    instructor = models.ForeignKey(Instructor)
    year = models.CharField(max_length=4)

class Requirement(models.Model):
    course_name = models.CharField(max_length=70)
    number = models.IntegerField()
    letter = models.CharField(max_length=1)
    text = models.TextField()

class Scout(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35)
    unit = models.IntegerField()

class Course(models.Model):
    course_reference = models.ForeignKey(CourseReference)
    week = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    scouts = models.ManyToManyField(Scout)

# The merit badge requirements that a scout has completed
class CourseRecord(models.Model):
    scout = models.ForeignKey(Scout)
    course = models.ForeignKey(Course)
    requirement = models.ForeignKey(Requirement)

