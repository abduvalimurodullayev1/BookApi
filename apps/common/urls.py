from django.urls import path

from apps.common.api_endpoints import *
from apps.common.views import health_check_redis, BookList, BookDelete, BookUpdate, BookDetail, BookDownload

app_name = "common"

urlpatterns = [
    # path("VersionHistory/", VersionHistoryView.as_view(), name="version-history"),
    path("Book-List", BookList.as_view(), name="book-list"),
    path("Book-delete/<int:pk>", BookDelete.as_view(), name="delete"),
    path("Book-Update/<int:pk>", BookUpdate.as_view(), name="update"),
    path("Book-Detail/<int:pk>", BookDetail.as_view(), name="detail"),
    path("Book-Download/<int:pk>", BookDownload.as_view(), name="download"),



    path("health-check/redis/", health_check_redis, name="health-check-redis"),
]
