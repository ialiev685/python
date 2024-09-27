from django.urls import path, include
from django.views.generic import TemplateView
from blog import views

product_patterns = [
    path("", view=views.products),
    path("new/", view=views.new),
    path("top/", view=views.top),
]

urlpatterns = [
    path("", views.index, name="index"),
    path("access/<int:age>", views.acceess),
    path("access/", views.acceess),
    path("products/<int:id>/", include(product_patterns)),
    path("user/", views.user),
    path("about/", views.about, name="about"),
    # path(
    #     "about/",
    #     TemplateView.as_view(
    #         template_name="blog/about.html", extra_context={"header": "О сайте"}
    #     ),
    # ),
    path("contact/", views.contact),
    path("details/", views.details),
]
