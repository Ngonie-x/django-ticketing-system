from django.urls import path
from . import views

app_name = 'ticketapp'

urlpatterns = [
    path('', views.TicketListView.as_view(), name='ticket-list'),
    path('ticket-detail/<int:pk>/',
         views.TicketDetailView.as_view(), name='ticket-detail'),
    path('create-ticket/', views.TicketCreateView.as_view(), name='create-ticket'),
    path('update-ticket/<int:pk>/',
         views.TicketUpdateView.as_view(), name='update-ticket'),
    path('delete-ticket/<int:pk>/',
         views.TicketDeleteView.as_view(), name='delete-ticket'),
    path('all-tickets/', views.ticket_list, name='all-tickets'),
    path('resolved-tickets/', views.resolved_tickets, name='resolved-tickets'),
    path('unresolved-tickets/', views.unresolved_tickets,
         name='unresolved-tickets'),
    path('urgent-tickets/', views.urgent_ticket_list, name='urgent-tickets'),
    path('add-comment/<int:ticket_id>/', views.add_comment, name='add-comment'),
]
