import {fetchBuilder, extractData, buildWith} from './model_builder';

const postProccess = (response) => {
    const html = response.data;
    const parser = new DOMParser();
    var data = {};

    const htmlDoc = parser.parseFromString(
        html, 'text/html'
    );

    if(htmlDoc.links[0] !== undefined) {
        data.article_html = htmlDoc.links[0].outerHTML;
    }

    console.log(htmlDoc.links[0].outerHTML);

    return data;
}
const customActions = {
    fetch: fetchBuilder('/api/v1/hx_toolkit/week/', postProccess, 'text'),
};

export default buildWith(
    {customActions},
);
