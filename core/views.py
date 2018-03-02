from django.shortcuts import render
from django.views.generic import View
from collections import namedtuple
from core.models import PRCIrun


class HomeView(View):
    def get(self, request):
        pr_data = []
        pr_cont = namedtuple('PR', 'pr_number pr_name runs')
        pr_list = list(PRCIrun.objects.values_list('pr_number', flat=True).distinct())

        # TODO: could be done better
        for pr in pr_list:
            runs = PRCIrun.objects.filter(pr_number=pr)
            pr_name = runs.values_list('pr_name', flat=True).distinct()[0]
            pr_data.append(pr_cont(pr, pr_name, runs))

        return render(request, 'prci_dash_home.html', {'pr_details': pr_data})
