import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRole(models.TextChoices):
    STUDENT = 'STUDENT', 'Student'
    EXAMINER = 'EXAMINER', 'Examiner'
    ADMIN = 'ADMIN', 'Admin'

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.STUDENT)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_student(self):
        return self.role == UserRole.STUDENT or self.is_superuser

    def is_examiner(self):
        return self.role == UserRole.EXAMINER or self.is_superuser

    def is_admin_user(self):
        return self.role == UserRole.ADMIN or self.is_superuser

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject.code} - {self.name}"

class QuestionType(models.TextChoices):
    CHOICE = 'CHOICE', 'Multiple Choice'
    TRUE_FALSE = 'TRUE_FALSE', 'True / False'
    SHORT_ANSWER = 'SHORT_ANSWER', 'Short Answer'

class DifficultyLevel(models.TextChoices):
    EASY = 'EASY', 'Easy'
    MEDIUM = 'MEDIUM', 'Medium'
    HARD = 'HARD', 'Hard'

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QuestionType.choices, default=QuestionType.CHOICE)
    difficulty = models.CharField(max_length=20, choices=DifficultyLevel.choices, default=DifficultyLevel.MEDIUM)
    options = models.JSONField(default=list, blank=True)  # List of dicts e.g. [{"id":"A","text":"Opt A"}]
    correct_answer = models.TextField(help_text="For CHOICE: option id ('A'). For TRUE_FALSE: 'True'/'False'. For SHORT_ANSWER: Model answer keywords.")
    explanation = models.TextField(blank=True, null=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.question_type}] {self.question_text[:50]}"

class ExamStatus(models.TextChoices):
    SCHEDULED = 'SCHEDULED', 'Scheduled'
    LIVE = 'LIVE', 'Live'
    CONCLUDED = 'CONCLUDED', 'Concluded'

class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='exams')
    join_code = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_exams')
    duration_minutes = models.PositiveIntegerField(default=60)
    total_marks = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    pass_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=40.00)
    negative_marking = models.BooleanField(default=False)
    negative_marks_per_question = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    randomize_questions = models.BooleanField(default=True)
    randomize_options = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    proctoring_enabled = models.BooleanField(default=True)
    instructions = models.TextField(blank=True, default="Please read all questions carefully before submitting.")
    status = models.CharField(max_length=20, choices=ExamStatus.choices, default=ExamStatus.LIVE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.join_code})"

class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='in_exams')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        unique_together = ('exam', 'question')

class AttemptStatus(models.TextChoices):
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    SUBMITTED = 'SUBMITTED', 'Submitted'
    EVALUATED = 'EVALUATED', 'Evaluated'

class ExamAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=AttemptStatus.choices, default=AttemptStatus.IN_PROGRESS)
    total_score = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    max_possible_score = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_passed = models.BooleanField(default=False)
    time_spent_seconds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - {self.exam.title} ({self.status})"

class EvalMethod(models.TextChoices):
    AUTO_MCQ = 'AUTO_MCQ', 'Auto MCQ/TF'
    GEMINI = 'GEMINI', 'Gemini AI'
    KEYWORD_FALLBACK = 'KEYWORD_FALLBACK', 'Keyword Fallback'
    MANUAL_OVERRIDE = 'MANUAL_OVERRIDE', 'Manual Examiner Override'

class StudentAnswer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=100, null=True, blank=True)
    short_answer_text = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True)
    score_obtained = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    ai_confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ai_explanation = models.TextField(null=True, blank=True)
    evaluation_method = models.CharField(max_length=30, choices=EvalMethod.choices, default=EvalMethod.AUTO_MCQ)
    examiner_override = models.BooleanField(default=False)
    examiner_notes = models.TextField(null=True, blank=True)
    is_marked_for_review = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('attempt', 'question')

class FlagSeverity(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'

class ProctoringFlag(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='proctor_flags')
    flag_type = models.CharField(max_length=50) # TAB_SWITCH, FULLSCREEN_EXIT, FACE_MISSING, MULTIPLE_FACES
    severity = models.CharField(max_length=20, choices=FlagSeverity.choices, default=FlagSeverity.MEDIUM)
    timestamp = models.DateTimeField(auto_now_add=True)
    image_snapshot = models.TextField(null=True, blank=True) # base64 data string
    reviewed = models.BooleanField(default=False)
    examiner_notes = models.TextField(null=True, blank=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    details = models.JSONField(default=dict)
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
