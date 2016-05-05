from django.conf.urls import include,url
from web_api import views

urlpatterns = [
    url(r'get_config/$',views.get_config),
	url(r'handle_data/$',views.handle_data),
]
