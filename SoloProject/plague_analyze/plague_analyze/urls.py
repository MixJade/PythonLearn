"""plague_analyze URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path

from plague_analyze.前端控制器 import qian01, qian02, qian03, qian04, qian05


print("urls开始发挥作用")
urlpatterns = [
    path('admin/', admin.site.urls),
    path('qian01/', qian01),
    path('qian02/', qian02),
    path('qian03/', qian03),
    path('qian04/', qian04),
    path('qian05/', qian05),
    ]
