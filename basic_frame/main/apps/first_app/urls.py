from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index), #template for registration
    url(r'^users$', views.index), #template for registration
    url(r'^users/(?P<id>\d+)$', views.show), #template for success
    url(r'^users/login_page$', views.login_page), #template for login
    url(r'^users/(?P<id>\d+)/edit$', views.edit_page),#edit template
    url(r'^quotes$', views.dashboard), #quote homepage
    #------POSTS------------
    url(r'^users/logout$', views.logout), #clears session
    url(r'^users/add$', views.create), #post create user
    url(r'^users/edit$', views.edit_user), #edit post and validate
    url(r'^quotes/add/(?P<user_id>\d+)$', views.addquote), #posts a quote from dashboard
    url(r'^quotes/delete/(?P<quote_id>\d+)$', views.delquote), #posts a quote from dashboard
    url(r'^quotes/like/(?P<user_id>\d+)/(?P<quote_id>\d+)$', views.like), #posts a quote from dashboard
    #-------VALIDATIONS------
    url(r'^users/login$', views.login), #login validation
    #url(r'^users/(?P<id>\d+)/delete$', views.destroy) #post
    # ------PAGE---------
    url(r'^coin$', views.coin),
]
