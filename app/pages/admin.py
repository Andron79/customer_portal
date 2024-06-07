from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from pages.models import (
    Information,
    Product,
    Document,
    FAQ,
    File,
    Tutorial
)


class UserContentModelAdmin(admin.ModelAdmin):

    def companies_list(self, obj):
        return ',\n '.join([company.title for company in obj.company.all()])

    companies_list.short_description = _('Companies')

    def products_list(self, obj):
        return ',\n '.join([product.title for product in obj.product.all()])

    products_list.short_description = _('Products')

    def company_types_list(self, obj):
        return ',\n '.join([company_type.title for company_type in obj.company_types.all()])

    company_types_list.short_description = _('Company types')

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)


class InformationInline(admin.TabularInline):
    Information.product.through.__str__ = lambda x: ''
    model = Information.product.through
    extra = 0
    verbose_name = _('Information')
    verbose_name_plural = _('Informations')


class DocumentInline(admin.TabularInline):
    Document.product.through.__str__ = lambda x: ''
    model = Document.product.through
    extra = 0
    verbose_name = _('Document')
    verbose_name_plural = _('Documents')


class FileInline(admin.TabularInline):
    File.product.through.__str__ = lambda x: ''
    model = File.product.through
    extra = 0
    verbose_name = _('File')
    verbose_name_plural = _('Files')


class TutorialInline(admin.TabularInline):
    Tutorial.product.through.__str__ = lambda x: ''
    model = Tutorial.product.through
    extra = 0
    verbose_name = _('Tutorial')
    verbose_name_plural = _('Tutorials')


class FAQInline(admin.TabularInline):
    FAQ.product.through.__str__ = lambda x: ''
    model = FAQ.product.through
    extra = 0
    verbose_name = _('FAQ')
    verbose_name_plural = _('FAQs')


class ProductAdmin(UserContentModelAdmin):
    model = Product
    list_display = ('title', 'company_types_list', 'created_at')
    list_filter = ('company_types__title',)
    list_display_links = ('title',)
    filter_horizontal = ('company_types',)
    inlines = [InformationInline, DocumentInline, FileInline, TutorialInline, FAQInline]
    save_as = True
    save_on_top = True
    save_as_continue = False


class InformationPageAdmin(UserContentModelAdmin):
    model = Information
    list_display = ('title', 'products_list', 'companies_list', 'created_at', 'is_public',)
    list_filter = ('company', 'product', 'is_public')
    empty_value_display = '🚫️'
    filter_horizontal = ('product', 'company',)
    fields = ('title', 'description', 'is_public', 'company', 'product',)
    list_display_links = ('title',)
    list_editable = ('is_public',)
    save_as = True
    save_on_top = True
    save_as_continue = False


class DocumentAdmin(UserContentModelAdmin):
    model = Document
    list_display = (
        'title', 'file_name', 'file_format', 'humanized_file_size', 'products_list', 'companies_list',
        'created_at', 'is_public',
    )
    save_as = True
    save_on_top = True
    list_filter = ('product', 'company', 'is_public')
    filter_horizontal = ('product', 'company',)
    empty_value_display = '🚫️'
    search_fields = ('title',)
    list_display_links = ('title',)
    list_editable = ('is_public',)
    exclude = ('file_size',)

    change_readonly_fields = (
        'file',
        'humanized_file_size',
        'file_format',
        'companies_list',
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(DocumentAdmin, self).get_readonly_fields(request, obj)
        if obj:
            return self.change_readonly_fields
        return readonly_fields

    def has_change_permission(self, request, obj=None):
        return True


class FileAdmin(UserContentModelAdmin):
    model = File
    list_display = (
        'title', 'file_name', 'file_format', 'humanized_file_size', 'products_list', 'companies_list', 'created_at',
    )
    save_as = True
    save_on_top = True
    save_as_continue = False

    list_filter = ('product', 'company',)
    filter_horizontal = ('product', 'company',)
    search_fields = ('title',)
    empty_value_display = '🚫️'
    list_display_links = ('title',)
    exclude = ('is_public', 'file_size',)
    change_readonly_fields = (
        'file',
        'humanized_file_size',
        'file_format',
        'companies_list',
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(FileAdmin, self).get_readonly_fields(request, obj)
        if obj:
            return self.change_readonly_fields
        return readonly_fields


class TutorialAdmin(UserContentModelAdmin):
    model = Tutorial
    list_display = ('title', 'products_list', 'companies_list', 'created_at', 'is_public')
    list_filter = ('company', 'product', 'is_public')
    empty_value_display = '🚫️'
    filter_horizontal = ('product', 'company',)
    list_display_links = ('title',)
    list_editable = ('is_public',)
    save_as = True
    save_on_top = True
    save_as_continue = False


class FAQAdmin(UserContentModelAdmin):
    model = FAQ
    list_display = ('question', 'products_list', 'companies_list', 'created_at', 'is_public')
    list_filter = ('company', 'product', 'is_public')
    empty_value_display = '🚫️'
    filter_horizontal = ('product', 'company',)
    fields = ('question', 'answer', 'is_public', 'company', 'product')
    list_display_links = ('question',)
    list_editable = ('is_public',)
    save_as = True
    save_on_top = True
    save_as_continue = False


admin.site.register(Product, ProductAdmin)
admin.site.register(Information, InformationPageAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(FAQ, FAQAdmin)
