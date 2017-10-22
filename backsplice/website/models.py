from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone

# The field sizes are based on those recommended by the Government Data 
# Standards Catalogue created by the U.K. where applicable.
# 
# The standard can be found here: 
# http://webarchive.nationalarchives.gov.uk/+/http://www.cabinetoffice.gov.uk/media/254290/GDS%20Catalogue%20Vol%202.pdf

class Instructor(models.Model):
    """
    A member of camp staff who teaches one or merit badges or other camp 
    program courses.
    """

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35)
    email = models.EmailField()

# The course catalog according to Doubleknot. Used as a reference table 
# for assigning instructor permissions.
class CourseReference(models.Model):
    """
    A camp program offering for a summer.

    This is a catalog entry that represents the course being offered and 
    the time of day it is offered each week of camp. These are typically 
    merit badges, but can be any sort of program a camp offers such as 
    Brownsea or another first year camper program.
    """

    name = models.CharField(max_length=70)
    period = models.CharField(max_length=15)
    # should probably be many to many between instructors and courses but
    # keep it simple for now.
    instructor = models.ForeignKey(Instructor, null=True)
    year = models.CharField(max_length=4)

    def __str__(self):
        return self.name + ": " + self.period

class Requirement(models.Model):
    """
    A requirement for successful completion of a course. 

    Typically merit badge requirements, but can also be requirements for 
    any other camp program which has requirements. Scouts must complete 
    requirements to earn badges and other awards.
    """

    course_reference = models.ForeignKey(CourseReference)
    number = models.IntegerField()
    letter = models.CharField(max_length=1)
    text = models.TextField()

class Scout(models.Model):
    """
    A boy scout. 

    Scouts attend one or more weeks of summer camp and 
    participate in one or more courses (typically merit badges, but not 
    neccessarily) completing requirements in pursuit of one or more merit 
    badges or awards.
    """

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35)
    unit = models.IntegerField()

class Course(models.Model):
    """
    A course as offered from the course catalog.

    Represents one week of one course. If the course reference (from the 
    catalog) is Rifle Shooting period 1 and camp offers it for 8 weeks during 
    the summer then at the end of the summer there would be 8 records pointing 
    to the Rifle Shooting period 1 course reference. Each instance of a course 
    is used as a base to track the progress of all scouts in that course that 
    week.
    """

    course_reference = models.ForeignKey(CourseReference)
    week = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    scouts = models.ManyToManyField(Scout)

# The merit badge requirements that a scout has completed
class CourseRecord(models.Model):
    """
    A record indicating a scout has completed a requirement for a course.

    Each of these records indicates that a particular scout has completed a 
    particular requirement for a particular course. At the end of of the week 
    The instructor will use this information to determine whether or not the 
    scout has completed the course successfully or not.
    """

    scout = models.ForeignKey(Scout)
    course = models.ForeignKey(Course)
    requirement = models.ForeignKey(Requirement)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, 
                     **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """

        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True, 
                          is_superuser=is_superuser, date_joined=now, 
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):

        return self._create_user(email, password, False, False, 
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        return self._create_user(email, password, True, True, 
                                 **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for Backsplice which requires an email address to be 
    used ad the user name.

    Requires email address, first name, and last name. User name is set to 
    the email address that is provided.
    """

    email = models.EmailField(_('email'), unique=True,
        help_text=_('Required.'),
        error_messages={
            'unique': _('A user with that username already exists.'),
        })
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last_name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into the admin ' 
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_approved = models.BooleanField(_('approved'), default=True,
        help_text=_('Designates whether this user has been approved for '
                    'Backsplice access by an administrator.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'
    
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """

        full_name = '%s %s' % (self.first_name, self.last_name)
        
        return full_name.strip()

    def get_short_name(self):
        """
        Returls the short name for the user."
        """
       
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """

        send_mail(subject, message, from_email, [self.email], **kwargs)

