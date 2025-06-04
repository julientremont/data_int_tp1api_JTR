from django.urls import path
from . import views

urlpatterns = [ path("test_json_view/", views.test_json_view, name="test_json_view"),
               path("post_user/", views.post_user, name="add_user"),
               path("get_allproducts/", views.get_allproducts, name="get_allproducts"),
               path("get_maxprice/", views.get_maxprice, name="get_maxprice"),
               path("post_product/", views.post_product, name="post_product"),
               path("update_product/<int:product_id>/", views.update_product, name="update_product"),
                path("admin/create_user/", views.create_api_user, name="create_api_user"),
                path("admin/create_role/", views.create_role, name="create_role"),
]