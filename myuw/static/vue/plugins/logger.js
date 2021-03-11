import VueGtag from 'vue-gtag';
import utils from '../mixins/utils';
import { findParentMyUWComponentTag } from './utils';

class Logger {
  constructor(sink, options) {
    this.sink = sink;
    this.compsInViewport = {};
    this.currentTerm = null;

    this.options = options || {};
    if (!this.options.compInViewportRatioThreshold) {
      this.options.compInViewportRatioThreshold = 0.9;
    }
    if (!this.options.compInViewportDurationThreshold) {
      this.options.compInViewportDurationThreshold = 2;
    }

    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') {
        this.flushCompInViewPort();
      } else if (document.visibilityState === 'visible') {
        this.restartCompInViewPort();
      }
    });
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

  visibilityChanged(component, entry) {
    let onScreen = false;

    let screenCoveredRatio = 0;
    if (entry.rootBounds) {
      const rootArea = entry.rootBounds.height * entry.rootBounds.width;
      const cardArea = entry.boundingClientRect.height * entry.boundingClientRect.width;
      screenCoveredRatio = 1 - (rootArea - (cardArea * entry.intersectionRatio)) / rootArea;
    }

    // Update the array (dict in reality) of components on the page
    this.compsInViewport[component.uid] = {
      instance: component,
      compOnScreenRatio: entry.intersectionRatio,
      screenCoveredRatio: screenCoveredRatio,
      timer: this.compsInViewport[component.uid] ?
        this.compsInViewport[component.uid].timer : null,
    };

    // Report if the component it is mostly visible
    if (entry.intersectionRatio > this.options.compInViewportRatioThreshold) {
      onScreen = true;
    }

    // Covers the most screen space
    onScreen = onScreen || (Object.values(this.compsInViewport).every(
      (comp) => comp.screenCoveredRatio <= screenCoveredRatio,
    ) && screenCoveredRatio > 0.1);

    if (onScreen) {
      if (!this.compsInViewport[component.uid].timer) {
        this.compsInViewport[component.uid].timer = Date.now();
      }
    } else if (this.compsInViewport[component.uid].timer) {
      const duration = (Date.now() - this.compsInViewport[component.uid].timer) / 1000;
      this.compsInViewport[component.uid].timer = null;

      if (duration > this.options.compInViewportDurationThreshold) {
        this.sink.event('comp_in_viewport', {
          comp_tag: findParentMyUWComponentTag(component),
          duration: duration,
        });
      }
    }
  }

  flushCompInViewPort() {
    Object.values(this.compsInViewport).forEach((compData) => {
      if (compData.timer) {
        const duration = (Date.now() - compData.timer) / 1000;
        compData.timer = null;
        compData.terminatedByFlush = true;

        if (duration > this.options.compInViewportDurationThreshold) {
          this.sink.event('comp_in_viewport', {
            comp_tag: findParentMyUWComponentTag(compData.instance),
            duration: duration,
          });
        }
      }
    });
  }

  restartCompInViewPort() {
    Object.values(this.compsInViewport)
      .filter((compData) => compData.terminatedByFlush)
      .forEach((compData) => {
        compData.timer = Date.now();
        compData.terminatedByFlush = false;
      });
  }

  quicklink(action, url) {
    this.sink.event(`quick_link`, {
      link_url: url,
      action: action,
    });
  }

  disclosureOpen(component) {
    this.sink.event('disclosure_open', {
      comp_tag: findParentMyUWComponentTag(component),
    });
  }

  noticeOpen(component, notice) {
    const htmlDoc = new DOMParser().parseFromString(
      notice.notice_title, 'text/html',
    );
    this.sink.event('notice_open', {
      comp_tag: findParentMyUWComponentTag(component),
      notice_title: htmlDoc.getElementsByClassName('notice-title')[0].innerText,
    });
  }

  noticeRead(component, notice) {
    const htmlDoc = new DOMParser().parseFromString(
      notice.notice_title, 'text/html',
    );
    this.sink.event('notice_read', {
      comp_tag: findParentMyUWComponentTag(component),
      notice_title: htmlDoc.getElementsByClassName('notice-title')[0].innerText,
    });
  }

  classEmailList(component, cardTid) {
    this.sink.event('class_email_list', {
      comp_tag: findParentMyUWComponentTag(component),
      card_tid: cardTid,
    });
  }

  onBoarding(component) {
    this.sink.event('on_boarding', {
      comp_tag: findParentMyUWComponentTag(component),
    });
  }

  cardPin(component, cardTid) {
    this.sink.event('card_pin', {
      comp_tag: findParentMyUWComponentTag(component),
      card_tid: cardTid,
    });
  }

  cardUnPin(component, cardTid) {
    this.sink.event('card_unpin', {
      comp_tag: findParentMyUWComponentTag(component),
      card_tid: cardTid,
    });
  }

  termSelected(term) {
    // Sometimes the same term gets reported twice
    // this deduplicates it
    if (this.currentTerm !== term) {
      this.sink.event('term_selected', {
        term_tid: term,
      });
      this.currentTerm = term;
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

  Vue.$logger = Vue.prototype.$logger = new Logger(sink, options.logger);
};