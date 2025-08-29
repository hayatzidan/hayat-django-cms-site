# from django import template
# from employees.models import LinkedAccount

# register = template.Library()

# @register.inclusion_tag('employees/linked_accounts_list.html', takes_context=True)
# def show_linked_accounts(context, provider):
#     user = context['request'].user
#     if user.is_authenticated:
#         accounts = LinkedAccount.objects.filter(user=user, provider=provider)
#     else:
#         accounts = []
#     return {'accounts': accounts, 'provider': provider}