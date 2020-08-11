import axios from 'axios';
import { buildWith } from './model-builder';

const postProcess = (respose) => {
  const notices = respose.data;

  const parser = new DOMParser();
  return notices.map(notice => {
    // Split the notice_content into notice_body and notice_title
    if (notice.notice_content.includes('&nbsp')) {
      const parts = notice.notice_content.split('&nbsp');
      notice.notice_title = parts[0];
      notice.notice_body = parts[1];
      if (notice.notice_body[0] === ';') {
        notice.notice_body = notice.notice_body.slice(1)
      }
    } else {
      const htmlDoc = parser.parseFromString(notice.notice_content, 'text/html');
      if (htmlDoc.getElementsByClassName('notice-title')[0] !== undefined) {
        notice.notice_title = htmlDoc.getElementsByClassName('notice-title')[0].outerHTML;
      }
      if (htmlDoc.getElementsByClassName('notice-body-with-title')[0] !== undefined) {
        notice.notice_body = htmlDoc.getElementsByClassName('notice-body-with-title')[0].outerHTML;
      }
    }
    
    // Build dates for the notices
    const dateFiled = notice.attributes.find(attr => (attr.name == 'StartDate' || attr.name == 'Date'));
    if (dateFiled !== undefined) {
      const parts = dateFiled.value.split("-");

      notice.date = new Date(parts[0], parts[1]-1, parts[2]);
    } else {
      notice.date = new Date();
    }

    return notice;
  })
};

const custom_mutations = {
  setRead(state, notice) {
    notice.is_read = true;
  }
}

const custom_actions = {
  setRead({commit, rootState}, notice) {
    axios.put("/api/v1/notices/",{
        "notice_hashes": [notice.id_hash]
      }, {
        headers: {
          'X-CSRFToken': rootState.csrfToken,
        }
      }).then(() => commit('setRead', notice)).catch(() => {});
  }
}

export default buildWith(
  "/api/v1/notices/",
  postProcess,
  {custom_mutations, custom_actions}
);