import json
from myuw.views.api.prev_unfinished_schedule import\
    StudUnfinishedPrevQuarClasSche
from myuw.test.api import MyuwApiTest, require_url, fdao_sws_override,\
    fdao_pws_override


url_name = "myuw_prev_unfinished_schedule"


@fdao_pws_override
@fdao_sws_override
@require_url(url_name)
class TestStudUnfinishedPrevQuarClasSche(MyuwApiTest):

    def get_prev_unfinished_schedule(self, user=None, date=None):
        if user:
            self.set_user(user)
        if date:
            self.set_date(date)
        return self.get_response_by_reverse(url_name)

    def get_section(self, data, abbr, number, section_id):
        for section in data['sections']:
            if section['curriculum_abbr'] == abbr and\
                    section['course_number'] == number and\
                    section['section_id'] == section_id:

                return section

        self.fail('Did not find course %s %s %s' % (abbr, number, section_id))

    def test_404(self):
        response = self.get_prev_unfinished_schedule('javerage')
        self.assertEquals(response.content, 'Data not found')
        self.assertEquals(response.status_code, 404)

    def test_no_prev_terms(self):
        response = self.get_prev_unfinished_schedule('jpce',
                                                     '2013-08-08 00:00:01')
        self.assertEquals(response.content, 'Data not found')
        self.assertEquals(response.status_code, 404)

    def test_one_prev_term(self):
        response = self.get_prev_unfinished_schedule('jpce')
        self.assertEquals(response.status_code, 200)
        ret_data = json.loads(response.content)

        self.assertEquals(len(ret_data), 1)
        data = ret_data[0]
        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Winter')
        self.assertEquals(len(data["sections"]), 2)

        com = self.get_section(data, 'COM', '201', 'A')
        self.assertEquals(com['start_date'], '2013-01-30 00:00:00')
        self.assertEquals(com['end_date'], '2013-04-29 00:00:00')
        self.assertFalse(com["is_ended"])

        psych = self.get_section(data, 'PSYCH', '203', 'A')
        self.assertEquals(psych['start_date'], '2013-01-29 00:00:00')
        self.assertEquals(psych['end_date'], '2013-07-30 00:00:00')
        self.assertFalse(psych["is_ended"])

    def test_two_prev_terms(self):
        response = self.get_prev_unfinished_schedule('jpce',
                                                     '2013-06-24 00:00:01')
        self.assertEquals(response.status_code, 200)
        ret_data = json.loads(response.content)
        self.assertEquals(len(ret_data), 2)

        data = ret_data[0]
        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 2)

        data = ret_data[1]
        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Winter')
        self.assertEquals(len(data["sections"]), 1)
