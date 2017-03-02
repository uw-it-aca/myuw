import json
from myuw.test.api import MyuwApiTest, require_url, fdao_bookstore_override


VERBACOMPARE_URL_PREFIX = 'http://uw-seattle.verbacompare.com'
IMAGE_URL_PREFIX = 'www7.bookstore.washington.edu/MyUWImage.taf'


@fdao_bookstore_override
@require_url('myuw_current_book')
class TestApiCurBooks(MyuwApiTest):

    def test_javerage_cur_term_books(self):
        self.set_user('javerage')
        response = self.get_response_by_reverse('myuw_current_book')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data["13833"]), 1)
        self.assertEquals(
            data["verba_link"],
            "%s/m?section_id=AB12345&quarter=spring" % VERBACOMPARE_URL_PREFIX)
        book = data['18532'][0]
        self.assertEquals(len(book["authors"]), 1)
        self.assertTrue(book["is_required"])
        self.assertIsNone(book["price"])
        self.assertIsNone(book["used_price"])
        self.assertEquals(book["isbn"], '9780878935970')
        self.assertEquals(book["notes"], 'required')
        self.assertEquals(
            book["cover_image_url"],
            ("%s?isbn=9780878935970&key=46c9ef715edb2ec69517e2c8e6ec9c18" %
             IMAGE_URL_PREFIX))

    def test_eight_cur_term_books(self):
        self.set_user('eight')
        response = self.get_response_by_reverse('myuw_current_book')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data["11646"]), 1)
        book = data['11646'][0]
        self.assertIsNone(book["cover_image_url"])
        self.assertEquals(len(book["authors"]), 1)
        self.assertTrue(book["is_required"])
        self.assertEquals(book["price"], 45.0)
        self.assertIsNone(book["used_price"])
        self.assertEquals(book["isbn"], "9780521600491")
        self.assertEquals(book["notes"], 'required')
