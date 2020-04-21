from django.contrib import admin
from tracker.models import Users,Skills,SkillMap

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id','user_email', 'user_name','user_date_created')

class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_id','skill_name', 'skill_description','skill_date_created')

class SkillMapAdmin(admin.ModelAdmin):
    list_display = ('skillmap_user_id', 'skillmap_skill_id','skillmap_level')

admin.site.register(Users, UserAdmin)
admin.site.register(Skills, SkillAdmin)
admin.site.register(SkillMap, SkillMapAdmin)
