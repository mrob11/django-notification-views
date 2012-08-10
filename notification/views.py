from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from notification.mixins import NotifyMixin, NotifyFormMixin


class NotifyDeleteView(DeleteView, NotifyMixin):
    
    cancel_url = None
    template_name = 'notification/base_confirm_delete.html'
    
    def show_valid_flash(self):
        self.valid_message = "<strong>Hooray!</strong> The %s has been deleted successfully." % self.model._meta.verbose_name.title()
        if self.valid_flash:
            messages.add_message(self.request, self.valid_type, self.valid_message)
        
    
    def get_context_data(self, **kwargs):
        context = super(NotifyDeleteView, self).get_context_data(**kwargs)
        context['object_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.get_cancel_url()
        
        return context
    
    def delete(self, request, *args, **kwargs):
        self.show_valid_flash()
        return super(NotifyDeleteView, self).delete(request, *args, **kwargs)
    
    def get_cancel_url(self):
        if self.cancel_url:
            return self.cancel_url
        else:
            raise ImproperlyConfigured("No URL to redirect to. Provide a cancel_url.")


class NotifyCreateView(CreateView, NotifyFormMixin):
    pass


class NotifyUpdateView(UpdateView, NotifyFormMixin):
    pass


