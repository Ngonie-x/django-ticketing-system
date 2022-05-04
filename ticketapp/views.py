from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Ticket, Comment
from .forms import TicketForm, TicketUpdateForm

# Create your views here.


class TicketListView(LoginRequiredMixin, generic.ListView):
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urgent_count'] = Ticket.objects.filter(
            assigned_to=self.request.user, urgent_status=True).count()
        context['resolved_count'] = Ticket.objects.filter(
            assigned_to=self.request.user, completed_status=True).count()
        context['unresolved_count'] = Ticket.objects.filter(
            assigned_to=self.request.user, completed_status=False).count()

        return context


class TicketDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            ticket=self.get_object()).order_by('-created_date')
        return context


class TicketCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ticket
    form_class = TicketForm


class TicketUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ticket
    form_class = TicketUpdateForm
    template_name = 'ticketapp/ticket_update.html'


class TicketDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ticket
    success_url = reverse_lazy('ticketapp:ticket-list')


@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticketapp/all_tickets.html', {'tickets': tickets})


@login_required
def urgent_ticket_list(request):
    tickets = Ticket.objects.filter(
        assigned_to=request.user, urgent_status=True)
    return render(request, 'ticketapp/urgent_tickets.html', {'tickets': tickets})


@login_required
def resolved_tickets(request):
    tickets = Ticket.objects.filter(
        assigned_to=request.user, completed_status=True)
    return render(request, 'ticketapp/resolved_tickets.html', {'tickets': tickets})


@login_required
def unresolved_tickets(request):
    tickets = Ticket.objects.filter(
        assigned_to=request.user, completed_status=False)
    return render(request, 'ticketapp/unresolved_tickets.html', {'tickets': tickets})


def add_comment(request, ticket_id):
    if request.method == 'POST':
        comment = request.POST['comment']
        ticket = Ticket.objects.get(id=ticket_id)
        user = request.user

        Comment.objects.create(ticket=ticket, user=user, text=comment)
        return HttpResponseRedirect(reverse("ticketapp:ticket-detail", kwargs={'pk': ticket_id}))
