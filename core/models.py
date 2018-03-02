from django.db import models


class PRCIrun(models.Model):

    pr_number = models.IntegerField()
    pr_date = models.DateTimeField(db_index=True)
    pr_name = models.CharField(max_length=100)
    pr_url = models.CharField(max_length=100)
    run_name = models.CharField(max_length=100)
    run_logs_url = models.CharField(max_length=100)
    run_result = models.CharField(max_length=100)

    # TODO: if completed and add pr_name

    # class Meta:
    #     unique_together = ["pr_number", "pr_url"]

    def __str__(self):
        return '%s/%s' % (self.pr_number, self.pr_name)
