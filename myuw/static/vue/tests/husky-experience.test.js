import axios from 'axios';
import {mount} from '@vue/test-utils';
import {expectAction} from './helper';
import {statusOptions} from '../vuex/store/model_builder';

import Vuex from 'vuex';
import {createLocalVue} from './helper';
import hx_toolkit from '../vuex/store/hx_toolkit';
import mockList from './mock_data/husky-exp/list.json';

import UwCard from '../components/_templates/card.vue';
import HuskyExp from '../components/husky_experience/husky-exp.vue';

const localVue = createLocalVue(Vuex);
localVue.component('uw-card', UwCard);
jest.mock('axios');

describe('hx_toolkit page content', () => {
  let store;
  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        hx_toolkit,
      },
      state: {
        staticUrl: '/static/',
        user: {
          affiliations: {
            hxt_viewer: true,
          }
        }
      }
    });
  });

  it('Check render', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/hx_toolkit/list/': mockList,
      };
      return Promise.resolve({data: urlData[url]});
    });
    const wrapper = mount(HuskyExp, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBe(true);
    expect(wrapper.vm.hxtViewer).toBe(true);
    expect(wrapper.vm.staticUrl).toBe('/static/');
    expect(wrapper.findAllComponents(UwCard).length).toBe(4);
  });
});
