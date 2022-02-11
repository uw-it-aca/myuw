import { mount } from '@vue/test-utils'
import { createLocalVue } from '../helper';

import Vuex from 'vuex';

import Tabs from '../../components/_templates/tabs/tabs.vue';
import TabButton from '../../components/_templates/tabs/button.vue';
import TabDropdown from '../../components/_templates/tabs/dropdown.vue';
import TabPanel from '../../components/_templates/tabs/panel.vue';

const localVue = createLocalVue(Vuex);

const TabsTestComponent = {
  template: `
  <uw-tabs
    pills
    bottom-border
    nav-class="mock-nav-class"
    nav-wrapper-class="mock-nav-wrapper-class">
        <template #tabs>
            <uw-tab-button panel-id="tab1"
                title-item-class="me-2 mb-1"
                title-link-class="rounded-0 text-body">
            TAB 1 TITLE
            </uw-tab-button>
            <uw-tab-button panel-id="tab2"
                title-item-class="mock-title-item-class"
                title-link-class="mock-title-link-class">
            TAB 2 TITLE
            </uw-tab-button>
            <uw-tab-dropdown
                v-model="selectedOption"
                panel-id="dropdown"
                :options-list="dropdownOptions"
                title-item-class="mock-title-item-class"
                title-link-class="mock-title-link-class">
            </uw-tab-dropdown>
        </template>
        <template #panels>
            <uw-tab-panel panel-id="tab1">
                TAB 1 PANEL
            </uw-tab-panel>
            <uw-tab-panel panel-id="tab2">
                TAB 2 PANEL
            </uw-tab-panel>
            <uw-tab-panel panel-id="dropdown">
                DROPDOWN PANEL
            </uw-tab-panel>
        </template>
    </uw-tabs>
  `,
  components: {
    'uw-tabs': Tabs,
    'uw-tab-button': TabButton,
    'uw-tab-dropdown': TabDropdown,
    'uw-tab-panel': TabPanel,
  },
  data: function() {
    return {
      selectedOption: 0,
      dropdownOptions: [
          {value: "option0", text: "Option 0", disabled: true},
          {value: "option1", text: "Option 1"},
          {value: "option2", text: "Option 2"},
      ],
    };
  },
}

it('test tabs initial content', () => {
  const wrapper = mount(TabsTestComponent, {localVue})
  let tabs = wrapper.findComponent(Tabs)
  let tabButtons = wrapper.findAllComponents(TabButton);
  let tabButton0 = tabButtons.at(0);
  let tabButton1 = tabButtons.at(1);
  let tabDropdowns = wrapper.findAllComponents(TabDropdown);
  let tabDropdown0 = tabDropdowns.at(0);
  let tabPanels = wrapper.findAllComponents(TabPanel);
  let tabPanel0 = tabPanels.at(0);
  let tabPanel1 = tabPanels.at(1);
  let tabPanel2 = tabPanels.at(2);

  // tabs container
  expect(tabs.exists()).toBe(true);
  expect(tabs.attributes('class')).toBe('tabs');
  expect(tabs.props('activeTabIdx')).toBe(0);
  expect(tabs.props('small')).toBe(false);
  expect(tabs.props('justified')).toBe(false);
  expect(tabs.props('pills')).toBe(true);
  expect(tabs.props('bottomBorder')).toBe(true);
  expect(tabs.vm.navWrapperClassesComputed).toStrictEqual(
      {"mock-nav-wrapper-class": true});
  expect(tabs.vm.navClassesComputed).toStrictEqual(
      {"mock-nav-class": true, "nav": true, "myuw-tabs": true,
       "nav-pills": true, "nav-tabs": false, "myuw-bottom-border": true});

  // buttons
  expect(tabButtons.length).toBe(2);

  expect(tabButton0.text()).toBe("TAB 1 TITLE")
  expect(tabButton0.props('panelId')).toBe('tab1');
  expect(tabButton0.props('titleItemClass')).toBe('me-2 mb-1');
  expect(tabButton0.props('titleLinkClass')).toBe('rounded-0 text-body');
  expect(tabButton0.vm.active).toBe(true);
  expect(tabButton0.vm.titleItemClassComputed).toStrictEqual(
      {"mb-1": true, "me-2": true, "nav-item": true});
  expect(tabButton0.attributes('class')).toBe('me-2 mb-1 nav-item');
  expect(tabButton0.vm.titleLinkClassComputed).toStrictEqual(
    {"rounded-0": true, "text-body": true, "nav-link": true,
     "text-nowrap": true, "px-2": true, "py-1": true, "h-100": true,
     "active": true});

  expect(tabButton1.text()).toBe("TAB 2 TITLE")
  expect(tabButton1.props('panelId')).toBe('tab2');
  expect(tabButton1.props('titleItemClass')).toBe('mock-title-item-class');
  expect(tabButton1.props('titleLinkClass')).toBe('mock-title-link-class');
  expect(tabButton1.vm.active).toBe(false);
  expect(tabButton1.vm.titleItemClassComputed).toStrictEqual(
    {"mock-title-item-class": true, "nav-item": true});
  expect(tabButton1.attributes('class')).toBe('mock-title-item-class nav-item');
  expect(tabButton1.vm.titleLinkClassComputed).toStrictEqual(
    {"mock-title-link-class": true, "nav-link": true,
     "text-nowrap": true, "px-2": true, "py-1": true, "h-100": true,
     "active": false});

  // dropdowns
  expect(tabDropdowns.length).toBe(1);
  expect(tabDropdown0.props('panelId')).toBe('dropdown');
  expect(tabDropdown0.vm.active).toBe(false);
  expect(tabDropdown0.vm.titleItemClassComputed).toStrictEqual(
    {"mock-title-item-class": true, "nav-item": true});
  expect(tabDropdown0.attributes('class')).toBe('mock-title-item-class nav-item');
  expect(tabDropdown0.vm.titleLinkClassComputed).toStrictEqual(
    {"mock-title-link-class": true, "nav-link": true,
     "text-nowrap": true, "pb-1": true, "pt-1": true, "h-100": true,
     "active": false, "text-body": true, "rounded-0": true});
  // dropdown options
  const optionEls = tabDropdown0.findAll('option');
  expect(optionEls.exists()).toBe(true);
  expect(optionEls.length).toBe(3);
  expect(optionEls.at(0).text()).toBe("Option 0");
  expect(optionEls.at(0).attributes('value')).toBe("option0");
  expect(optionEls.at(0).element.disabled).toBe(true);
  expect(optionEls.at(1).text()).toBe("Option 1");
  expect(optionEls.at(1).attributes('value')).toBe("option1");
  expect(optionEls.at(1).element.disabled).toBe(false);
  expect(optionEls.at(2).text()).toBe("Option 2");
  expect(optionEls.at(2).attributes('value')).toBe("option2");
  expect(optionEls.at(2).element.disabled).toBe(false);

  // panels
  expect(tabPanels.length).toBe(3);

  expect(tabPanel0.text()).toBe("TAB 1 PANEL")
  expect(tabPanel0.props('panelId')).toBe('tab1');
  expect(tabPanel0.vm.active).toBe(true);

  expect(tabPanel1.text()).toBe("TAB 2 PANEL")
  expect(tabPanel1.props('panelId')).toBe('tab2');
  expect(tabPanel1.vm.active).toBe(false);

  expect(tabPanel2.text()).toBe("DROPDOWN PANEL")
  expect(tabPanel2.props('panelId')).toBe('dropdown');
  expect(tabPanel2.vm.active).toBe(false);
});

it('test changing active tab via a button click', async () => {
    const wrapper = mount(TabsTestComponent, {localVue})
    let tabs = wrapper.findComponent(Tabs)
    let tabButtons = wrapper.findAllComponents(TabButton);
    let tabButton1 = tabButtons.at(1);

    const buttonEl = tabButton1.find('button');
    buttonEl.trigger('click');
    await wrapper.vm.$nextTick();
    // assert event has been emitted
    expect(tabs.emitted().setActivePanel).toBeTruthy()
    expect(tabs.emitted().setActivePanel.length).toBe(1)
    expect(tabs.emitted().setActivePanel[0]).toEqual(["tab2"])
});

it('test changing active tab via left key press on button', async () => {
    const wrapper = mount(TabsTestComponent, {localVue})
    let tabs = wrapper.findComponent(Tabs)
    let tabButtons = wrapper.findAllComponents(TabButton);
    let tabButton0 = tabButtons.at(0);

    const buttonEl = tabButton0.find('button');
    buttonEl.trigger('keydown.left.prevent');
    await wrapper.vm.$nextTick();
    // assert event has been emitted
    expect(tabs.emitted().moveActiveTabLeft).toBeTruthy()
    expect(tabs.emitted().moveActiveTabLeft.length).toBe(1)
});

it('test changing active tab via right key press on button', async () => {
    const wrapper = mount(TabsTestComponent, {localVue})
    let tabs = wrapper.findComponent(Tabs)
    let tabButtons = wrapper.findAllComponents(TabButton);
    let tabButton0 = tabButtons.at(0);

    const buttonEl = tabButton0.find('button');
    buttonEl.trigger('keydown.right.prevent');
    await wrapper.vm.$nextTick();
    // assert event has been emitted
    expect(tabs.emitted().moveActiveTabRight).toBeTruthy()
    expect(tabs.emitted().moveActiveTabRight.length).toBe(1)
});

it('test changing active tab via dropdown select change', async () => {
    const wrapper = mount(TabsTestComponent, {localVue})
    let tabs = wrapper.findComponent(Tabs)
    let tabDropdowns = wrapper.findAllComponents(TabDropdown);
    let tabDropdown0 = tabDropdowns.at(0);

    const selectEl = tabDropdown0.find('select');
    selectEl.trigger('change');
    await wrapper.vm.$nextTick();
    // assert event has been emitted
    expect(tabDropdown0.emitted().input).toBeTruthy()
    expect(tabDropdown0.emitted().input.length).toBe(1)
    expect(tabs.emitted().setActivePanel).toBeTruthy()
    expect(tabs.emitted().setActivePanel.length).toBe(1)
});

it('test changing active tab via left key press on dropdown', async () => {
    const wrapper = mount(TabsTestComponent, {localVue})
    let tabs = wrapper.findComponent(Tabs)
    let tabDropdowns = wrapper.findAllComponents(TabDropdown);
    let tabDropdown0 = tabDropdowns.at(0);

    const selectEl = tabDropdown0.find('select');
    selectEl.trigger('keydown.left.prevent');
    await wrapper.vm.$nextTick();
    // assert event has been emitted
    expect(tabs.emitted().moveActiveTabLeft).toBeTruthy()
    expect(tabs.emitted().moveActiveTabLeft.length).toBe(1)
});

it('test changing active tab via right key press on dropdown', async () => {
    const wrapper = mount(TabsTestComponent, {localVue})
    let tabs = wrapper.findComponent(Tabs)
    let tabDropdowns = wrapper.findAllComponents(TabDropdown);
    let tabDropdown0 = tabDropdowns.at(0);

    const selectEl = tabDropdown0.find('select');
    selectEl.trigger('keydown.right.prevent');
    await wrapper.vm.$nextTick();
    // assert event has been emitted
    expect(tabs.emitted().moveActiveTabRight).toBeTruthy()
    expect(tabs.emitted().moveActiveTabRight.length).toBe(1)
});