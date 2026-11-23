"""
SpeechBloom AI - Core App URL Configuration
"""
from django.urls import path
from core import views

urlpatterns = [
    # ── Page Routes ──────────────────────────────────────────
    path('',                   views.index_view,              name='index'),
    path('login/',             views.login_view,              name='login'),
    path('register/',          views.register_view,           name='register'),
    path('logout/',            views.logout_view,             name='logout'),
    path('profile/',           views.child_profile_view,      name='profile'),
    path('dashboard/',         views.child_dashboard_view,    name='child_dashboard'),
    path('child-dashboard/',   views.child_dashboard_view,    name='child_dashboard_alias'),
    path('parent/',            views.parent_dashboard_view,   name='parent_dashboard'),
    path('therapist/',         views.therapist_dashboard_view,name='therapist_dashboard'),
    path('practice/',          views.practice_view,           name='practice'),
    path('recording/',         views.recording_view,          name='recording'),
    path('games/',             views.games_hub_view,          name='games'),
    path('games/<str:game_type>/', views.game_detail_view,    name='game_detail'),
    path('progress/',          views.progress_view,           name='progress'),
    path('about/',             views.about_view,              name='about'),
    path('dataset-info/',      views.dataset_info_view,       name='dataset_info'),

    # ── REST API Routes ───────────────────────────────────────
    path('api/register',                   views.api_register,         name='api_register'),
    path('api/login',                      views.api_login,            name='api_login'),
    path('api/children',                   views.api_children,         name='api_children'),
    path('api/children/<int:child_id>',    views.api_children,         name='api_child_detail'),
    path('api/recording',                  views.api_recording,        name='api_recording'),
    path('api/analyze',                    views.api_analyze,          name='api_analyze'),
    path('api/exercises',                  views.api_exercises,        name='api_exercises'),
    path('api/progress/<int:child_id>',    views.api_progress,         name='api_progress'),
    path('api/games/save',                 views.api_game_save,        name='api_game_save'),
    path('api/games/progress/<int:child_id>', views.api_game_progress, name='api_game_progress'),
    path('api/dashboard/parent',           views.api_parent_dashboard, name='api_parent_dashboard'),
    path('api/model/status',               views.api_model_status,     name='api_model_status'),
    path('api/unique-words/<int:child_id>', views.api_unique_words,     name='api_unique_words'),
    path('api/daily-quest/<int:child_id>',  views.api_daily_quest,      name='api_daily_quest'),
    path('api/badges/<int:child_id>',       views.api_badges,           name='api_badges'),
]
