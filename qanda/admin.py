from qanda.models import Question,Category,Answer
from django.contrib import admin

class QuestionAdmin(admin.ModelAdmin):
    ordering = ['-pub_date']
    prepopulated_fields = {"slug": ("title",)}
    actions = ['make_published']
    
    # returns the status of the question
    def status(self):
        """
        if its still draft,returns Inactive
        otherwise,returns Published
        """
        if self.active == 0:
            st = 'Inactive'
        else:
            st = 'Published'
        return st
    status.short_description = "Status"
    
    list_display = ('title','pub_date',status)
    list_display_links = ('title',)
    list_filter = ('pub_date','active')
    fields = ('title','slug',
              'body','user','categories','active',
              'tags','pub_date')

    # publishes the selected questions
    def make_published(self, request, queryset):
        """
        Changes the status of the selected questions
        'Draft' becomes 'Active'
        """
        rows_updated = queryset.update(active='1')
        if rows_updated == 1:
            message_bit = "1 question was"
        else:
            message_bit = "%s questions were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
    make_published.short_description = "Mark selected stories as published"

class AnswerAdmin(admin.ModelAdmin):
    ordering = ['-pub_date']
    
    # get the title of the question that the answer belongs to
    def q(self):
        """
        Returns the title of a comment
        """
        title = Question.objects.get(title=self.question)
        return title
    q.short_description = "Question"
    
    # returns the first X words of a answer
    def getAnswer(self,words_to_return=10):
        """
        Returns the first X words of a answer
        """
        answer = Answer.objects.get(pk=self.id)
        answer_content = answer.content
        return ' '.join(answer_content.split()[0:words_to_return]) + ' ...'
    getAnswer.short_description = "Answer"
    
    list_filter = ('user','pub_date')
    list_display = (getAnswer,'user',q,'pub_date')
    fieldsets = [('Answer Information',
                  {'fields' : ('user','content','pub_date','question')})]

class CategoryAdmin(admin.ModelAdmin):
    ordering = ['title']
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [('Category Information',
                 {'fields': ('title','description','slug'),})]
    list_display = ('title','description')

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(Category,CategoryAdmin)
