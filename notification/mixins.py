from django.contrib import messages
from django.views.generic.edit import FormMixin

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
            return "<strong>Success:</strong> The %s has been saved." % self.model._meta.verbose_name.title()

    def get_invalid_message(self):
        if self.invalid_message:
            return self.invalid_message
        else:
            return "<strong>Failed:</strong> There was a problem. Please fix the errors below."

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
