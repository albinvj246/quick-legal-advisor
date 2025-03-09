
from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# from Crime.models import Criminals, Feedback, UserReg, PoliceReg, fir_reg
from law.models import Lawyer, Appointment, Client, Ask, Feedback


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'user/user_index.html'
    login_url = '/'

class ViewLaw(LoginRequiredMixin,TemplateView):
    template_name = 'user/view_law.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(ViewLaw,self).get_context_data(**kwargs)
        l = Lawyer.objects.filter(user__last_name='1',user__is_staff='0')
        context['l'] =  l
        return context


class ViewLawDe(LoginRequiredMixin,TemplateView):
    template_name = 'user/law_details.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(ViewLawDe,self).get_context_data(**kwargs)
        id = self.request.GET['id']
        l = Lawyer.objects.filter(pk=id)
        context['l'] =  l
        return context

class Appoinments(LoginRequiredMixin,TemplateView):
    template_name = 'user/appoinment.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(Appoinments,self).get_context_data(**kwargs)
        id = self.request.GET['id']

        context['id'] =  id
        return context

    def post(self, request, *args, **kwargs):
        lawyer = request.POST['lawyer']
        reason = request.POST['reason']


        l = Lawyer.objects.get(pk=lawyer)

        c = Client.objects.get(user_id=self.request.user.id)

        b = Appointment()

        b.reason = reason
        b.status = 'Sent'
        b.client = c
        b.lawyer = l
        b.save()

        messages = "Appointment Successfully"
        return render(request, 'user/user_index.html', {'message': messages})


class ViewAppoinments(LoginRequiredMixin,TemplateView):
    template_name = 'user/my_appointment.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(ViewAppoinments,self).get_context_data(**kwargs)
        l = Appointment.objects.filter(client__user_id=self.request.user.id)

        context['l'] =  l
        return context




class MyLawyer(LoginRequiredMixin,TemplateView):
    template_name = 'user/my_lawyer.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(MyLawyer,self).get_context_data(**kwargs)
        l = Appointment.objects.filter(client__user_id=self.request.user.id,status='Myclient')

        context['l'] =  l
        return context

class MessageDetails(LoginRequiredMixin, TemplateView):
    template_name = 'user/message.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(MessageDetails, self).get_context_data(**kwargs)
        l = Ask.objects.filter(client__user_id=self.request.user.id)
        context['l'] = l
        return context
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        reply = request.POST['reply']
        ask = request.POST['ask']

        b = Ask.objects.get(pk=ask)

        b.status = reply
        b.file = file
        b.save()

        messages = "Upload Successfully"
        return render(request, 'user/user_index.html', {'message': messages})

class FeedbackSug(LoginRequiredMixin,TemplateView):
    template_name = 'user/feed.html'
    login_url = '/'

    def post(self, request, *args, **kwargs):

        feed = request.POST['feed']

        c = Client.objects.get(user_id=self.request.user.id)
        b = Feedback()

        b.feed = feed
        b.client = c
        b.save()

        messages = "sent Successfully"
        return render(request, 'user/user_index.html', {'message': messages})