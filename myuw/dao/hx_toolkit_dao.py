from hx_toolkit.file_dao import get_rendered_article_by_id


def get_article_html(article_id):
    html = get_rendered_article_by_id(article_id)
    return html
