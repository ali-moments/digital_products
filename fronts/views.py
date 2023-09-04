from django.shortcuts import render

from subscriptions.models import Package

def home_page(request):
    packages = Package.objects.filter(is_enable=True)
    context = {'packages': packages}
    return render(request, 'fronts/home.html', context=context)


def package_detail(request, package_id):
    package = Package.objects.get(pk=package_id)
    context = {'package': package}
    return render(request, 'fronts/package-details.html', context=context)

