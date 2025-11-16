from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import make_password,check_password
# Create your models here.

class courses(models.Model):
    course_id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=100)

class sub(models.Model):
    sub_id=models.AutoField(primary_key=True)
    sub_names=models.CharField(max_length=100)

class course_sub:
    course_id=models.ForeignKey(courses,on_delete=models.CASCADE)
    sub_id=models.ForeignKey(sub,on_delete=models.CASCADE)


class stu_details(models.Model):
    stu_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=75)
    age = models.IntegerField(
    validators=[
        MinValueValidator(18),  # Minimum value constraint
        MaxValueValidator(50)  # Maximum value constraint
    ]
    )
    div=models.CharField(max_length=2)
    enroll=models.CharField(max_length=15, unique=True)
    email=models.EmailField(max_length=150,unique=True,null=True)
    stu_pass=models.CharField(max_length=128,null=True)
    roll_no=models.IntegerField()
    course_id=models.ForeignKey(courses,on_delete=models.CASCADE)


class Registration_t(models.Model):
    t_id=models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    sub_id = models.ForeignKey(sub, on_delete=models.CASCADE)
    experience = models.PositiveIntegerField()
    address = models.TextField()
    teach_pass=models.CharField(max_length=128,null=True)

class Admin_log(models.Model):
    a_id = models.AutoField(primary_key=True)
    admin_id = models.CharField(max_length=10, unique=True, default='1234@')
    admin_pass = models.CharField(max_length=128, default='admin123')  # Default plaintext password

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is new
            self.admin_pass = make_password(self.admin_pass)  # Hash the password
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.admin_pass)


class stu_Login(models.Model):
    stu_id = models.ForeignKey(stu_details, on_delete=models.CASCADE, related_name='logins_by_stu_id', null=True)  # Allow null temporarily
    enroll = models.ForeignKey(stu_details, on_delete=models.CASCADE, related_name='logins_by_enroll', null=True)  # Allow null temporarily
    stu_pass = models.CharField(max_length=128)


class profess(models.Model):
    prof_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=75)
    prof_login_id=models.CharField(max_length=50)
    prof_pass=models.CharField(max_length=128)

class questions(models.Model):
    que_id=models.AutoField(primary_key=True)
    question_main=models.TextField()
    class Difficulty(models.IntegerChoices):
        EASY = 1, 'Easy'
        MODERATE = 2, 'Moderate'
        DIFFICULT = 3, 'Difficult'
        VERY_DIFFICULT = 4, 'Very Difficult'

    difficulty_level = models.IntegerField(choices=Difficulty.choices, default=Difficulty.EASY)
    description=models.TextField(null=True)
    solve_time=models.TimeField()
    sub_id=models.ForeignKey(sub,on_delete=models.CASCADE,null=True)
    marks=models.IntegerField(null=True)

class in_out(models.Model):
    que_id=models.ForeignKey(questions,on_delete=models.CASCADE)
    in_put=models.CharField(max_length=50)
    out_put=models.CharField(max_length=50)

class prac(models.Model):
    que_id=models.ForeignKey(questions,on_delete=models.CASCADE)
    sub_id=models.ForeignKey(sub,on_delete=models.CASCADE)

class exam(models.Model):
    exam_id=models.AutoField(primary_key=True)
    sub_id=models.ForeignKey(sub,on_delete=models.CASCADE)
    exam_title=models.TextField(null=True)
    div=models.TextField(null=True)
    exam_time=models.TimeField()
    exam_date=models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
    duration=models.TimeField(default="20:00")

class exam_stu(models.Model):
    test = models.ForeignKey(exam, on_delete=models.CASCADE)
    stu_id=models.ForeignKey(stu_details,on_delete=models.CASCADE)
    q1=models.IntegerField(null=True)
    q2=models.IntegerField(null=True)
    q3=models.IntegerField(null=True)
    q4=models.IntegerField(null=True)
    q5=models.IntegerField(null=True)

class assignment(models.Model):
    assi_id=models.AutoField(primary_key=True)
    deadline=models.DateTimeField(auto_now_add=True)

class assi_sub(models.Model):
    assi_id=models.ForeignKey(assignment,on_delete=models.CASCADE)
    sub_id=models.ForeignKey(sub,on_delete=models.CASCADE)

class assi_que(models.Model):
    assi_id=models.ForeignKey(assignment,on_delete=models.CASCADE)
    que_id=models.ForeignKey(questions,on_delete=models.CASCADE)

class assi_stu(models.Model):
    assi_id=models.ForeignKey(assignment,on_delete=models.CASCADE)
    que_id=models.ForeignKey(questions,on_delete=models.CASCADE)
    stu_id=models.ForeignKey(stu_details,on_delete=models.CASCADE)

class penalty(models.Model):
    stu_id=models.ForeignKey(stu_details,on_delete=models.CASCADE)
    assi_id=models.ForeignKey(assignment,on_delete=models.CASCADE)
    amt=models.IntegerField()
    status=models.BooleanField(default=False)

class Mark(models.Model):
    student = models.ForeignKey(stu_details, on_delete=models.CASCADE,default=False)
    test = models.ForeignKey(exam, on_delete=models.CASCADE)
    total_marks = models.IntegerField()

    def __str__(self):
        return self.message

class MarkDetail(models.Model):
    question = models.ForeignKey(questions, on_delete=models.CASCADE)
    student = models.ForeignKey(stu_details, on_delete=models.CASCADE,default=False)
    test = models.ForeignKey(exam, on_delete=models.CASCADE,default=False)
    marks_obtained = models.IntegerField()
    def __str__(self):
        return self.message

class Notification(models.Model):
    user = models.ForeignKey(stu_details, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    