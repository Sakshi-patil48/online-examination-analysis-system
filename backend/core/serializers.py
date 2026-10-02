from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Subject, Topic, Question, Exam, ExamQuestion,
    ExamAttempt, StudentAnswer, ProctoringFlag, Notification, AuditLog, QuestionType, DifficultyLevel
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'role', 'bio', 'profile_picture', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_full_name(self, obj):
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}".strip()
        return obj.username

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'full_name', 'first_name', 'last_name', 'role']

    def validate_role(self, value):
        if value.upper() == 'ADMIN':
            raise serializers.ValidationError("Self-registration as ADMIN is strictly prohibited.")
        if value.upper() not in ['STUDENT', 'EXAMINER']:
            raise serializers.ValidationError("Role must be either STUDENT or EXAMINER.")
        return value.upper()

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({'confirm_password': "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        full_name = validated_data.pop('full_name', '')
        
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')

        if full_name and not (first_name or last_name):
            parts = full_name.strip().split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''

        username = validated_data['username']
        email = validated_data.get('email', username)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name,
            role=validated_data.get('role', 'STUDENT')
        )
        return user

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Topic
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['created_by']

class ExamQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = ExamQuestion
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ['created_by', 'join_code', 'created_at']

    def get_questions_count(self, obj):
        return obj.exam_questions.count()

class StudentAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)
    correct_answer = serializers.CharField(source='question.correct_answer', read_only=True)
    options = serializers.JSONField(source='question.options', read_only=True)

    class Meta:
        model = StudentAnswer
        fields = '__all__'
        read_only_fields = ['attempt', 'is_correct', 'score_obtained', 'ai_confidence', 'ai_explanation', 'evaluation_method']

class ExamAttemptSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    exam_subject = serializers.CharField(source='exam.subject.name', read_only=True)
    answers = StudentAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = ExamAttempt
        fields = '__all__'
        read_only_fields = ['student', 'start_time', 'end_time', 'total_score', 'max_possible_score', 'percentage', 'is_passed']

class ProctoringFlagSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='attempt.student.get_full_name', read_only=True)
    exam_title = serializers.CharField(source='attempt.exam.title', read_only=True)

    class Meta:
        model = ProctoringFlag
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = AuditLog
        fields = '__all__'
