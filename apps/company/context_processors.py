from .models import Company, CompanySocialLink, UsefulLink


def company_processor(request):
    company = Company.objects.last()
    useful_links = UsefulLink.objects.all()
    company_social_links = CompanySocialLink.objects.all()
    return {'company': company,
            'useful_links': useful_links,
            'company_social_links': company_social_links}
