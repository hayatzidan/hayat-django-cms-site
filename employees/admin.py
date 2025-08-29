from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Creator


class EmployeeNameFilter(admin.SimpleListFilter):
    title = "Employee Name"  # Title shown in the admin filter section
    parameter_name = "employee_name"  # URL parameter used for filtering

    def lookups(self, request, model_admin):
        """Returns a list of employees as filter options"""
        employees = Employee.objects.all()
        return [(f"{emp.first_name} {emp.last_name}", f"{emp.first_name} {emp.last_name}") for emp in employees]

    def queryset(self, request, queryset):
        """Filters the employee table based on selection"""
        if self.value():
            first_name, last_name = self.value().split(" ", 1)  # Split first and last name
            return queryset.filter(first_name=first_name, last_name=last_name)
        return queryset  # Return all employees if no filter is applied

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')  # Display first and last names
    search_fields = ('first_name', 'last_name')  # Enable search
    ordering = ('first_name',)  # Order by first name
    list_filter = (EmployeeNameFilter,)  # Add the custom filter

admin.site.register(Employee, EmployeeAdmin)

@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']
    list_filter = ['category']

    