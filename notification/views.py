from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin, ModelFormMixin


class NotifyMixin(object):
    
    valid_type = messages.SUCCESS
    valid_message = None
    valid_flash = True
    
    invalid_type = messages.ERROR
    invalid_message = None
    invalid_flash = True
    
    notify_list = None
    notify_template = None
    
    def get_valid_message(self):
        if self.valid_message:
            return self.valid_message
        else:
            return "<strong>Hooray!</strong> The %s has been saved successfully." % self.model._meta.verbose_name.title()

    def get_invalid_message(self):
        if self.invalid_message:
            return self.invalid_message
        else:
            return "<strong>Oops!</strong> There was a problem. Please fix the errors below."

    def show_invalid_flash(self):
        if self.invalid_flash:
            messages.add_message(self.request, self.invalid_type, self.get_invalid_message())
            
    def show_valid_flash(self):
        if self.valid_flash:
            messages.add_message(self.request, self.valid_type, self.get_valid_message())

    
class NotifyFormMixin(FormMixin, NotifyMixin):
    
    def form_valid(self, form):
        self.show_valid_flash()
        return super(NotifyFormMixin, self).form_valid(form)
    
    def form_invalid(self, form, **kwargs):
        self.show_invalid_flash()
        return super(NotifyFormMixin, self).form_invalid(form)


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


