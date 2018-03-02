import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from core.models import PRCIrun
from django.db import IntegrityError

# BeautifulSoup constants
PR_URL_REQ = 'html_url'

PR_NAME_CLS = 'js-issue-title'
PR_DATE_TAG = 'relative-time'

RUNS_LIST = 'merge-status-list'
RUN_ATTRS = 'merge-status-item d-flex flex-items-baseline'
RUN_NAME = 'strong'
RUN_RESULT_TAG = 'svg'
RUN_PASS = 'text-green'
RUN_LOGS_URL = 'status-actions'


def pr_to_db(data):
    prci_run = PRCIrun()
    prci_run.pr_number = data['pr_number']
    prci_run.pr_name = data['pr_name']
    prci_run.pr_date = data['pr_date']
    prci_run.pr_url = data['pr_url']
    prci_run.run_name = data['run_name']
    prci_run.run_logs_url = data['run_logs_url']
    prci_run.run_result = data['run_result']
    try:
        prci_run.save()
    except IntegrityError:
        print('Exists?')
        pass


def process_pr(url):
    data = {}
    text = requests.get(url).text
    soup = BeautifulSoup(text, 'lxml')

    data['pr_number'] = url.split('/')[-1]
    data['pr_name'] = soup.find('span', {"class": PR_NAME_CLS}).text.strip()
    data['pr_date'] = soup.find(PR_DATE_TAG)['datetime']
    data['pr_url'] = url

    for item in soup.findAll(attrs={'class': RUNS_LIST}):
        for x in item.findAll(attrs={'class': RUN_ATTRS}):
            data['run_name'] = x.find(RUN_NAME).text.strip()
            data['run_result'] = 'FAIL' if RUN_PASS not in x.find(RUN_RESULT_TAG)['class'] else 'PASS'
            try:
                data['run_logs_url'] = x.find("a", {"class": RUN_LOGS_URL})['href']
            except TypeError:
                data['run_logs_url'] = 'N/A'
                data['run_result'] = 'ERR'

            pr_to_db(data)


class Command(BaseCommand):
    help = "Poll GH PRs"

    def handle(self, *args, **options):
        last30pr = requests.get('https://api.github.com/repos/freeipa/freeipa/pulls').json()

        for pr in last30pr:
            print('processing:',pr[PR_URL_REQ])
            process_pr(pr[PR_URL_REQ])
