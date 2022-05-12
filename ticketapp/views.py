import datetime
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.db.models import Q
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
        context['normal_user_list'] = Ticket.objects.filter(
            user=self.request.user)
        context['staff_user_list'] = Ticket.objects.filter(
            assigned_to=self.request.user)

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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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


@login_required
def mark_ticket_as_resolved(request, id):
    if request.method == 'POST':
        comment = request.POST['comment']
        ticket = Ticket.objects.get(id=id)
        user = request.user
        date_time = datetime.datetime.now()
        ticket.resolved_by = user
        ticket.resolved_date = date_time
        ticket.completed_status
        Comment.objects.create(ticket=ticket, user=user, text=comment)
        Ticket.objects.filter(id=id).update(
            completed_status=True, resolved_by=user, resolved_date=date_time)

    return HttpResponseRedirect(reverse("ticketapp:ticket-detail", kwargs={'pk': id}))


@login_required
def mark_ticket_as_unresolved(request, id):
    Ticket.objects.filter(id=id).update(completed_status=False)
    return HttpResponseRedirect(reverse("ticketapp:ticket-detail", kwargs={'pk': id}))


@login_required
def add_comment(request, ticket_id):
    if request.method == 'POST':
        comment = request.POST['comment']
        ticket = Ticket.objects.get(id=ticket_id)
        user = request.user
        date_time = datetime.datetime.now()
        ticket.resolved_by = user
        ticket.resolved_date = date_time
        ticket.completed_status

        Comment.objects.create(ticket=ticket, user=user, text=comment)
        return HttpResponseRedirect(reverse("ticketapp:ticket-detail", kwargs={'pk': ticket_id}))


class SearchResultView(LoginRequiredMixin, generic.ListView):
    model = Ticket
    template_name = 'ticketapp/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Ticket.objects.filter(
            Q(title__icontains=query) | Q(customer_full_name__icontains=query) | Q(
                issue_description__icontains=query)
        ).filter(user=self.request.user)

        return object_list


class StaffSearchResultView(LoginRequiredMixin, generic.ListView):
    model = Ticket
    template_name = 'ticketapp/staff_search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Ticket.objects.filter(
            Q(title__icontains=query) | Q(customer_full_name__icontains=query) | Q(
                issue_description__icontains=query)
        ).filter(assigned_to=self.request.user)

        return object_list


class AllSearchResultView(LoginRequiredMixin, generic.ListView):
    model = Ticket
    template_name = 'ticketapp/staff_search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Ticket.objects.filter(
            Q(title__icontains=query) | Q(customer_full_name__icontains=query) | Q(
                issue_description__icontains=query)
        )

        return object_list
