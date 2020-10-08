import axios from 'axios';
import {mount, shallowMount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import quicklinks from '../vuex/store/quicklinks';
import Link from '../components/home/cards/quicklinks/link.vue';
import Quicklinks from '../components/home/cards/quicklinks/quicklinks.vue';

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

library.add(faExclamationTriangle);
library.add(faPencilAlt);
library.add(faTimes);
library.add(faPlus);

localVue.component('font-awesome-icon', FontAwesomeIcon);
localVue.component('font-awesome-layers', FontAwesomeLayers);

jest.mock('axios');

describe('Quicklinks/Link', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        quicklinks,
      },
      state: {
        csrfToken: "dfsdfsgfsdg",
      },
    });
  });

  it('Basic Mount', async () => {
    axios.get.mockResolvedValueOnce({data: mockQuicklinks, status: 200});
    const wrapper = mount(Quicklinks, {store, localVue});

    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('h3').text()).toEqual('Quick Links');
    expect(wrapper.findAllComponents(Link)).toHaveLength(mockQuicklinks['default_links'].length);
  });

  it('Add link', async () => {
    axios.get.mockResolvedValueOnce({data: mockQuicklinks, status: 200});
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
    const wrapper = mount(Quicklinks, {store, localVue});

    await new Promise((r) => setTimeout(r, 10));
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
    axios.get.mockResolvedValueOnce({data: mockQuicklinks, status: 200});
    const removeLinkIndex = 4;
    const mockQuicklinksCopy = JSON.parse(JSON.stringify(mockQuicklinks));

    mockQuicklinksCopy.default_links.splice(removeLinkIndex, 1);
    axios.post.mockResolvedValue({data: mockQuicklinksCopy});
    const wrapper = mount(Quicklinks, {store, localVue});

    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('h3').text()).toEqual('Quick Links');

    wrapper.findAllComponents(Link).at(removeLinkIndex).findAll('button').at(0).trigger('click');

    // It takes like 10 ms for the dom to update
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.findAllComponents(Link)).toHaveLength(
      mockQuicklinksCopy['default_links'].length
    );
  });

  it('Custom remove link', async () => {
    axios.get.mockResolvedValueOnce({data: mockQuicklinks, status: 200});
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
    await new Promise((r) => setTimeout(r, 10));
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
    axios.get.mockResolvedValueOnce({data: mockQuicklinks, status: 200});
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
    await new Promise((r) => setTimeout(r, 10));
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
    axios.get.mockResolvedValue({data: mockQuicklinksCopy});
    const wrapper = mount(Quicklinks, {store, localVue});
    await new Promise((r) => setTimeout(r, 10));
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

  it('onReset', async () => {
    axios.get.mockResolvedValueOnce({data: mockQuicklinks, status: 200});

    const wrapper = mount(Quicklinks, {store, localVue});
    await new Promise((r) => setTimeout(r, 10));
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
    expect(
      wrapper.findAllComponents(Link).at(0).vm.currentCustomLink
    ).toEqual(mockQuicklinks.default_links[0]);
  });
});
