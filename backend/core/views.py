import random
from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg, Count, Q, Sum, Max, Min
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    User, Subject, Topic, Question, Exam, ExamQuestion,
    ExamAttempt, StudentAnswer, ProctoringFlag, Notification, AuditLog,
    QuestionType, DifficultyLevel, ExamStatus, AttemptStatus, EvalMethod, UserRole
)
from .serializers import (
    UserSerializer, RegisterSerializer, SubjectSerializer, TopicSerializer,
    QuestionSerializer, ExamSerializer, ExamAttemptSerializer, StudentAnswerSerializer,
    ProctoringFlagSerializer, NotificationSerializer, AuditLogSerializer
)
from .permissions import IsStudent, IsExaminer, IsAdminUser
from .services.ai_evaluator import evaluate_short_answer

class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_import']:
            return [IsExaminer()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        total = Question.objects.count()
        mcq_count = Question.objects.filter(question_type=QuestionType.CHOICE).count()
        tf_count = Question.objects.filter(question_type=QuestionType.TRUE_FALSE).count()
        short_count = Question.objects.filter(question_type=QuestionType.SHORT_ANSWER).count()

        return Response({
            'total_questions': total,
            'mcq_count': mcq_count,
            'tf_count': tf_count,
            'short_count': short_count
        })

    @action(detail=False, methods=['post'])
    def bulk_import(self, request):
        questions_data = request.data.get('questions', [])
        created_count = 0
        for item in questions_data:
            Question.objects.create(
                created_by=request.user,
                question_text=item.get('question_text', ''),
                question_type=item.get('question_type', QuestionType.CHOICE),
                difficulty=item.get('difficulty', DifficultyLevel.MEDIUM),
                options=item.get('options', []),
                correct_answer=item.get('correct_answer', ''),
                explanation=item.get('explanation', ''),
                marks=item.get('marks', 1.0)
            )
            created_count += 1

        return Response({'message': f'Successfully imported {created_count} questions.'}, status=status.HTTP_201_CREATED)

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all().order_by('-created_at')
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsExaminer()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        exam = serializer.save(created_by=self.request.user)
        question_ids = self.request.data.get('question_ids', [])
        for idx, q_id in enumerate(question_ids):
            try:
                q = Question.objects.get(id=q_id)
                ExamQuestion.objects.create(exam=exam, question=q, order=idx+1)
            except Question.DoesNotExist:
                pass

    @action(detail=False, methods=['get'])
    def public(self, request):
        public_exams = Exam.objects.filter(is_public=True).order_by('-created_at')
        serializer = self.get_serializer(public_exams, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_exams(self, request):
        if request.user.is_examiner():
            exams = Exam.objects.filter(created_by=request.user)
        else:
            attempted_exam_ids = ExamAttempt.objects.filter(student=request.user).values_list('exam_id', flat=True)
            exams = Exam.objects.filter(Q(is_public=True) | Q(id__in=attempted_exam_ids)).distinct()
        
        serializer = self.get_serializer(exams, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def join(self, request):
        join_code = request.data.get('join_code', '').strip()
        try:
            exam = Exam.objects.get(join_code__iexact=join_code)
            serializer = self.get_serializer(exam)
            return Response(serializer.data)
        except Exam.DoesNotExist:
            return Response({'error': 'Invalid exam join code.'}, status=status.HTTP_404_NOT_FOUND)

class ExamAttemptViewSet(viewsets.ModelViewSet):
    queryset = ExamAttempt.objects.all().order_by('-start_time')
    serializer_class = ExamAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def start(self, request):
        exam_id = request.data.get('exam_id')
        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            return Response({'error': 'Exam not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check existing in-progress attempt for this student
        attempt = ExamAttempt.objects.filter(
            student=request.user,
            exam=exam,
            status=AttemptStatus.IN_PROGRESS
        ).first()

        if not attempt:
            max_score = ExamQuestion.objects.filter(exam=exam).aggregate(total=Sum('question__marks'))['total'] or 0.0
            attempt = ExamAttempt.objects.create(
                student=request.user,
                exam=exam,
                status=AttemptStatus.IN_PROGRESS,
                max_possible_score=max_score
            )

        serializer = self.get_serializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def attempt_state(self, request, pk=None):
        attempt = self.get_object()
        if attempt.student != request.user and not request.user.is_examiner():
            return Response({'error': 'Access denied to this attempt.'}, status=status.HTTP_403_FORBIDDEN)

        exam = attempt.exam
        deadline = attempt.start_time + timedelta(minutes=exam.duration_minutes)
        now = timezone.now()
        remaining_seconds = max(0, int((deadline - now).total_seconds()))

        # Auto-submit if time expired and still in progress
        if remaining_seconds <= 0 and attempt.status == AttemptStatus.IN_PROGRESS:
            self._evaluate_attempt(attempt, time_spent=exam.duration_minutes * 60)
            attempt.refresh_from_db()

        # Fetch questions
        exam_questions = ExamQuestion.objects.filter(exam=exam).select_related('question')
        questions_data = []
        for eq in exam_questions:
            q = eq.question
            q_dict = {
                'id': q.id,
                'question_text': q.question_text,
                'question_type': q.question_type,
                'difficulty': q.difficulty,
                'marks': float(q.marks),
                'options': q.options if q.question_type == QuestionType.CHOICE or q.question_type == QuestionType.TRUE_FALSE else []
            }
            questions_data.append(q_dict)

        # Fetch saved answers
        saved_answers = StudentAnswer.objects.filter(attempt=attempt)
        answers_dict = {}
        for sa in saved_answers:
            answers_dict[sa.question_id] = {
                'selected_option': sa.selected_option,
                'short_answer_text': sa.short_answer_text,
                'is_marked_for_review': sa.is_marked_for_review
            }

        return Response({
            'attempt_id': attempt.id,
            'exam_id': exam.id,
            'exam_title': exam.title,
            'instructions': exam.instructions,
            'duration_minutes': exam.duration_minutes,
            'status': attempt.status,
            'remaining_seconds': remaining_seconds,
            'questions': questions_data,
            'saved_answers': answers_dict,
            'is_passed': attempt.is_passed,
            'total_score': float(attempt.total_score),
            'max_possible_score': float(attempt.max_possible_score),
            'percentage': float(attempt.percentage)
        })

    @action(detail=True, methods=['post'])
    def save_answer(self, request, pk=None):
        attempt = self.get_object()
        if attempt.student != request.user:
            return Response({'error': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)

        if attempt.status != AttemptStatus.IN_PROGRESS:
            return Response({'error': 'Attempt is already completed or submitted.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check deadline
        deadline = attempt.start_time + timedelta(minutes=attempt.exam.duration_minutes)
        if timezone.now() > deadline + timedelta(seconds=10):
            self._evaluate_attempt(attempt, time_spent=attempt.exam.duration_minutes * 60)
            return Response({'error': 'Time limit expired. Exam submitted.'}, status=status.HTTP_400_BAD_REQUEST)

        question_id = request.data.get('question_id')
        selected_option = request.data.get('selected_option', None)
        short_answer_text = request.data.get('short_answer_text', None)
        is_marked_for_review = request.data.get('is_marked_for_review', False)

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found.'}, status=status.HTTP_404_NOT_FOUND)

        answer, _ = StudentAnswer.objects.get_or_create(attempt=attempt, question=question)
        if selected_option is not None:
            answer.selected_option = selected_option
        if short_answer_text is not None:
            answer.short_answer_text = short_answer_text
        answer.is_marked_for_review = bool(is_marked_for_review)
        answer.save()

        return Response({'message': 'Answer saved successfully.'})

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        attempt = self.get_object()
        if attempt.student != request.user:
            return Response({'error': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)

        if attempt.status in [AttemptStatus.SUBMITTED, AttemptStatus.EVALUATED]:
            serializer = self.get_serializer(attempt)
            return Response(serializer.data)

        time_spent = request.data.get('time_spent_seconds', 0)
        self._evaluate_attempt(attempt, time_spent=time_spent)
        attempt.refresh_from_db()

        serializer = self.get_serializer(attempt)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def result(self, request, pk=None):
        attempt = self.get_object()
        if attempt.student != request.user and not request.user.is_examiner():
            return Response({'error': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)

        exam = attempt.exam
        answers = StudentAnswer.objects.filter(attempt=attempt).select_related('question', 'question__topic')
        
        # Calculate topic performance
        topic_stats = {}
        answers_list = []

        correct_count = 0
        incorrect_count = 0
        unanswered_count = 0

        total_questions = ExamQuestion.objects.filter(exam=exam).count()

        for ans in answers:
            q = ans.question
            t_name = q.topic.name if q.topic else 'General'
            if t_name not in topic_stats:
                topic_stats[t_name] = {'total_marks': 0.0, 'earned_marks': 0.0}
            
            topic_stats[t_name]['total_marks'] += float(q.marks)
            topic_stats[t_name]['earned_marks'] += float(ans.score_obtained)

            if ans.is_correct:
                correct_count += 1
            elif ans.selected_option or ans.short_answer_text:
                incorrect_count += 1

            answers_list.append({
                'id': ans.id,
                'question_id': q.id,
                'question_text': q.question_text,
                'question_type': q.question_type,
                'difficulty': q.difficulty,
                'marks': float(q.marks),
                'score_obtained': float(ans.score_obtained),
                'is_correct': ans.is_correct,
                'selected_option': ans.selected_option,
                'short_answer_text': ans.short_answer_text,
                'correct_answer': q.correct_answer,
                'explanation': q.explanation,
                'ai_confidence': float(ans.ai_confidence) if ans.ai_confidence else None,
                'ai_explanation': ans.ai_explanation,
                'evaluation_method': ans.evaluation_method
            })

        unanswered_count = max(0, total_questions - (correct_count + incorrect_count))

        topic_breakdown = []
        for t_name, stat in topic_stats.items():
            perc = round((stat['earned_marks'] / stat['total_marks'] * 100), 1) if stat['total_marks'] > 0 else 0.0
            topic_breakdown.append({'topic': t_name, 'accuracy': perc})

        return Response({
            'attempt_id': attempt.id,
            'exam_id': exam.id,
            'exam_title': exam.title,
            'student_name': attempt.student.get_full_name() or attempt.student.username,
            'status': attempt.status,
            'is_passed': attempt.is_passed,
            'total_score': float(attempt.total_score),
            'max_possible_score': float(attempt.max_possible_score),
            'percentage': float(attempt.percentage),
            'pass_percentage': float(exam.pass_percentage),
            'time_spent_seconds': attempt.time_spent_seconds,
            'correct_count': correct_count,
            'incorrect_count': incorrect_count,
            'unanswered_count': unanswered_count,
            'total_questions': total_questions,
            'topic_breakdown': topic_breakdown,
            'answers': answers_list
        })

    def _evaluate_attempt(self, attempt, time_spent=0):
        attempt.time_spent_seconds = time_spent
        attempt.end_time = timezone.now()
        attempt.status = AttemptStatus.EVALUATED

        total_score = 0.0
        max_possible = 0.0

        exam_questions = ExamQuestion.objects.filter(exam=attempt.exam).select_related('question')
        for eq in exam_questions:
            q = eq.question
            max_possible += float(q.marks)
            ans = StudentAnswer.objects.filter(attempt=attempt, question=q).first()

            if not ans:
                continue

            if q.question_type in [QuestionType.CHOICE, QuestionType.TRUE_FALSE]:
                user_ans = str(ans.selected_option or '').strip().lower()
                correct_ans = str(q.correct_answer or '').strip().lower()
                if user_ans == correct_ans:
                    ans.is_correct = True
                    ans.score_obtained = float(q.marks)
                    ans.evaluation_method = EvalMethod.AUTO_MCQ
                else:
                    ans.is_correct = False
                    if attempt.exam.negative_marking:
                        ans.score_obtained = -float(attempt.exam.negative_marks_per_question)
                    else:
                        ans.score_obtained = 0.0
                    ans.evaluation_method = EvalMethod.AUTO_MCQ
                ans.save()
            elif q.question_type == QuestionType.SHORT_ANSWER:
                res = evaluate_short_answer(
                    question_text=q.question_text,
                    model_answer=q.correct_answer,
                    student_answer=ans.short_answer_text or '',
                    max_marks=float(q.marks)
                )
                ans.is_correct = res['is_correct']
                ans.score_obtained = res['score_obtained']
                ans.ai_confidence = res['confidence']
                ans.ai_explanation = res['explanation']
                ans.evaluation_method = res['evaluation_method']
                ans.save()

            total_score += float(ans.score_obtained)

        attempt.total_score = max(0.0, total_score)
        attempt.max_possible_score = max_possible
        attempt.percentage = round((attempt.total_score / max_possible * 100), 2) if max_possible > 0 else 0.0
        attempt.is_passed = attempt.percentage >= float(attempt.exam.pass_percentage)
        attempt.save()

class ProctoringViewSet(viewsets.ModelViewSet):
    queryset = ProctoringFlag.objects.all().order_by('-timestamp')
    serializer_class = ProctoringFlagSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def log_flag(self, request):
        attempt_id = request.data.get('attempt_id')
        flag_type = request.data.get('flag_type', 'SUSPICIOUS_BEHAVIOR')
        severity = request.data.get('severity', 'MEDIUM')
        image_snapshot = request.data.get('image_snapshot', '')

        try:
            attempt = ExamAttempt.objects.get(id=attempt_id)
        except ExamAttempt.DoesNotExist:
            return Response({'error': 'Attempt not found.'}, status=status.HTTP_404_NOT_FOUND)

        flag = ProctoringFlag.objects.create(
            attempt=attempt,
            flag_type=flag_type,
            severity=severity,
            image_snapshot=image_snapshot
        )
        serializer = self.get_serializer(flag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsExaminer])
    def review(self, request, pk=None):
        flag = self.get_object()
        flag.reviewed = True
        flag.examiner_notes = request.data.get('notes', '')
        flag.save()
        serializer = self.get_serializer(flag)
        return Response(serializer.data)

class StudentAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        attempts = ExamAttempt.objects.filter(student=user, status=AttemptStatus.EVALUATED)
        exams_taken = attempts.count()

        if exams_taken == 0:
            return Response({
                'exams_taken': 0,
                'avg_score': 0.0,
                'pass_rate': 0.0,
                'weak_topics_count': 0,
                'topic_mastery': [],
                'weak_topics': [],
                'strong_topics': [],
                'active_sessions': ExamSerializer(Exam.objects.filter(status=ExamStatus.LIVE, is_public=True)[:5], many=True).data,
                'study_plan': [
                    "Complete your first exam to unlock AI-driven personalized insights.",
                    "Explore public exams in Computer Science and AI/ML.",
                    "Practice short-answer and multiple-choice questions in the Question Bank."
                ]
            })

        avg_score = attempts.aggregate(avg=Avg('percentage'))['avg'] or 0.0
        passed_count = attempts.filter(is_passed=True).count()
        pass_rate = round((passed_count / exams_taken * 100), 1)

        answers = StudentAnswer.objects.filter(attempt__in=attempts, question__topic__isnull=False).select_related('question__topic')
        topic_stats = {}
        for ans in answers:
            t_name = ans.question.topic.name
            if t_name not in topic_stats:
                topic_stats[t_name] = {'total': 0, 'correct': 0}
            topic_stats[t_name]['total'] += 1
            if ans.is_correct:
                topic_stats[t_name]['correct'] += 1

        topic_mastery = []
        weak_topics = []
        strong_topics = []
        for t_name, stat in topic_stats.items():
            acc = round((stat['correct'] / stat['total'] * 100), 1) if stat['total'] > 0 else 0.0
            topic_mastery.append({'topic': t_name, 'accuracy': acc, 'attempts': stat['total']})
            if acc < 60.0:
                weak_topics.append(t_name)
            elif acc >= 80.0:
                strong_topics.append(t_name)

        study_plan = []
        if weak_topics:
            study_plan.append(f"Focus on improving mastery in weak topics: {', '.join(weak_topics)}.")
            study_plan.append("Review detailed explanations in Question Bank for short-answer items.")
        else:
            study_plan.append("Great job! Your performance across all evaluated topics is strong.")
            study_plan.append("Keep practicing timed assessments to maintain accuracy and speed.")

        active_sessions = Exam.objects.filter(status=ExamStatus.LIVE, is_public=True)[:5]

        return Response({
            'exams_taken': exams_taken,
            'avg_score': round(avg_score, 1),
            'pass_rate': pass_rate,
            'weak_topics_count': len(weak_topics),
            'topic_mastery': topic_mastery,
            'weak_topics': weak_topics,
            'strong_topics': strong_topics,
            'active_sessions': ExamSerializer(active_sessions, many=True).data,
            'study_plan': study_plan
        })

class ExaminerAnalyticsView(APIView):
    permission_classes = [IsExaminer]

    def get(self, request):
        attempts = ExamAttempt.objects.filter(status=AttemptStatus.EVALUATED)
        total_students = User.objects.filter(role=UserRole.STUDENT).count()
        total_attempts = attempts.count()
        
        avg_score = attempts.aggregate(avg=Avg('percentage'))['avg'] or 0.0
        passed_count = attempts.filter(is_passed=True).count()
        pass_rate = round((passed_count / total_attempts * 100), 1) if total_attempts > 0 else 0.0
        
        highest_score = attempts.aggregate(max_s=Max('percentage'))['max_s'] or 0.0
        lowest_score = attempts.aggregate(min_s=Min('percentage'))['min_s'] or 0.0

        return Response({
            'total_students': total_students,
            'total_attempts': total_attempts,
            'class_avg_score': round(avg_score, 1),
            'pass_rate': pass_rate,
            'highest_score': highest_score,
            'lowest_score': lowest_score,
        })

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        if user == request.user:
            return Response({'error': 'You cannot deactivate your own admin account.'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = not user.is_active
        user.save()
        return Response({'message': f"User {user.username} active status set to {user.is_active}."})

class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            'total_users': User.objects.count(),
            'total_students': User.objects.filter(role=UserRole.STUDENT).count(),
            'total_examiners': User.objects.filter(role=UserRole.EXAMINER).count(),
            'total_exams': Exam.objects.count(),
            'total_attempts': ExamAttempt.objects.count(),
            'total_proctor_flags': ProctoringFlag.objects.count()
        })
