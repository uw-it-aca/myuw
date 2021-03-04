import VueGtag from 'vue-gtag';
import utils from '../mixins/utils';

class Logger {
  constructor(sink) {
    this.sink = sink;
  }

  cardLoad(component) {
    component.$nextTick(() => {
      let compTid = component.compTid;
      if (!compTid) {
        // Try to create the compTid from the card heading
        const cardHeading = component.$slots['card-heading'];
        if (
          cardHeading &&
          cardHeading[0] &&
          cardHeading[0].children &&
          cardHeading[0].children[0] &&
          cardHeading[0].children[0].text
        ) {
          compTid = cardHeading[0].children[0].text.trim();
        }
      }

      let parentCompTag = null;
      // Try to find the component tag
      for (let comp=component.$parent; comp.$parent; comp = comp.$parent) {
        if (comp.$options._componentTag.startsWith("myuw")) {
          parentCompTag = comp.$options._componentTag;
          break;
        }
      }

      if (compTid) {
        this.sink.event('card_load', {
          comp_tid: compTid,
          comp_tag: parentCompTag,
        });
      }
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

  Vue.prototype.$logger = new Logger(sink);
};