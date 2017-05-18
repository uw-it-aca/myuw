from django.db import models


class ResCategoryLink(models.Model):
    ALL = "all"
    UGRAD = 'ugrad'
    GRAD = 'grad'
    PCE = 'pce'
    FYP = 'fyp'
    SEATTLE = 'seattle'
    BOTHELL = 'bothell'
    TACOMA = 'tacoma'

    url = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    affiliation = models.CharField(max_length=80, null=True)
    pce = models.NullBooleanField()
    campus = models.CharField(max_length=8, null=True)
    category_id = models.CharField(max_length=80)
    category_name = models.CharField(max_length=80)
    sub_category = models.CharField(max_length=80)
    new_tab = models.BooleanField(default=False)

    def category_id_matched(self, acategory_id):
        return self.category_id == acategory_id

    def all_affiliation(self):
        return self.affiliation == ResCategoryLink.ALL

    def for_undergrad(self):
        return self.affiliation == ResCategoryLink.UGRAD

    def for_grad(self):
        return self.affiliation == ResCategoryLink.GRAD

    def for_pce(self):
        return self.affiliation == ResCategoryLink.PCE

    def for_fyp(self):
        return self.affiliation == ResCategoryLink.FYP

    def campus_matched(self, acampus):
        return (self.for_all_campus() or
                acampus is not None and self.campus == acampus.lower())

    def for_sea_campus(self):
        return self.campus == ResCategoryLink.SEATTLE

    def for_bot_campus(self):
        return self.campus == ResCategoryLink.BOTHELL

    def for_tac_campus(self):
        return self.campus == ResCategoryLink.TACOMA

    def for_all_campus(self):
        return self.campus is None

    def json_data(self):
        data = {
            "title": self.title,
            "url": self.url,
            "new_tab": self.new_tab
        }
        return data

    def set_category_id(self, category_name):
        category_id = category_name.lower()
        category_id = "".join(c for c in category_id if c.isalpha())
        self.category_id = category_id

    class Meta:
        db_table = "myuw_res_category_links"
