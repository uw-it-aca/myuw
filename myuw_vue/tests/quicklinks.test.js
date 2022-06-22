import axios from 'axios';
import { mount } from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import quicklinks from '../vuex/store/quicklinks';
import Link from '../components/home/quicklinks/link.vue';
import CovidLink from '../components/home/quicklinks/covid-links.vue';
import Quicklinks from '../components/home/quicklinks/quicklinks.vue';

import mockQuicklinks from './mock_data/quicklinks.json';

const localVue = createLocalVue(Vuex);

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
        user: {
          affiliations: {
            student: true,
            instructor: true,
            seattle: false,
            bothell: false,
            tacoma: false,
            official_seattle: true,
            official_bothell: false,
            official_tacoma: false,
          }
        },
      }
    });
  });

  it('Basic Mount', async () => {
    axios.get.mockResolvedValueOnce({data: mockQuicklinks, status: 200});
    const wrapper = mount(Quicklinks, {store, localVue});

    await new Promise(setImmediate);
    expect(wrapper.find('h2').text()).toEqual('Quick Links');
    expect(wrapper.findAllComponents(Link)).toHaveLength(mockQuicklinks['default_links'].length);
    expect(wrapper.findComponent(CovidLink).exists()).toBe(true);

    let wrapperCovid = mount(CovidLink, { store, localVue });
    expect(wrapperCovid.vm.student).toBe(true);
    expect(wrapperCovid.vm.instructor).toBe(true);
    expect(wrapperCovid.vm.seattleStudent).toBe(false);
    expect(wrapperCovid.vm.bothellStudent).toBe(false);
    expect(wrapperCovid.vm.tacomaStudent).toBe(false);
    expect(wrapperCovid.vm.seattleEmp).toBe(true);
    expect(wrapperCovid.vm.bothellEmp).toBe(false);
    expect(wrapperCovid.vm.tacomaEmp).toBe(false);
    // MUWM-5077
    let allH3s = wrapperCovid.findAll('h3');
    expect(allH3s.length).toBe(2);
    expect(allH3s.at(0).text()).toEqual('UW Coronavirus');
    expect(allH3s.at(1).text()).toEqual('Online Teaching');

    store.state.user.affiliations.seattle = true;
    store.state.user.affiliations.official_seattle = false;
    store.state.user.affiliations.official_tacoma = true;
    wrapperCovid = mount(CovidLink, { store, localVue });
    expect(wrapperCovid.vm.seattleStudent).toBe(true);
    expect(wrapperCovid.vm.seattleEmp).toBe(false);
    expect(wrapperCovid.vm.tacomaEmp).toBe(true);
    allH3s = wrapperCovid.findAll('h3');
    expect(allH3s.length).toBe(3);
    expect(allH3s.at(1).text()).toEqual('Online Learning');
    expect(allH3s.at(2).text()).toEqual('Online Teaching');
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

    await new Promise(setImmediate);
    expect(wrapper.find('h2').text()).toEqual('Quick Links');

    wrapper.vm.customLink = newCustomLink;
    wrapper.vm.addLink({preventDefault: jest.fn()})

    // It takes like 10 ms for the dom to update
    await new Promise(setImmediate);
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

    await new Promise(setImmediate);
    expect(wrapper.find('h2').text()).toEqual('Quick Links');

    wrapper.findAllComponents(Link).at(removeLinkIndex).findAll('button').at(0).trigger('click');

    // It takes like 10 ms for the dom to update
    await new Promise(setImmediate);
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
    await new Promise(setImmediate);
    expect(wrapper.find('h2').text()).toEqual('Quick Links');

    wrapper.vm.customLink = newCustomLink;
    wrapper.vm.addLink({preventDefault: jest.fn()})

    // It takes like 10 ms for the dom to update
    await new Promise(setImmediate);
    expect(wrapper.findAllComponents(Link)).toHaveLength(
      mockQuicklinksCopy['default_links'].length + mockQuicklinksCopy['custom_links'].length
    );

    mockQuicklinksCopy.custom_links.splice(removeLinkIndex, 1);
    axios.post.mockResolvedValue({data: mockQuicklinksCopy});
    wrapper.findAllComponents(Link).at(
      mockQuicklinksCopy['default_links'].length + removeLinkIndex
    ).findAll('button').at(1).trigger('click');

    // It takes like 10 ms for the dom to update
    await new Promise(setImmediate);
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
    await new Promise(setImmediate);
    expect(wrapper.find('h2').text()).toEqual('Quick Links');

    wrapper.vm.customLink = newCustomLink;
    wrapper.vm.addLink({preventDefault: jest.fn()});

    // It takes like 10 ms for the dom to update
    await new Promise(setImmediate);
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
    await new Promise(setImmediate);
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
    await new Promise(setImmediate);
    expect(wrapper.find('h2').text()).toEqual('Quick Links');

    // It takes like 10 ms for the dom to update
    await new Promise(setImmediate);
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
    await new Promise(setImmediate);
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
