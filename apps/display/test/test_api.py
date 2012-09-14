import test_utils
import json
from display.models import Results

class PostResults(test_utils.TestCase):
    
    def test_we_can_post_results_to_a_database(self):
        
        data = {"_id" : 1, "report_type": 'firefox-update',"time_upload":"2012-02-03T14:32:35Z",
                "results": [{ "failed": 0,"name": "foo"}]}
        response = self.client.post("/en-US/report/", json.dumps(data),content_type="application/json" )
        self.assertEqual(200, response.status_code)
        self.assertEqual("Hello World", response.content)
        self.assertEqual(1, len(Results.objects.values()))

