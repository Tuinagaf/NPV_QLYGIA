from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_prices_view, name='search_prices'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('partners/', views.partner_list, name='partner_list'),
    path('partners/create/', views.partner_create, name='partner_create'),
    path('partners/<int:pk>/', views.partner_detail, name='partner_detail'),
    path('partners/<int:pk>/edit/', views.partner_update, name='partner_update'),
    path('partners/<int:pk>/add_route/', views.partner_add_route, name='partner_add_route'),
    path('api/routes/<int:pk>/', views.api_route_detail, name='api_route_detail'),
    path('api/routes/<int:pk>/update/', views.api_route_update, name='api_route_update'),
    path('api/routes/<int:pk>/delete/', views.api_delete_route, name='api_delete_route'),
    
    # Base Price URLs
    path('base-prices/', views.base_price_list, name='base_price_list'),
    path('api/base-prices/', views.api_get_base_prices, name='api_get_base_prices'),
    path('api/base-prices/save/', views.api_save_base_price, name='api_save_base_price'),
    path('api/base-prices/<int:pk>/', views.api_base_price_detail, name='api_base_price_detail'),
    path('api/base-prices/<int:pk>/update/', views.api_update_base_price, name='api_update_base_price'),
    path('api/base-prices/export-info/', views.api_export_base_prices_info, name='api_export_base_prices_info'),
    path('api/base-prices/export/', views.api_export_base_prices_excel, name='api_export_base_prices_excel'),
    path('api/base-prices/template/', views.api_download_base_price_template, name='api_download_base_price_template'),
    path('api/base-prices/import/', views.api_import_base_prices_excel, name='api_import_base_prices_excel'),
    
    # Search Prices URLs
    path('api/search-prices/', views.api_search_prices, name='api_search_prices'),
    path('api/get-base-price/', views.api_get_base_price, name='api_get_base_price'),
    path('api/base-prices/bulk-update/', views.api_bulk_update_base_prices, name='api_bulk_update_base_prices'),
    
    # Proposals
    path('proposals/', views.proposal_list_view, name='proposal_list'),
    path('api/proposals/create/', views.api_create_proposal, name='api_create_proposal'),
    path('api/proposals/<int:pk>/approve/', views.api_approve_proposal, name='api_approve_proposal'),
    path('api/proposals/<int:pk>/reject/', views.api_reject_proposal, name='api_reject_proposal'),
    path('api/check-duplicate-partner-routes/', views.api_check_duplicate_partner_routes, name='api_check_duplicate_partner_routes'),
    path('api/partners/<int:pk>/delete/', views.api_delete_partner, name='api_delete_partner'),
    path('api/partners/export/', views.api_export_partners_excel, name='api_export_partners_excel'),
    path('api/partners/template/', views.api_export_partner_template, name='api_export_partner_template'),
    path('api/partners/import/', views.api_import_partners_excel, name='api_import_partners_excel'),
    path('api/partners/bulk-delete/', views.api_bulk_delete_partners, name='api_bulk_delete_partners'),
    path('api/base-prices/<int:pk>/delete/', views.api_delete_base_price, name='api_delete_base_price'),
    path('api/check-new-proposals/', views.api_check_new_proposals, name='api_check_new_proposals'),
    
    # User Management (cũ - modal)
    path('users/', views.user_management_list, name='user_list'),
    path('api/users/create/', views.api_create_user, name='api_create_user'),
    path('api/users/<int:pk>/update/', views.api_update_user, name='api_update_user'),
    path('api/users/<int:pk>/delete/', views.api_delete_user, name='api_delete_user'),

    # Quản lý Tài khoản (mới - trang riêng)
    path('manage-accounts/', views.account_list, name='account_list'),
    path('manage-accounts/create/', views.account_create, name='account_create'),
    path('manage-accounts/<int:pk>/edit/', views.account_update, name='account_update'),
    path('api/manage-accounts/<int:pk>/delete/', views.api_delete_account, name='api_delete_account'),
]
