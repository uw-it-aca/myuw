from django.db import models

class User(models.Model):
    uwnetid = models.SlugField(max_length=16, db_index=True)
    uwregid = models.CharField(max_length=32, db_index=True, unique=True)
    last_visit = models.DateTimeField(default=datetime.now())

class Term(models.Model):
    year = models.PositiveSmallIntegerField()
    QUARTER_CHOICES = (
        ('1', 'Winter'),
        ('2', 'Spring'),
        ('3', 'Summer'),
        ('4', 'Fall'),
    )
    quarter = models.CharField(max_length=1, choices=QUARTER_CHOICES)
    first_day_quarter = models.DateField(db_index=True) 
    last_day_instruction = models.DateField(db_index=True)
    aterm_last_date = models.DateField()
    bterm_first_date = models.DateField()
    last_final_exam_date = models.DateField()
    last_verified = models.DateTimeField()

class Building(models.Model):
    building_code = models.SlugField(max_length=5, db_index=True)
    map_url = models.URLField(verify_exists=False, max_length=255)

class Section(models.Model):
    term = models.ForeignKey(Term, on_delete=models.PROTECT)
    curriculum_abbreviation = models.CharField(max_length=6, db_index=True)
    course_number = models.PositiveSmallIntegerField(db_index=True)
    section_id = models.CharField(max_length=2, db_index=True)
    course_title = models.CharField(max_length=20)
    course_campus = models.CharField(max_length=7)
    section_type = models.CharField(max_length=2)
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
    regid = models.CharField(max_length=32, db_index=True)
    email = models.EmailField(max_length=75)
    name = models.CharField(max_length=80) 
    phone = models.CharField(max_length=16)
    last_verified = models.DateTimeField()

class SectionMeeting(models.Model):
    term = models.ForeignKey(Term, on_delete=models.PROTECT)
    section = models.ForeignKey(Section, on_delete=models.PROTECT)
    meeting_number = models.PositiveSmallIntegerField()
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

class ClassSchedule(models.Model):
    user = models.ForeignKey(User)
    term = models.ForeignKey(Term, on_delete=models.PROTECT)
    section = models.ForeignKey(Section, on_delete=models.PROTECT)
    last_verified = models.DateTimeField()
