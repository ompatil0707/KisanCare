from services.schemes_service import GovernmentSchemesService

svc = GovernmentSchemesService()
scheme = svc.get_scheme_by_id('subsidy-seeds', 'en')
print('✅ Seed Subsidy scheme updated')
print('Website:', scheme['website'])
