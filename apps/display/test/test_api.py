import test_utils
import json
from display.models import Results, SystemInfo, Addons

class PostResults(test_utils.TestCase):
    

    data = {'application_id': '{ec8030f7-c20a-464f-9b0e-13a3a9e97384}', 'results': [{'passes': [], 'fails': [],
    'passed_function': 'test1.js::setupModule', 'name': 'test1.js::setupModule', 'filename':
    '/var/folders/t1/5wm63z9x4859xl2rykk46ck00000gn/T/tmpGI9w3P.mozmill-tests/tests/update/testDirectUpdate/test1.js',
    'failed': 0, 'passed': 0}, {'passes': [], 'fails': [], 'passed_function': 'test2.js::setupModule', 'name':
    'test2.js::setupModule', 'filename':
    '/var/folders/t1/5wm63z9x4859xl2rykk46ck00000gn/T/tmpGI9w3P.mozmill-tests/tests/update/testDirectUpdate/test2.js',
    'failed': 0, 'passed': 0}, {'passes': [{'function': """: controller.assert('function () {\\n    return
    update.allowed;\\n}')"""}, {'function': 'controller.click()'}, {'function':
    'Controller.assertJSProperty("Selector: #updateButton") : false'}, {'function': 'controller.waitFor()'},
    {'function': 'controller.waitFor()'}, {'function': 'controller.waitFor()'}, {'function': """:controller.assert('function () {\\n    return channel == this.channel;\\n}')"""}, {'function':
    'controller.click()'}, {'function': 'controller.waitFor()'}, {'function': 'controller.waitFor()'},
    {'function': 'controller.waitFor()'}], 'fails': [], 'passed_function': 'test2.js::testDirectUpdate_Download',
    'name': 'test2.js::testDirectUpdate_Download', 'filename':
    '/var/folders/t1/5wm63z9x4859xl2rykk46ck00000gn/T/tmpGI9w3P.mozmill-tests/tests/update/testDirectUpdate/test2.js',
    'failed': 0, 'passed': 11}, {'passes': [], 'fails': [], 'passed_function': 'test2.js::teardownModule',
    'name': 'test2.js::teardownModule', 'filename':
    '/var/folders/t1/5wm63z9x4859xl2rykk46ck00000gn/T/tmpGI9w3P.mozmill-tests/tests/update/testDirectUpdate/test2.js',
    'failed': 0, 'passed': 0}, {'passes': [], 'fails': [], 'passed_function': 'test3.js::setupModule', 'name':
    'test3.js::setupModule', 'filename':
    '/var/folders/t1/5wm63z9x4859xl2rykk46ck00000gn/T/tmpGI9w3P.mozmill-tests/tests/update/testDirectUpdate/test3.js',
    'failed': 0, 'passed': 0}, {'passes': [{'function': 'controller.waitFor()'}, {'function':
    'controller.waitFor()'}, {'function': ": controller.assert('function () {\\n    return check >= 0;\\n}')"},
    {'function': """: controller.assert('function () {\\n    return info.build_post.buildid ===
    info.patch.buildid;\\n}')"""}, {'function': """: controller.assert('function () {\\n    return info.build_post.buildid
    === info.target_buildid;\\n}')"""}, {'function': """: controller.assert('function () {\\n    return
    info.build_post.locale === info.build_pre.locale;\\n}')"""}, {'function': """: controller.assert('function () {\\n
    return info.build_post.disabled_addons === info.build_pre.disabled_addons;\\n}')"""}, {'function':
    'controller.click()'}, {'function': 'Controller.assertJSProperty("Selector: #updateButton") : false'}], 'fails':
    [], 'passed_function': 'test3.js::testDirectUpdate_AppliedAndNoUpdatesFound', 'name':
    'test3.js::testDirectUpdate_AppliedAndNoUpdatesFound', 'filename':
    '/var/folders/t1/5wm63z9x4859xl2rykk46ck00000gn/T/tmpGI9w3P.mozmill-tests/tests/update/testDirectUpdate/test3.js',
    'failed': 0, 'passed': 9}, {'passes': [], 'fails': [], 'passed_function': 'test3.js::teardownModule', 'name':
    'test3.js::teardownModule', 'filename':
    '/var/folders/t1/5wm63z9x4859xl2rykk46ck00000gn/T/tmpGI9w3P.mozmill-tests/tests/update/testDirectUpdate/test3.js',
    'failed': 0, 'passed': 0}], 'report_type': 'firefox-update', 'tests_repository':
    'http://hg.mozilla.org/qa/mozmill-tests', 'tests_changeset': 'b1761bcb17d2', 'time_start':
    '2012-02-03T14:31:58Z', 'application_changeset': 'e777c939a3f9', 'system_info': {'hostname':
    'release8-osx-107.qa.mtv1.mozilla.com.73.250.10.in-addr.arpa', 'service_pack': '', 'system': 'Mac', 'version':
    'OS X 10.7.2', 'bits': '64', 'processor': 'x86_64'}, 'platform_version': '13.0a1', 'tests_passed': 7,
    'application_repository': 'http://hg.mozilla.org/mozilla-central', 'platform_changeset': 'e777c939a3f9',
    'platform_repository': 'http://hg.mozilla.org/mozilla-central', 'tests_failed': 0, 'time_end':
    '2012-02-03T14:32:35Z', 'application_locale': 'en-US', 'platform_buildid': '20120203031138',
    'application_version': '13.0a1', 'tests_skipped': 0, 'time_upload': '2012-02-03T14:32:35Z',
    'application_name': 'Firefox', 'mozmill_version': '1.5.8', 'addons': [{'name': 'jsbridge', 'isCompatible':
    True, 'version': '2.4.8', 'type': 'extension', 'id': 'jsbridge@mozilla.com', 'isActive': True}, {'name':
    'MozMill', 'isCompatible': True, 'version': '1.5.8', 'type': 'extension', 'id': 'mozmill@mozilla.com',
    'isActive': True}, {'name': 'Default', 'isCompatible': True, 'version': '13.0a1', 'type': 'theme', 'id':
    '{972ce4c6-7e08-4474-a285-3208198ce6fd}', 'isActive': True}, {'name': 'QuickTime Plug-in 7.7.1',
    'isCompatible': True, 'version': '7.7.1', 'type': 'plugin', 'id': '{d95f2237-07c7-b389-7956-65e6f1ce8e0a}',
    'isActive': True}, {'name': 'Java Applet Plug-in', 'isCompatible': True, 'version': '14.1.0', 'type':
    'plugin', 'id': '{07b90314-1e79-c84a-4b47-fb7e1853be39}', 'isActive': True}], 'updates': [{'build_pre':
    {'disabled_addons': '', 'buildid': '20120202031238', 'locale': 'en-US', 'version': '13.0a1', 'user_agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0a1) Gecko/20120202 Firefox/13.0a1', 'url_aus':
    'https://aus3.mozilla.org/update/3/Firefox/13.0a1/20120202031238/Darwin_x86_64-gcc3-u-i386-x86_64/en-US/nightly/Darwin%2011.2.0/default/default/update.xml?force=1'},
    'success': True, 'patch': {'url_mirror':
    'http://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/2012/02/2012-02-03-03-11-38-mozilla-central/firefox-13.0a1.en-US.mac.partial.20120202031238-20120203031138.mar',
    'buildid': '20120203031138', 'download_duration': 675, 'type': 'minor', 'is_complete': False, 'channel':
    'nightly', 'size': 5606743}, 'target_buildid': '20120203031138', 'fallback': False, 'build_post':
    {'disabled_addons': '', 'buildid': '20120203031138', 'locale': 'en-US', 'version': '13.0a1', 'user_agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0a1) Gecko/20120203 Firefox/13.0a1', 'url_aus':
    'https://aus3.mozilla.org/update/3/Firefox/13.0a1/20120203031138/Darwin_x86_64-gcc3-u-i386-x86_64/en-US/nightly/Darwin%2011.2.0/default/default/update.xml?force=1'}}],
    'report_version': '1.0'}
    
    def test_we_can_post_results_to_a_database(self):
        
        response = self.client.post("/en-US/report/", json.dumps(self.data),content_type="application/json" )
        self.assertEqual(200, response.status_code)
        self.assertEqual("Hello World", response.content)
        self.assertEqual(1, len(SystemInfo.objects.values()))
        self.assertEqual(1, len(Results.objects.values()))
        self.assertEqual(5, len(Addons.objects.values()))
