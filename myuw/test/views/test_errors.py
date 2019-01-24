from myuw.views.error import not_instructor_error, data_not_found,\
    unknown_uwnetid, invalid_input_data, invalid_method, invalid_future_term,\
    data_error
from myuw.test.api import MyuwApiTest


class TestViewsError(MyuwApiTest):

    def test_data_not_found(self):
        response = data_not_found()
        self.assertEquals(response.content, b'Data not found')
        self.assertEquals(response.status_code, 404)

    def test_not_instructor_error(self):
        response = not_instructor_error()
        self.assertEquals(response.content,
                          b'Access Forbidden to Non Instructor')
        self.assertEquals(response.status_code, 403)

    def test_unknown_uwnetid(self):
        response = unknown_uwnetid()
        self.assertEquals(
            response.content,
            (b'MyUW cannot find data for this user account '
             b'in the person registry services. '
             b'If you have just created your UW NetID, '
             b'please try signing in to MyUW again in one hour.'))
        self.assertEquals(response.status_code, 400)

    def test_invalid_input_data(self):
        response = invalid_input_data()
        self.assertEquals(response.content, b'Invalid post data content')
        self.assertEquals(response.status_code, 400)

    def test_invalid_method(self):
        response = invalid_method()
        self.assertEquals(response.content, b'Method not allowed')
        self.assertEquals(response.status_code, 405)

    def test_invalid_future_term(self):
        response = invalid_future_term("2013,spring")
        self.assertEquals(response.content,
                          b'Invalid requested future term 2013,spring')
        self.assertEquals(response.status_code, 410)

    def test_data_error(self):
        response = data_error()
        self.assertEquals(response.content,
                          b'Data not available due to an error')
        self.assertEquals(response.status_code, 543)
