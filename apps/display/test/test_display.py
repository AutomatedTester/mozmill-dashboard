import test_utils


class DisplayResults(test_utils.TestCase):
    
    fixtures = ['display_views_testdata.json']

    def test_that_we_can_display_all_results(self):
        response = self.client.get("/en-US/")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 
                                'display/reports/reports.html')
        self.assertEquals(3, len(response.context['reports'].values_list()))

    def test_that_filters_dont_create_500(self):
        response = self.client.get('/en-US/', {'os': 'all', 
                                                'locale':'en-US', 
                                                'to_date': '2012-09-12',
                                                'from_date': '2012-09-14'})
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 
                                'display/reports/reports.html')
        self.assertEquals(0, len(response.context['reports'].values_list()))

    def test_that_we_can_load_a_specific_result(self):
        response = self.client.get("/en-US/report/2")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'display/report/functional.html')
    def test_that_we_can_load_endurance_reports(self):
        response = self.client.get("/en-US/endurance/")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'display/reports/updateReports.html')
    
    def test_that_we_can_load_individual_update_tests(self):
        response = self.client.get("/en-US/report/1")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'display/report/update.html')
