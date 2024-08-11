from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create-listing", views.create_listing, name="create-listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path('listing/<int:listing_id>/handle_bid/', views.handle_bid, name='handle_bid'),
    path('listing/<int:listing_id>/handle_watchlist/', views.handle_watchlist, name='handle_watchlist'),
    path('listing/<int:listing_id>/add_comment/', views.add_comment, name='add_comment'),
    path('listing/<int:listing_id>/close/', views.close, name='close'),
    path('listing/<int:listing_id>/open/', views.open, name='open'),
    path('listing/<int:listing_id>/delete/', views.delete, name='delete'),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>/", views.category_listings, name="category_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
