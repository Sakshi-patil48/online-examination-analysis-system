from django.core.management.base import BaseCommand
from core.models import User, UserRole, Subject, Topic, Question, QuestionType, DifficultyLevel, Exam, ExamQuestion, ExamStatus

class Command(BaseCommand):
    help = 'Seeds initial database data with demo users, subjects, topics, questions, and active exams.'

    def handle(self, *args, **options):
        self.stdout.write("Seeding SmartExams database...")

        # 1. Create Seed Users
        student, _ = User.objects.get_or_create(
            username='student@smartexams.com',
            defaults={
                'email': 'student@smartexams.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': UserRole.STUDENT,
            }
        )
        student.set_password('student123')
        student.save()

        teacher, _ = User.objects.get_or_create(
            username='teacher@smartexams.com',
            defaults={
                'email': 'teacher@smartexams.com',
                'first_name': 'Sarah',
                'last_name': 'Connor',
                'role': UserRole.EXAMINER,
            }
        )
        teacher.set_password('teacher123')
        teacher.save()

        admin_user, _ = User.objects.get_or_create(
            username='admin@smartexams.com',
            defaults={
                'email': 'admin@smartexams.com',
                'first_name': 'Admin',
                'last_name': 'System',
                'role': UserRole.ADMIN,
                'is_staff': True,
                'is_superuser': True
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        self.stdout.write(self.style.SUCCESS("Demo users created: student@smartexams.com / teacher@smartexams.com / admin@smartexams.com"))

        # 2. Create Subjects & Topics
        cs, _ = Subject.objects.get_or_create(code='CS101', defaults={'name': 'Computer Science', 'description': 'Full-stack Web Dev & Architecture'})
        ai, _ = Subject.objects.get_or_create(code='AI201', defaults={'name': 'Artificial Intelligence', 'description': 'Machine Learning & Neural Nets'})
        cyber, _ = Subject.objects.get_or_create(code='SEC301', defaults={'name': 'Cybersecurity', 'description': 'Network Defense & Cryptography'})

        top_react, _ = Topic.objects.get_or_create(subject=cs, name='React Hooks')
        top_rest, _ = Topic.objects.get_or_create(subject=cs, name='REST Protocols')
        top_arch, _ = Topic.objects.get_or_create(subject=cs, name='System Architecture')
        top_trans, _ = Topic.objects.get_or_create(subject=ai, name='Transformers')
        top_model, _ = Topic.objects.get_or_create(subject=ai, name='Model Training')

        # 3. Create Questions (matching Screenshot 4 Question Bank)
        questions_data = [
            {
                'text': 'Which React hook is primarily used for handling side effects like data fetching?',
                'topic': top_react,
                'subject': cs,
                'type': QuestionType.CHOICE,
                'difficulty': DifficultyLevel.EASY,
                'options': [
                    {'id': 'A', 'text': 'useState'},
                    {'id': 'B', 'text': 'useEffect'},
                    {'id': 'C', 'text': 'useContext'},
                    {'id': 'D', 'text': 'useReducer'}
                ],
                'correct': 'B',
                'explanation': 'useEffect allows running side effects in functional React components.',
                'marks': 2.0
            },
            {
                'text': 'In HTTP REST APIs, POST requests are guaranteed to be idempotent according to standard specs.',
                'topic': top_rest,
                'subject': cs,
                'type': QuestionType.TRUE_FALSE,
                'difficulty': DifficultyLevel.MEDIUM,
                'options': [
                    {'id': 'True', 'text': 'True'},
                    {'id': 'False', 'text': 'False'}
                ],
                'correct': 'False',
                'explanation': 'POST is non-idempotent because multiple identical POST requests can create multiple resources.',
                'marks': 1.0
            },
            {
                'text': 'Explain the core difference between client-side rendering (CSR) and server-side rendering (SSR) in web applications.',
                'topic': top_arch,
                'subject': cs,
                'type': QuestionType.SHORT_ANSWER,
                'difficulty': DifficultyLevel.HARD,
                'options': [],
                'correct': 'Client side rendering renders HTML in the browser using JavaScript, whereas Server side rendering generates full HTML on the server before sending it to the client for faster initial page render and better SEO.',
                'explanation': 'Key points: JS bundle execution vs server pre-rendering HTML, SEO impact, and TTFB.',
                'marks': 5.0
            },
            {
                'text': 'What architectural innovation allowed Transformers to process sequence tokens in parallel rather than sequentially?',
                'topic': top_trans,
                'subject': ai,
                'type': QuestionType.CHOICE,
                'difficulty': DifficultyLevel.MEDIUM,
                'options': [
                    {'id': 'A', 'text': 'Recurrent Gates'},
                    {'id': 'B', 'text': 'Self-Attention Mechanism & Positional Encoding'},
                    {'id': 'C', 'text': 'Convolutional Kernels'},
                    {'id': 'D', 'text': 'Max Pooling Layers'}
                ],
                'correct': 'B',
                'explanation': 'Self-attention calculates token interactions simultaneously across the entire sequence.',
                'marks': 3.0
            },
            {
                'text': 'Overfitting occurs when a neural network performs exceptionally well on training data but poorly on unseen test data.',
                'topic': top_model,
                'subject': ai,
                'type': QuestionType.TRUE_FALSE,
                'difficulty': DifficultyLevel.EASY,
                'options': [
                    {'id': 'True', 'text': 'True'},
                    {'id': 'False', 'text': 'False'}
                ],
                'correct': 'True',
                'explanation': 'Overfitting means the model memorizes noise in training data instead of generalizing.',
                'marks': 1.0
            }
        ]

        created_questions = []
        for qd in questions_data:
            q, _ = Question.objects.get_or_create(
                question_text=qd['text'],
                defaults={
                    'created_by': teacher,
                    'topic': qd['topic'],
                    'subject': qd['subject'],
                    'question_type': qd['type'],
                    'difficulty': qd['difficulty'],
                    'options': qd['options'],
                    'correct_answer': qd['correct'],
                    'explanation': qd['explanation'],
                    'marks': qd['marks']
                }
            )
            created_questions.append(q)

        self.stdout.write(self.style.SUCCESS(f"Created {len(created_questions)} sample questions."))

        # 4. Create Active Exams (matching Screenshot 1 & 3)
        exam1, _ = Exam.objects.get_or_create(
            join_code='FULLSTACK-101',
            defaults={
                'title': 'Full-Stack Web Development Midterm',
                'description': 'Comprehensive evaluation of React 18, State Management, REST APIs, and System Architecture.',
                'subject': cs,
                'created_by': teacher,
                'duration_minutes': 45,
                'total_marks': 25.0,
                'pass_percentage': 50.0,
                'is_public': True,
                'proctoring_enabled': True,
                'status': ExamStatus.LIVE
            }
        )
        exam2, _ = Exam.objects.get_or_create(
            join_code='AIML-202',
            defaults={
                'title': 'AI & Machine Learning Assessment',
                'description': 'Evaluation covering Neural Networks, Model Optimization, and Transformer Architectures.',
                'subject': ai,
                'created_by': teacher,
                'duration_minutes': 60,
                'total_marks': 30.0,
                'pass_percentage': 50.0,
                'is_public': True,
                'proctoring_enabled': True,
                'status': ExamStatus.LIVE
            }
        )
        exam3, _ = Exam.objects.get_or_create(
            join_code='CYBER-303',
            defaults={
                'title': 'Cybersecurity & Network Defense',
                'description': 'Covers Encryption standards, Threat vectors, Authentication protocols, and Firewall rules.',
                'subject': cyber,
                'created_by': teacher,
                'duration_minutes': 30,
                'total_marks': 20.0,
                'pass_percentage': 40.0,
                'is_public': True,
                'proctoring_enabled': True,
                'status': ExamStatus.LIVE
            }
        )

        # Attach questions to exam 1
        for idx, q in enumerate(created_questions[:3]):
            ExamQuestion.objects.get_or_create(exam=exam1, question=q, defaults={'order': idx + 1})

        for idx, q in enumerate(created_questions[3:]):
            ExamQuestion.objects.get_or_create(exam=exam2, question=q, defaults={'order': idx + 1})

        self.stdout.write(self.style.SUCCESS("SmartExams database successfully seeded!"))
