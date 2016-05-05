from django.conf.urls import include,url
from web_manage import views
urlpatterns = [
	url(r'login/',views.login,name='login'),
    url(r'host/',views.host),
    url(r'user_group/',views.user_group),
    url(r'audit_user/',views.user_audit),
	url(r'user_audit/(\d+)/$',views.user_audit, name='user_audit'),
    url(r'memory/(\d+)/$',views.memory),
	url(r'cpu/(\d+)/$',views.cpu),
    url(r'graphs_json/(\d+)/$',views.graphs_json),
    url(r'idle/(\d+)/$',views.idle),
]
