import {fetchBuilder, extractData, buildWith} from './model_builder';

const postProccess = (response, urlExtra) => {
  let proccessValue = {};
  proccessValue[urlExtra] = {};

  const parser = new DOMParser();
  const htmlDoc = parser.parseFromString(
    response.data, 'text/html',
  );

  if (htmlDoc.getElementsByTagName('a')[0]) {
    proccessValue[urlExtra].expLink =
      htmlDoc.getElementsByTagName('a')[0].href;
  }

  if (htmlDoc.getElementsByClassName('myuw-card-image-full')[0]) {
    proccessValue[urlExtra].srcset = htmlDoc.getElementsByClassName(
      'myuw-card-image-full'
    )[0].srcset;
    proccessValue[urlExtra].src = htmlDoc.getElementsByClassName(
      'myuw-card-image-full'
    )[0].src;
    proccessValue[urlExtra].alt = htmlDoc.getElementsByClassName(
      'myuw-card-image-full'
    )[0].alt;
  }

  if (htmlDoc.getElementsByClassName('myuw-highlight')[0]) {
    proccessValue[urlExtra].articleTeaserTitle = 
      htmlDoc.getElementsByClassName('myuw-highlight')[0].innerHTML;
  }

  if (htmlDoc.getElementsByClassName('myuw-highlight')[1]) {
    proccessValue[urlExtra].articleTeaserBody = 
      htmlDoc.getElementsByClassName('myuw-highlight')[1].textContent;
    if (htmlDoc.getElementsByClassName('myuw-highlight')[1].children[0]) {
      proccessValue[urlExtra].articleFaClass = htmlDoc.getElementsByClassName(
        'myuw-highlight'
      )[1].children[0].classList[1].slice(3);
    }
  }

  return proccessValue;
}

const customActions = {
  fetch: fetchBuilder('/api/v1/hx_toolkit/', postProccess, 'text'),
};

export default buildWith(
  {customActions},
);
