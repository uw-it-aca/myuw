from django.db import models

class User(models.Model):
    netid = models.SlugField(max_length=16)
    regid = models.CharField(max_length=32)
    last_visit = models.DateTimeField()

class Term(models.Model):
    year = models.CharField(max_length=4)
    quarter = models.CharField(max_length=6)
    first_day_quarter = models.DateField() 
    last_day_instruction = models.DateField()
    aterm_last_date = models.DateField()
    bterm_first_date = models.DateField()
    last_final_exam_date = models.DateField()
    last_verified = models.DateTimeField()

class Building(models.Model):
    building_code = models.SlugField(max_length=10)
    map_url = models.URLField(verify_exists=False, max_length=255)

class Section(models.Model):
    term = models.ForeignKey(Term)
    curriculum_abbreviation = models.CharField(max_length=5)
    course_number = models.PositiveSmallIntegerField()
    section_id = models.CharField(max_length=2)
    course_title = models.CharField(max_length=255)
    course_campus = models.PositiveSmallIntegerField()
    section_type = models.CharField(max_length=1)
    class_website_url = models.URLField(verify_exists=False, max_length=255)
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
        
class Instructor(models.Model):
    name = models.CharField(max_length=80) 
    regid = models.CharField(max_length=32)
    email = models.EmailField(max_length=75)
    phone = models.CharField(max_length=16)
    last_verified = models.DateTimeField()

class SectionMeeting(models.Model):
    term = models.ForeignKey(Term)
    section = models.ForeignKey(Section)
    meeting_number = models.PositiveSmallIntegerField()
    meeting_type = models.CharField(max_length=2)
    building_to_be_arranged = models.CharField(max_length=16)
    building = models.ForeignKey(Building)
    room_to_be_arranged = models.CharField(max_length=16)
    room_number = models.CharField(max_length=5)
    days_to_be_arranged = models.CharField(max_length=16)
    days_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    instructor = models.ForeignKey(Instructor)
    last_verified = models.DateTimeField()

class ClassSchedule(models.Model):
    user = models.ForeignKey(User)
    term = models.ForeignKey(Term)
    section = models.ForeignKey(Section)
    last_verified = models.DateTimeField()
