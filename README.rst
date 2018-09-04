==================
wagtail-exportcsv
==================

wagtail-exportcsv is a simple Django app to export form submission as CSV.

Detailed documentation is in the "docs" directory.

Installation
------------

.. code-block::

    pip install wagtail-exportcsv

    or

    pip install -e git+git@github.com:7aleb/wagtail-exportcsv.git#egg=wagtail_exportcsv_dev

And add ``wagtail_exportcsv`` to ``INSTALLED_APPS``

Quick start
-----------

First, create a resource class to define a CSV export. Then add
``ExportModelAdminMixin`` to your Wagtail ``ModelAdmin`` class. Example:

.. code-block:: python

    from import_export import resources
    from wagtail.contrib.modeladmin.options import ModelAdmin

    class ExampleResource(resources.ModelResource):

        class Meta:
            model = ExampleModel
            fields = ('first_name', 'email',)


    class ExampleAdmin(ExportModelAdminMixin, ModelAdmin):

        model = ExampleModel
        resource_class = ExampleResource
