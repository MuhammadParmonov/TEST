from django.urls import path
from .views import index, my_tests, create_test, create_question, update_test

urlpatterns = [
    path("", index, name="index" ),
    path("my_tests/", my_tests, name="my_tests"),
    path("create-test/", create_test, name="create_test"),
    path("create-question/<int:test_id>/", create_question, name="create_question"),
    path("update_test/<int:test_id>/", update_test, name="update_test"),
]