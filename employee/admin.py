from django.contrib import admin
from employee.models import Progress, CompletedModuledetail, QuestionAttempted, PostScenario, Recommendation, ReportIssue, Contribution, QnA

class ProgressAdmin(admin.ModelAdmin):
    list_display = ('person_name', 'person_email', 'course_name', 'couse_assigndate')
    list_display_links = ('person_name', 'person_email')
    search_fields = ('person_name', 'person_email', 'course_name')

class CompletedModuleAdmin(admin.ModelAdmin):
    list_display = ('person_email', 'course_name', 'completed_module')
    list_display_links = ('person_email', )
    search_fields = ('completed_module', 'course_name', 'person_email')

class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('person_email', 'recommended_course')
    list_display_links = ('person_email', )
    search_fields = ('recommended_course', 'person_email')

class ContributionAdmin(admin.ModelAdmin):
    list_display = ('title', 'contributor_name', 'submission_date', 'status')
    list_display_links = ('title',)
    search_fields = ('title', 'contributor_name', 'contributor_email', 'status')

class PostScenarioAdmin(admin.ModelAdmin):
    list_display = ('associated_module', 'associated_course', 'person_email', 'is_correct')
    list_display_links = ('associated_module', 'associated_course', 'person_email')
    search_fields = ('associated_module', 'associated_course', 'person_email', 'is_correct')


admin.site.register(Recommendation,RecommendationAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(CompletedModuledetail, CompletedModuleAdmin)
admin.site.register([QuestionAttempted, ReportIssue])
admin.site.register(Contribution, ContributionAdmin)
admin.site.register(PostScenario, PostScenarioAdmin)
admin.site.register(QnA)
