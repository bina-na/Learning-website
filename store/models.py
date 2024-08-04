from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set_permissions",  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Category(models.Model):
    title = models.CharField(max_length=255)

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="instructor")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    enrollment_date = models.DateField(auto_now_add=True)

class Course(models.Model):
    STATUS_PENDING = 'Y'
    STATUS_PUBLISHED = 'O'
    
    STATUS_CHOICE = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PUBLISHED, 'Published'),
    ]
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    instructor = models.OneToOneField(Instructor, on_delete=models.PROTECT, related_name="course_instructor")
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default=STATUS_PENDING)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="course_category")

class Lesson(models.Model):
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, primary_key=True, related_name="lessons")
    video_file = models.FileField(upload_to='lessons/tutorial/', blank=True, null=True)

class Assignment(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, primary_key=True, related_name="course_assignment")
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    upload_file = models.FileField(upload_to='lessons/assignment/', blank=True, null=True)

class Question(models.Model):
    question = models.CharField(max_length=255)
    choice_a = models.CharField(max_length=255)
    choice_b = models.CharField(max_length=255)
    choice_c = models.CharField(max_length=255)
    choice_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

class Quiz(models.Model):
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, primary_key=True, related_name="course_quiz")

class Exam(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, primary_key=True, related_name="course_exam")

class QuizResult(models.Model):
    quiz = models.OneToOneField(Quiz, on_delete=models.PROTECT, primary_key=True, related_name="quizresult")
    score = models.CharField(max_length=255)

class AssignmentResult(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.PROTECT, related_name="assignment_result")
    score = models.CharField(max_length=255)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="course_belongs_to")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_course")

class Track(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="track_stud")
    assignment_result = models.OneToOneField(AssignmentResult, on_delete=models.PROTECT, related_name="track_assignment")
    quiz_result = models.OneToOneField(QuizResult, on_delete=models.PROTECT, related_name="track_quiz")

class Certificate(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name="course_certified")
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="stud_certified")
    description = models.CharField(max_length=255)
    logo = models.FileField(upload_to='certificate/logo/', blank=True, null=True)
    student_photo = models.FileField(upload_to='certificate/student_photo/', blank=True, null=True)

class Grade(models.Model):
    quiz_result = models.ForeignKey(QuizResult, on_delete=models.CASCADE, related_name="quiz_grade")
    assignment_result = models.ForeignKey(AssignmentResult, on_delete=models.CASCADE, related_name="assignment_grade")
    calculate_result = models.CharField(max_length=255)

class Payment(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETED = 'C'
    PAYMENT_FAILED = 'F'

    PAYMENT_STATUS = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETED, 'Complete'),
        (PAYMENT_FAILED, 'Failed'),
    ]
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name="course_payment")
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="course_student")
    reference_no = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_PENDING)
