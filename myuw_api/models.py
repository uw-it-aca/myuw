from django.db import models
from datetime import datetime

class UserId(models.Model):
    uwregid = models.CharField(max_length=32,
                               db_index=True,
                               unique=True)
    class Meta:
        abstract = True

class User(UserId):
    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)
    last_visit = models.DateTimeField(default=datetime.now())


class Term(models.Model):
    year = models.PositiveSmallIntegerField()
    QUARTERNAME_CHOICES = (
        ('1', 'Winter'),
        ('2', 'Spring'),
        ('3', 'Summer'),
        ('4', 'Fall')
        )
    quarter = models.CharField(max_length=1, 
                               choices=QUARTERNAME_CHOICES)
    first_day_quarter = models.DateField(db_index=True) 
    last_day_instruction = models.DateField(db_index=True)
    aterm_last_date = models.DateField()
    bterm_first_date = models.DateField()
    last_final_exam_date = models.DateField()
    last_verified = models.DateTimeField()
    class Meta:
        unique_together = ('year',
                           'quarter')

class Building(models.Model):
    building_code = models.SlugField(max_length=5,
                                     db_index=True)
    map_url = models.URLField(max_length=255,
                              verify_exists=False)

class Section(models.Model):
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    curriculum_abbr = models.CharField(max_length=6,
                                       db_index=True)
    course_number = models.PositiveSmallIntegerField(db_index=True)
    section_id = models.CharField(max_length=2,
                                  db_index=True)
    course_title = models.CharField(max_length=20)
    course_campus = models.CharField(max_length=7)
    section_type = models.CharField(max_length=2)
    class_website_url = models.URLField(max_length=255,
                              verify_exists=False)
    sln = models.PositiveIntegerField()
    summer_term = models.CharField(max_length=1)
    start_date = models.DateField()
    end_date = models.DateField()
    final_exam_date = models.DateField()
    final_exam_start_time = models.TimeField()
    final_exam_end_time = models.TimeField()
    final_exam_building = models.ForeignKey(Building)
    final_exam_room_number = models.CharField(max_length=5)
    last_verified = models.DateTimeField()
    class Meta:
        unique_together = ('term',
                           'curriculum_abbr',
                           'course_number',
                           'section_id')
        
class Instructor(UserId):
    email = models.EmailField(max_length=75)
    name = models.CharField(max_length=80) 
    phone = models.CharField(max_length=16)
    last_verified = models.DateTimeField()

class SectionMeeting(models.Model):
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    section = models.ForeignKey(Section,
                                on_delete=models.PROTECT)
    meeting_index = models.PositiveSmallIntegerField()
    meeting_type = models.CharField(max_length=2)
    building_to_be_arranged = models.CharField(max_length=3)
    building = models.ForeignKey(Building)
    room_to_be_arranged = models.CharField(max_length=3)
    room_number = models.CharField(max_length=5)
    days_to_be_arranged = models.CharField(max_length=3)
    days_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    last_verified = models.DateTimeField()
    class Meta:
        unique_together = ('term', 
                           'section', 
                           'meeting_index')

class ClassSchedule(models.Model):
    user = models.ForeignKey(User)
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    section = models.ForeignKey(Section,
                                on_delete=models.PROTECT)
    last_verified = models.DateTimeField()


class CourseColor(models.Model):
    regid = models.CharField(max_length=32, db_index=True)
    year = models.PositiveSmallIntegerField(db_index=True)
    quarter = models.CharField(max_length=10, db_index=True)
    curriculum_abbr = models.CharField(max_length=10)
    course_number = models.PositiveSmallIntegerField()
    section_id = models.CharField(max_length=2)
    is_active = models.BooleanField()
    color_id = models.PositiveIntegerField()


