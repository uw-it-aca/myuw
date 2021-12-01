import {fetchBuilder, buildWith} from './model_builder';

const handeWeekParam = (data) => {
  const processed = {};

  const parser = new DOMParser();
  const htmlDoc = parser.parseFromString(
    data, 'text/html',
  );

  if (htmlDoc.getElementsByTagName('a')[0]) {
    processed.expLink =
      htmlDoc.getElementsByTagName('a')[0].href;
  }

  if (htmlDoc.getElementsByClassName('myuw-card-image-full')[0]) {
    processed.srcset = htmlDoc.getElementsByClassName(
      'myuw-card-image-full'
    )[0].srcset;
    processed.src = htmlDoc.getElementsByClassName(
      'myuw-card-image-full'
    )[0].src;
    processed.alt = htmlDoc.getElementsByClassName(
      'myuw-card-image-full'
    )[0].alt;
  }

  if (htmlDoc.getElementsByClassName('myuw-highlight')[0]) {
    processed.articleTeaserTitle = 
      htmlDoc.getElementsByClassName('myuw-highlight')[0].innerHTML;
  }

  if (htmlDoc.getElementsByClassName('myuw-highlight')[1]) {
    processed.articleTeaserBody = 
      htmlDoc.getElementsByClassName('myuw-highlight')[1].textContent;
    if (htmlDoc.getElementsByClassName('myuw-highlight')[1].children[0]) {
      processed.articleFaClass = htmlDoc.getElementsByClassName(
        'myuw-highlight'
      )[1].children[0].classList[1].slice(3);
    }
  }

  return processed;
}

const postProccess = (response, urlExtra) => {
  let proccessValue = {};

  if (urlExtra === 'week/') {
    proccessValue[urlExtra] = handeWeekParam(response.data);
  } else {
    proccessValue[urlExtra] = response.data;
  }

  return proccessValue;
}

const customActions = {
  fetch: fetchBuilder('/api/v1/hx_toolkit/', postProccess, 'text'),
};

export default buildWith(
  {customActions},
);
