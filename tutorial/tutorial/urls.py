"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('app01/', include('app01.urls')), # include allows referencing to other urls.py files (in other apps except your root app)
    # this always for easy plug and play behavior (let's say app01 has a few 100 views, you can just store in urls of app01 and include that in your site)
    path('admin/', admin.site.urls),
    # path is passed 4 arguments: 
    # 1. route: string that contains URL pattern (does not include domain name so for "koenvs.com/myapp", you only need to give up "myapp/")
    # 2. view: the first is the py file in which he will call a function, the second word behind the dot is the function he will call (clear in app01/views.py and app01/urls.py)
    # 3. kwargs 
    # 4. name
]
