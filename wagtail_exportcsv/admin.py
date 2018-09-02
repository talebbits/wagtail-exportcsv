from wagtail.core import hooks
from django.utils.html import format_html
from wagtail.contrib.modeladmin.options import (ModelAdmin,
                                                modeladmin_register)
from wagtail.contrib.modeladmin.options import (ModelAdmin,
                                                ModelAdminGroup,
                                                modeladmin_register)
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from wagtail.contrib.modeladmin.views import IndexView
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from import_export.resources import modelresource_factory
from import_export.formats.base_formats import CSV
from datetime import datetime


class ExportButtonHelper(ButtonHelper):
    """
    This helper constructs all the necessary attributes to create a button.

    There is a lot of boilerplate just for the classnames to be right :(
    """

    export_button_classnames = ['icon', 'icon-download']

    def export_button(self, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []

        classnames = self.export_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        text = _('Export {}'.format(self.verbose_name_plural.title()))

        return {
            'url': self.url_helper.get_action_url('export', query_params=self.request.GET),
            'label': text,
            'classname': cn,
            'title': text,
        }


class ExportAdminURLHelper(AdminURLHelper):
    """
    This helper constructs the different urls.

    This is mostly just to overwrite the default behaviour
    which consider any action other than 'create', 'choose_parent' and 'index'
    as `object specific` and will try to add the object PK to the url
    which is not what we want for the `export` option.

    In addition, it appends the filters to the action.
    """

    non_object_specific_actions = ('create', 'choose_parent', 'index', 'export')

    def get_action_url(self, action, *args, **kwargs):
        query_params = kwargs.pop('query_params', None)

        url_name = self.get_action_url_name(action)
        if action in self.non_object_specific_actions:
            url = reverse(url_name)
        else:
            url = reverse(url_name, args=args, kwargs=kwargs)

        if query_params:
            url += '?{params}'.format(params=query_params.urlencode())

        return url

    def get_action_url_pattern(self, action):
        if action in self.non_object_specific_actions:
            return self._get_action_url_pattern(action)

        return self._get_object_specific_action_url_pattern(action)


class ExportView(IndexView):
    """
    A Class Based View which will generate CSV
    """
    resource_class = None
    def __init__(self, model_admin, resource_class=None):
        self.resource_class = resource_class
        super().__init__(model_admin)

    def get_resource_kwargs(self, request, *args, **kwargs):
        return {}

    def get_export_resource_kwargs(self, request, *args, **kwargs):
        return self.get_resource_kwargs(request, *args, **kwargs)

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model)
        else:
            return self.resource_class

    def get_export_resource_class(self):
        """
        Returns ResourceClass to use for export.
        """
        return self.get_resource_class()

    def get_export_data(self, file_format, queryset, *args, **kwargs):
        request = kwargs.pop("request")
        resource_class = self.get_export_resource_class()
        data = resource_class(**self.get_export_resource_kwargs(request)).export(queryset, *args, **kwargs)
        export_data = file_format.export_data(data)
        return export_data

    def get_export_filename(self, file_format):
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = "%s-%s.%s" % (self.model.__name__,
                                 date_str,
                                 file_format.get_extension())
        return filename


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        queryset = self.queryset.all()
        file_format = CSV()
        export_data = self.get_export_data(file_format, queryset, request=request)
        # return a CSV instead
        content_type = file_format.get_content_type()
        response = HttpResponse(export_data, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % (
                self.get_export_filename(file_format),
            )
        return response


class ExportModelAdminMixin(object):
    """
    A mixin to add to your model admin which hooks the different helpers, the view and register the new urls.
    """

    button_helper_class = ExportButtonHelper
    url_helper_class = ExportAdminURLHelper

    export_view_class = ExportView
    index_template_name = 'wagtail_exportcsv/exportcsv.html'
    
    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls += (
            url(
                self.url_helper.get_action_url_pattern('export'),
                self.export_view,
                name=self.url_helper.get_action_url_name('export')
            ),
        )

        return urls

    def export_view(self, request):
        
        kwargs = {'model_admin': self, 'resource_class': self.resource_class}
        view_class = self.export_view_class
        return view_class.as_view(**kwargs)(request)


