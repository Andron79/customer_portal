from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import customer_portal
from customer_dashboard.models import Company, CompanyType

admin.site.index_title = _("Customer Portal {}").format(customer_portal.__version__)


class CustomModelViewAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)


class CompanyAdmin(CustomModelViewAdmin):
    model = Company
    list_display = (
        'title',
        'inn',
        'kpp',
        'company_type',
        'current_users_count',
        'max_num_company_users',
        'updated_at',
        'created_at',
    )
    empty_value_display = '🚫️'
    search_fields = ('title', 'inn', 'kpp')
    list_editable = (
        'company_type',
        'max_num_company_users'
    )
    save_as = True
    save_on_top = True
    save_as_continue = False

    def get_queryset(self, request):
        return super(CompanyAdmin, self).get_queryset(request).select_related('company_type')

    @admin.display(description=_('Company type'))
    def company_type(self, obj):
        return obj.company_types

    @admin.display(description=_('Current number of users'))
    def current_users_count(self, obj):
        return obj.userprofile_set.filter(company=obj).count()


class CompanyTypeAdmin(CustomModelViewAdmin):
    model = CompanyType
    list_display = (
        'title',
        'company_count',
        'companies_list'
    )
    list_filter = ('title',)
    search_fields = ('title',)
    empty_value_display = '🚫️'
    readonly_fields = ('company_count', 'companies_list')
    save_as = False
    save_on_top = True
    save_as_continue = False

    @admin.display(description=_('Company count'))
    def company_count(self, obj):
        return obj.companies.filter(company_type=obj).count()

    @admin.display(description=_('Companies'))
    def companies_list(self, obj):
        return ',\n '.join([company.title for company in obj.companies.all()])


admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyType, CompanyTypeAdmin)
