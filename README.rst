==================
wagtail-exportcsv
==================

wagtail=exportcsv is a simple Django app to export form submission as CSV.

Detailed documentation is in the "docs" directory.

Quick start
-----------

.. code-block:: python

    from import_export import resources

    class ExampleResource(resources.ModelResource):
        class Meta:
            model = ExampleModel
            fields = ('first_name', 'email',)


    class ExampleAdmin(ExportModelAdminMixin, ModelAdmin):

        model = ExampleModel
        resource_class = ExampleResource
