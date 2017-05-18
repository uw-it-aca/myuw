from myuw.views.error import not_instructor_error, data_not_found,\
    invalid_session, invalid_input_data, invalid_method, invalid_future_term,\
    data_error
from myuw.test.api import MyuwApiTest


class TestViewsError(MyuwApiTest):

    def test_data_not_found(self):
        response = data_not_found()
        self.assertEquals(response.content, 'Data not found')
        self.assertEquals(response.status_code, 404)

    def test_not_instructor_error(self):
        response = not_instructor_error()
        self.assertEquals(response.content,
                          'Access Forbidden to Non Instructor')
        self.assertEquals(response.status_code, 403)

    def test_invalid_session(self):
        response = invalid_session()
        self.assertEquals(response.content, 'No valid userid in session')
        self.assertEquals(response.status_code, 400)

    def test_invalid_input_data(self):
        response = invalid_input_data()
        self.assertEquals(response.content, 'Invalid post data content')
        self.assertEquals(response.status_code, 400)

    def test_invalid_method(self):
        response = invalid_method()
        self.assertEquals(response.content, 'Method not allowed')
        self.assertEquals(response.status_code, 405)

    def test_invalid_future_term(self):
        response = invalid_future_term()
        self.assertEquals(response.content, 'Invalid requested future term')
        self.assertEquals(response.status_code, 410)

    def test_data_error(self):
        response = data_error()
        self.assertEquals(response.content,
                          'Data not available due to an error')
        self.assertEquals(response.status_code, 543)
