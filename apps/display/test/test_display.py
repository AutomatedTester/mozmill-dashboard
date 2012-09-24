import test_utils


class DisplayResults(test_utils.TestCase):
    
    def test_that_we_can_display_all_results(self):
        response = self.client.get("/en-US/")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 
                                'display/reports/reports.html')
        self.assertEquals(0, len(response.context['reports'].values_list()))

