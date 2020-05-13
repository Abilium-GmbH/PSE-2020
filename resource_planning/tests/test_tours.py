import odoo.tests


@odoo.tests.common.at_install(False)
@odoo.tests.common.post_install(True)
class TestTours(odoo.tests.HttpCase):
    def test_tour_create(self):
        self.browser_js("/web",
                        "odoo.__DEBUG__.services['web_tour.tour'].run('tour_test_create')",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.tour_test_create.ready",
                        login="admin")

    def test_tour_navigation(self):
        self.browser_js("/web",
                        "odoo.__DEBUG__.services['web_tour.tour'].run('tour_test_navigation')",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.tour_test_navigation.ready",
                        login="admin")
