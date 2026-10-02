from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView, CurrentUserView, SubjectViewSet, TopicViewSet,
    QuestionViewSet, ExamViewSet, ExamAttemptViewSet, ProctoringViewSet,
    StudentAnalyticsView, ExaminerAnalyticsView, AdminUserViewSet, AdminStatsView
)

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'attempts', ExamAttemptViewSet)
router.register(r'proctoring', ProctoringViewSet)
router.register(r'admin/users', AdminUserViewSet, basename='admin_users')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/profile/', CurrentUserView.as_view(), name='auth_profile'),
    path('auth/me/', CurrentUserView.as_view(), name='auth_me'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('student/analytics/', StudentAnalyticsView.as_view(), name='student_analytics'),
    path('examiner/analytics/', ExaminerAnalyticsView.as_view(), name='examiner_analytics'),
    path('admin/stats/', AdminStatsView.as_view(), name='admin_stats'),
    path('', include(router.urls)),
]
