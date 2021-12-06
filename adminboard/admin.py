from django.contrib import admin
from adminboard.models import Module, AuthorizedPanel, Course, Scenario, Question, Process

class CourseList(admin.ModelAdmin):
    list_display = ('course_name', 'module', 'sequence_num')
    list_display_links = ('course_name', 'module')
    search_fields = ('course_name',)

class ModuleList(admin.ModelAdmin):
    list_display = ('module_name', 'status')
    list_display_links = ('module_name',)
    search_fields = ('module_name',)

class ScenarioList(admin.ModelAdmin):
    list_display = ('scenario_desc', 'associated_module')
    list_display_links = ('scenario_desc', 'associated_module')
    search_fields = ('scenario_desc', 'associated_module')

class QuestionList(admin.ModelAdmin):
    list_display = ('question', 'module_name')
    list_display_links = ('question', 'module_name')
    search_fields = ('question', 'module_name')

admin.site.register(Course, CourseList)
admin.site.register(Module, ModuleList)
admin.site.register(Scenario, ScenarioList)
admin.site.register(Question, QuestionList)
admin.site.register([AuthorizedPanel, Process])