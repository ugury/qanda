from django.conf.urls.defaults import patterns,url,include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('qanda.views',
    (r'^question/(\d+)/([-\w]+)','get_question'),
    (r'^questions/$','get_questions'),
    (r'^category/([-\w]+)','get_questions_by_category'),
    (r'^question/ask/','ask_question'),
    (r'^question/reply/(\d+)','reply_question'),
)

