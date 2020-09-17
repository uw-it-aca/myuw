import axios from 'axios';
import {mount, shallowMount, createLocalVue} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import Link from '../components/index/cards/quicklinks/link.vue';
import Quicklinks from '../components/index/cards/quicklinks/quicklinks.vue';

import mockQuicklinks from './mock_data/quicklinks.json';

import {library} from '@fortawesome/fontawesome-svg-core';
import {
  FontAwesomeIcon,
  FontAwesomeLayers,
} from '@fortawesome/vue-fontawesome';

import {
  faExclamationTriangle,
  faPencilAlt,
  faTimes,
  faPlus,
} from '@fortawesome/free-solid-svg-icons';

const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(Vuex);

library.add(faExclamationTriangle);
library.add(faPencilAlt);
library.add(faTimes);
library.add(faPlus);

localVue.component('font-awesome-icon', FontAwesomeIcon);
localVue.component('font-awesome-layers', FontAwesomeLayers);

jest.mock('axios');

function elementBuilder(id) {
  const elm = document.createElement('script');
  elm.id = id;
  elm.innerHTML = JSON.stringify(mockQuicklinks[id]);

  return elm;
}

const documentSpy = jest.spyOn(document, 'getElementById');

const mockElements = {
  'popular_links': elementBuilder('popular_links'),
  'recent_links': elementBuilder('recent_links'),
  'custom_links': elementBuilder('custom_links'),
  'default_links': elementBuilder('default_links'),
};
documentSpy.mockImplementation((id) => mockElements[id]);

describe('Quicklinks/Link', () => {
  let store;
  let quicklinks = jest.requireActual('../store/quicklinks')['default'];

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        quicklinks: {
          ...quicklinks
        },
      },
      state: {
        csrfToken: "dfsdfsgfsdg",
      },
    });
  });

  it('Basic Mount', () => {
    const wrapper = shallowMount(Quicklinks, {store, localVue});
    expect(wrapper.find('h3').text()).toEqual('Quick Links');

    expect(wrapper.findAllComponents(Link)).toHaveLength(mockQuicklinks['default_links'].length);
  });

  it('Add link', async () => {
    const mockQuicklinksCopy = JSON.parse(JSON.stringify(mockQuicklinks));
    const newCustomLink = {
      url: "http://test.com",
      label: "test",
    };

    mockQuicklinksCopy.custom_links.push({
      ...newCustomLink,
      id: 4,
    });
    axios.post.mockResolvedValue({data: mockQuicklinksCopy});
    const wrapper = shallowMount(Quicklinks, {store, localVue});
    expect(wrapper.find('h3').text()).toEqual('Quick Links');

    wrapper.vm.customLink = newCustomLink;
    wrapper.vm.addLink({preventDefault: jest.fn()})

    // It takes like 10 ms for the dom to update
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.findAllComponents(Link)).toHaveLength(
      mockQuicklinksCopy['default_links'].length + mockQuicklinksCopy['custom_links'].length
    );
  });

  it('Remove link', async () => {
    const removeLinkIndex = 4;
    const mockQuicklinksCopy = JSON.parse(JSON.stringify(mockQuicklinks));

    mockQuicklinksCopy.default_links.splice(removeLinkIndex, 1);
    axios.post.mockResolvedValue({data: mockQuicklinksCopy});
    const wrapper = mount(Quicklinks, {store, localVue});
    expect(wrapper.find('h3').text()).toEqual('Quick Links');

    wrapper.findAllComponents(Link).at(removeLinkIndex).findAll('button').at(0).trigger('click');

    // It takes like 10 ms for the dom to update
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.findAllComponents(Link)).toHaveLength(
      mockQuicklinksCopy['default_links'].length
    );
  });

  it('Custom remove link', async () => {
    const mockQuicklinksCopy = JSON.parse(JSON.stringify(mockQuicklinks));
    const newCustomLink = {
      url: "http://test.com",
      label: "test",
    };

    const removeLinkIndex = mockQuicklinksCopy.custom_links.push({
      ...newCustomLink,
      id: 4,
    }) - 1;
    axios.post.mockResolvedValue({data: mockQuicklinksCopy});
    const wrapper = mount(Quicklinks, {store, localVue});
    expect(wrapper.find('h3').text()).toEqual('Quick Links');

    wrapper.vm.customLink = newCustomLink;
    wrapper.vm.addLink({preventDefault: jest.fn()})

    // It takes like 10 ms for the dom to update
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.findAllComponents(Link)).toHaveLength(
      mockQuicklinksCopy['default_links'].length + mockQuicklinksCopy['custom_links'].length
    );

    mockQuicklinksCopy.custom_links.splice(removeLinkIndex, 1);
    axios.post.mockResolvedValue({data: mockQuicklinksCopy});
    wrapper.findAllComponents(Link).at(
      mockQuicklinksCopy['default_links'].length + removeLinkIndex
    ).findAll('button').at(1).trigger('click');

    // It takes like 10 ms for the dom to update
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.findAllComponents(Link)).toHaveLength(
      mockQuicklinksCopy['default_links'].length + mockQuicklinksCopy['custom_links'].length
    );
  });

  it('Custom edit link', async () => {
    const mockQuicklinksCopy = JSON.parse(JSON.stringify(mockQuicklinks));
    const newCustomLink = {
      url: "http://test.com",
      label: "test",
    };

    const editLinkIndex = mockQuicklinksCopy.custom_links.push({
      ...newCustomLink,
      id: 4,
    }) - 1;
    axios.post.mockResolvedValue({data: mockQuicklinksCopy});
    const wrapper = mount(Quicklinks, {store, localVue});
    expect(wrapper.find('h3').text()).toEqual('Quick Links');

    wrapper.vm.customLink = newCustomLink;
    wrapper.vm.addLink({preventDefault: jest.fn()});

    // It takes like 10 ms for the dom to update
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.findAllComponents(Link)).toHaveLength(
      mockQuicklinksCopy['default_links'].length + mockQuicklinksCopy['custom_links'].length
    );

    const editCustomLink = {
      url: "http://test.com",
      label: "test-edit",
      id: 4, // from the push to custom_links
    };
    mockQuicklinksCopy.custom_links[editLinkIndex].label = editCustomLink.label;
    axios.post.mockResolvedValue({data: mockQuicklinksCopy});
    wrapper.findAllComponents(Link).at(
      mockQuicklinksCopy['default_links'].length + editLinkIndex
    ).vm.currentCustomLink = editCustomLink;
    wrapper.findAllComponents(Link).at(
      mockQuicklinksCopy['default_links'].length + editLinkIndex
    ).vm.updateLink({preventDefault: jest.fn()});

    // It takes like 10 ms for the dom to update
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.findAllComponents(Link)).toHaveLength(
      mockQuicklinksCopy['default_links'].length + mockQuicklinksCopy['custom_links'].length
    );
    expect(wrapper.findAllComponents(Link).at(
      mockQuicklinksCopy['default_links'].length + editLinkIndex
    ).text()).toMatch(editCustomLink.label);
  });

  it('recent save link', async () => {
    const mockQuicklinksCopy = JSON.parse(JSON.stringify(mockQuicklinks));
    const newRecentLink = {
      added: false,
      id: 2,
      url: "http://test.com",
      label: "test",
    };

    const newLinkIndex = mockQuicklinksCopy.recent_links.push({
      ...newRecentLink,
    }) - 1;
    axios.post.mockResolvedValue({data: mockQuicklinksCopy});
    const wrapper = mount(Quicklinks, {store, localVue});
    expect(wrapper.find('h3').text()).toEqual('Quick Links');

    // It takes like 10 ms for the dom to update
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.findAllComponents(Link)).toHaveLength(
      mockQuicklinksCopy['default_links'].length + mockQuicklinksCopy['recent_links'].length
    );

    wrapper.findAllComponents(Link).at(
      mockQuicklinksCopy['default_links'].length + newLinkIndex,
    ).vm.currentCustomLink = newRecentLink;
    wrapper.findAllComponents(Link).at(
      mockQuicklinksCopy['default_links'].length + newLinkIndex,
    ).vm.saveLink({preventDefault: jest.fn()});
  });

  it('onReset', () => {
    const wrapper = mount(Quicklinks, {store, localVue});
    expect(wrapper.find('h3').text()).toEqual('Quick Links');
    const newCustomLink = {
      url: "http://test.com",
      label: "test",
    };

    wrapper.vm.customLink = newCustomLink;
    expect(wrapper.vm.customLink).toEqual(newCustomLink);
    wrapper.vm.onReset({preventDefault: jest.fn()});

    expect(wrapper.vm.customLink).toEqual({});

    wrapper.findAllComponents(Link).at(0).vm.currentCustomLink = newCustomLink;
    expect(wrapper.findAllComponents(Link).at(0).vm.currentCustomLink).toEqual(newCustomLink);
    wrapper.findAllComponents(Link).at(0).vm.onReset({preventDefault: jest.fn()});
    expect(wrapper.findAllComponents(Link).at(0).vm.currentCustomLink).toEqual({});
  });
});
