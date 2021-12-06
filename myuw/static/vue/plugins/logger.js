import VueGtag from 'vue-gtag';
import utils from '../mixins/utils';
import { VisibilityTracker } from './utils';

class Logger {
  constructor(sink, options) {
    this.sink = sink;
    this.currentTerm = null;
    this.cardGroupEvents = {};
    this.visibilityTracker = new VisibilityTracker(
      options,
      this.onVisibilityReport.bind(this),
    );
    this.config = {};
  }

  compLoad(component) {
    component.$nextTick(() => {
      let root = component.$meta.group;
      if (
        root.$meta.group &&
        this.cardGroupEvents[root.$meta.uid] &&
        this.cardGroupEvents[root.$meta.uid].compLoad
      ) {
        this.cardGroupEvents[root.$meta.uid].compLoad += 1;
        return;
      } else {
        this.cardGroupEvents[root.$meta.uid] = {
          compLoad: 1,
        };
      }
      const data = {
        comp_tag: component.compTag ? component.compTag : root.$meta.tag,
      };
      if (component.$meta.term) {
        data.term_tag = component.$meta.term;
      }
      this.sink.event('comp_load', data);
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

  linkClick(component, label, out) {
    const data = {
      comp_tag: component.$meta.group.$meta.tag,
      link_label: label,
      link_to_external: out,
    };
    if (component.$meta.term) {
      data.term_tag = component.$meta.term;
    }
    if (component.$meta.course) {
      data.course_tag = component.$meta.course;
    }
    this.sink.event('link_click', data);
  }

  visibilityChanged(component, entry) {
    this.onVisibilityReport(this.visibilityTracker.update(component, entry));
  }

  onVisibilityReport(compData) {
    if (compData.report) {
      this.sink.event('comp_in_viewport', {
        comp_tag: compData.tag,
        duration: Math.floor(compData.duration),
      });
    }
  }

  quicklink(action, url) {
    this.sink.event(`quick_link`, {
      link_url: url,
      action_label: action,
    });
  }

  disclosureOpen(component, label) {
    const data = {
      comp_tag: component.$meta.group.$meta.tag,
      disclosure_label: label,
    };
    if (component.$meta.term) {
      data.term_tag = component.$meta.term;
    }
    if (component.$meta.course) {
      data.course_tag = component.$meta.course;
    }
    this.sink.event('disclosure_open', data);
  }

  noticeOpen(component, notice) {
    const htmlDoc = new DOMParser().parseFromString(
      notice.notice_title, 'text/html',
    );
    const data = {
      comp_tag: component.$meta.group.$meta.tag,
      notice_title: htmlDoc.getElementsByClassName('notice-title')[0].innerText,
      is_critical: notice.is_critical,
      is_new: !notice.is_read,
      time_before_read: 0,
    };
    if (notice.startDate && !notice.is_read) {
      let timeBeforeRead = Math.floor((Date.now() - notice.startDate) / (1000 * 60 * 60));
      if (timeBeforeRead > 0) data.time_before_read = timeBeforeRead;
    }
    this.sink.event('notice_open', data);
  }

  classEmailList(component, action) {
    const data = {
      comp_tag: component.$meta.group.$meta.tag,
      action_label: action,
    };
    if (component.$meta.term) {
      data.term_tag = component.$meta.term;
    }
    if (component.$meta.course) {
      data.course_tag = component.$meta.course;
    }
    this.sink.event('class_email_list', data);
  }

  onBoarding(component) {
    this.sink.event('on_boarding', {
      comp_tag: component.$meta.group.$meta.tag,
    });
  }

  cardPin(component, cardLabel) {
    const data = {
      comp_tag: component.$meta.group.$meta.tag,
      card_label: cardLabel,
    };
    if (component.$meta.term) {
      data.term_tag = component.$meta.term;
    }
    if (component.$meta.course) {
      data.course_tag = component.$meta.course;
    }
    this.sink.event('card_pin', data);
  }

  cardUnPin(component, cardLabel) {
    const data = {
      comp_tag: component.$meta.group.$meta.tag,
      card_label: cardLabel,
    };
    if (component.$meta.term) {
      data.term_tag = component.$meta.term;
    }
    if (component.$meta.course) {
      data.course_tag = component.$meta.course;
    }
    this.sink.event('card_unpin', data);
  }

  termSelected(term) {
    // Sometimes the same term gets reported twice
    // this deduplicates it
    if (this.currentTerm !== term) {
      this.sink.event('term_selected', {
        term_tag: term,
      });
      this.currentTerm = term;
    }
  }

  buttonClick(component) {
    this.sink.event('button_click', {
      comp_tag: component.$meta.group.$meta.tag,
    });
  }

  setHybrid(value) {
    this.sink.hybrid = value;
  }
}

class ConsoleSink {
  constructor(options) {
    this.properties = {};
    this.config = {};
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

  config(config) {
    this.config = config;
  }
}

class GtagSink {
  constructor(gtag) {
    this.gtag = gtag;
    this.hybrid = false;
  }

  event(name, data) {
    data.is_hybrid = this.hybrid;
    this.gtag.event(name, data);
  }

  set(key, value) {
    this.gtag.set(key, value);
  }

  pageview(pageData) {
    this.gtag.pageview(pageData);
  }

  config(config) {
    this.gtag.config(config);
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

  Vue.$logger = Vue.prototype.$logger = new Logger(sink, options.logger);
};