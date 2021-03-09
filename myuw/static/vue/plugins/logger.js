import VueGtag from 'vue-gtag';
import utils from '../mixins/utils';
import { findParentMyUWComponentTag } from './utils';

class Logger {
  constructor(sink) {
    this.sink = sink;
    this.compsInViewport = [];
  }

  cardLoad(component) {
    component.$nextTick(() => {
      this.sink.event('card_load', {
        comp_tag: component.compTag ?
          component.compTag :
          findParentMyUWComponentTag(component),
      });
    });
  }

  setUserProperties(affiliations) {
    const properties = {};
    properties['affiliation'] = (
      affiliations['applicant'] ? 'Applicant' :
      affiliations['faculty'] ? 'Faculty' :
      affiliations['staff_employee'] ? 'Staff' :
      affiliations['student'] ? 'Student' :
      affiliations['alumni'] ? 'Alumni' : null
    );

    properties['class_level'] = utils.methods.titleCaseWord(affiliations['class_level']);

    properties['continuum_college'] = (
      affiliations['grad_c2'] ? 'GradC2' :
      affiliations['undergrad_c2'] ? 'UndergradC2' :
      affiliations['pce'] ? 'PCE' : null
    );

    properties['emp_position'] = (
      affiliations['instructor'] ? 'Instructor' :
      affiliations['stud_employee'] ? 'Stud employee' :
      affiliations['clinician'] ? 'Clinician' :
      affiliations['retiree'] ? 'Retiree' : null
    );

    properties['student_prop'] = (
      affiliations['intl_stud'] ? 'International' :
      affiliations['past_stud'] ? 'Former' : null
    );

    properties['student_campus'] = (
      affiliations['seattle'] ? 'Seattle' :
      affiliations['bothell'] ? 'Bothell' :
      affiliations['tacoma'] ? 'Tacoma' : null
    );

    properties['employment_campus'] = (
      affiliations['official_seattle'] ? 'Seattle' :
      affiliations['official_bothell'] ? 'Bothell' :
      affiliations['official_tacoma'] ? 'Tacoma' : null
    );

    this.sink.set('user_properties', properties);
  }

  pageview(pageData) {
    this.sink.pageview(pageData);
  }

  search(searchTerm) {
    this.sink.event('search', {search_term: searchTerm});
  }

  linkClick(component, url, label, out) {
    this.sink.event('link_click', {
      comp_tag: findParentMyUWComponentTag(component),
      link_url: url,
      link_label: label,
      link_to_external: out,
    });
  }

  compInViewport(component, intersectionRatio) {
    let report = false;

    // Update the array of components on the page
    let inArrayInstance = this.compsInViewport.find((o) => component === o.comp);
    if (inArrayInstance) {
      inArrayInstance.ir = intersectionRatio;
    } else {
      this.compsInViewport.push({comp: component, ir: intersectionRatio});
    }
    this.compsInViewport.sort((a, b) => - (a.ir - b.ir));

    // Report if the component it is mostly visible
    if (intersectionRatio > 0.995) {
      report = true;
    }

    // Report if the component is the most visible one
    if (inArrayInstance === this.compsInViewport[0]) {
      report = true;
    }

    if (report) console.log(report, intersectionRatio, component.$vnode.elm);
    if (report) {
      this.sink.event('comp_in_viewport', {
        comp_tag: findParentMyUWComponentTag(component),
      });
    }
  }
}

class ConsoleSink {
  constructor(options) {
    this.properties = {};
    this.logHistory = [];
    this.options = options;
    window.console_sink = this;
  }

  event(name, data) {
    this.logHistory.push({[name]: data});
    if (this.options['print']) {
      console.log('event', name, data);
    }
  }

  set(key, value) {
    this.properties[key] = value;
    if (this.options['print']) {
      console.log('set', key, value);
    }
  }

  pageview(pageData) {
    this.properties['page'] = pageData;
    if (this.options['print']) {
      console.log('pageview', pageData);
    }
  }
}

class GtagSink {
  constructor(gtag) {
    this.gtag = gtag;
  }

  event(name, data) {
    this.gtag.event(name, data);
  }

  set(key, value) {
    this.gtag.set(key, value);
  }

  pageview(pageData) {
    this.gtag.pageview(pageData);
  }
}

export default function (Vue, options) {
  let sink = null;
  if ('gtag' in options) {
    Vue.use(VueGtag, options['gtag']);
    sink = new GtagSink(Vue.prototype.$gtag);
  } else if ('console' in options) {
    sink = new ConsoleSink(options['console']);
  } else {
    throw '`gtag` or `console` config needed';
  }

  Vue.$logger = Vue.prototype.$logger = new Logger(sink);
};