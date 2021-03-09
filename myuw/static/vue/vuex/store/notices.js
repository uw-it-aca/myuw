import axios from 'axios';
import {fetchBuilder, buildWith} from './model_builder';
import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/timezone'))

const postProcess = (response, _, rootState) => {
  const notices = response.data;

  const parser = new DOMParser();
  return notices.map((notice) => {
    if (notice.notice_content.includes('notice-title')) {
      const noticeContent = notice.notice_content;

      // Split the notice_content into notice_body and notice_title
      if (noticeContent.includes('&nbsp')) {
        const parts = noticeContent.split('&nbsp');
        notice.notice_title = parts[0];
        notice.notice_body = parts[1];
        if (notice.notice_body[0] === ';') {
          notice.notice_body = notice.notice_body.slice(1);
        }
      } else {
        const htmlDoc = parser.parseFromString(
            noticeContent, 'text/html',
        );

        notice.notice_title = htmlDoc.getElementsByClassName('notice-title')[0].outerHTML;
        htmlDoc.body.removeChild(htmlDoc.getElementsByClassName('notice-title')[0]);
        notice.notice_body = htmlDoc.body.innerHTML;
      }
    }

    // Build dates for the notices
    const dateAttr = notice.attributes.find(
        (attr) => (attr.name == 'Date'),
    );
    const startDateAttr = notice.attributes.find(
        (attr) => (attr.name == 'DisplayBegin'),
    );
    // datetime will reflect BOF
    if (startDateAttr !== undefined && startDateAttr.value !== undefined) {
      notice.startDate = dayjs.utc(startDateAttr.value);
    }
    if (dateAttr !== undefined && dateAttr.value !== undefined) {
      notice.date = dayjs.utc(dateAttr.value);
      notice.formattedDate = dateAttr.formatted_value;
    }
    // Notices will be sorted by notice.sortDate
    // some notice only has DisplayBegin date
    notice.sortDate = notice.startDate ? notice.startDate : (
      notice.date ? notice.date : null
    );
    return notice;
  });
};

const customGetters = {
  hasRegisterNotices: (state) => {
    return state.value.filter(
        (notice) => notice.location_tags.includes('checklist_no_orient') ||
          notice.location_tags.includes('checklist_orient_after') ||
          notice.location_tags.includes('checklist_iss_before') ||
          notice.location_tags.includes('checklist_iss_after') ||
          notice.location_tags.includes('checklist_measles_before') ||
          notice.location_tags.includes('checklist_measles_after') ||
          notice.location_tags.includes('checklist_orient_before'),
    ).length > 0;
  },
}

const customMutations = {
  setReadTrue(state, notice) {
    notice.is_read = true;
  },
};

const customActions = {
  setRead: ({commit, rootState}, notice) => {
    axios.put('/api/v1/notices/', {
      'notice_hashes': [notice.id_hash],
    }, {
      headers: {
        'X-CSRFToken': rootState.csrfToken,
      },
    }).then(() => commit('setReadTrue', notice)).catch(() => {});
  },
  setReadNoUpdate: ({rootState}, notice) => {
    axios.put('/api/v1/notices/', {
      'notice_hashes': [notice.id_hash],
    }, {
      headers: {
        'X-CSRFToken': rootState.csrfToken,
      },
    });
  },
  fetch: fetchBuilder('/api/v1/notices/', postProcess, 'json'),
};

export default buildWith(
  {customMutations, customGetters, customActions},
);
