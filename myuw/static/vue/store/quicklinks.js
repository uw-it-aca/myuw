import axios from 'axios';
import { statusOptions, doNothing, buildWith } from './model_builder';

const customState = {
  value: {
    recentLinks: JSON.parse(document.getElementById('recent_links').innerHTML),
    popularLinks: JSON.parse(document.getElementById('popular_links').innerHTML),
    customLinks: JSON.parse(document.getElementById('custom_links').innerHTML),
    defaultLinks: JSON.parse(document.getElementById('default_links').innerHTML),
  },
  status: statusOptions[0],
}

const customMutations = {
  addLink(state, link) {
    // TODO
  },
  removeLink(state, link) {
    // TODO
  },
  updateLink(state, link) {
    // TODO
  }
}

export default buildWith(
  { customState },
);