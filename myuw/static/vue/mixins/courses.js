import utils from './utils';

let firstSelfAnchored = true;

export default {
  methods: {
    quoteField(x) {
        if (x) {
            x = x.replace(/"/g, '\\"');
            return '"'+x+'"';
        }
        return '""';
    },
    sectionFormattedDates(section) {
      const dayjs = utils.methods.dayjs;
      return `${dayjs(section.start_date).format('MMM D')} - ${dayjs(
          section.end_date).format('MMM D')}`;
    },
    combineMajors(majors) {
      if (majors === undefined || majors.length == 0) {
        return '';
      }
      const rmajors = [];
      for (let j = 0; j < majors.length; j++) {
        const mj = majors[j];
        let v = mj.full_name ? mj.full_name : utils.methods.titleCaseName(mj.name);
        rmajors.push(v.replace(/, /g, ' '));
      }
      return rmajors.length > 1 ? rmajors.join(', ') : rmajors[0];
    },
    buildClasslistCsv(registrations, hasLinkedSections) {
        const lines = [];
        const header = ["StudentNo","UWNetID","LastName","FirstName","Pronouns"];
        if (hasLinkedSections) {
            header.push("LinkedSection");
            }
        header.push("Credits","Class","Major","Email");
        lines.push(header.join(","));

        for (let i = 0; i < registrations.length; i++) {
            const reg = registrations[i];
            if (reg.isJoint) {  //MUWM-4371
                continue;
            }
            const fields = [
              "\t" + reg.student_number,  // MUWM-3978
              reg.netid,
              reg.surname,
              reg.first_name,
              reg.pronouns];

            if (hasLinkedSections) {
              fields.push(reg.linked_sections);
            }

            let credits = reg.is_auditor ? "Audit" : reg.credits;
            fields.push(
              credits, reg.class_level, this.combineMajors(reg.majors), reg.email);
            lines.push(fields.map(this.quoteField).join(","));
        }
        return lines.join("\n");
    },
    classlistFileName(section) {
      const fn = section.section_label + '_students.csv';
      return fn.replace(/[^a-z0-9._]/ig, '_');
    },
    downloadClassList(classlist) {
      const hiddenElement = document.createElement('a');
      const csvData = this.buildClasslistCsv(
          classlist.registrations, classlist.has_linked_sections);

      hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvData); // MUWM-5004
      hiddenElement.target = '_blank';
      hiddenElement.download = this.classlistFileName(classlist);
      hiddenElement.click();
    },
    getQuarterAbbr(quarter_str) {
      // return the first 3 letter word in upper case
      return (!quarter_str || quarter_str.length === 0) ? '' :
        quarter_str.substring(0, 3).toUpperCase();
    },
    getTimeScheHref(section) {
      return ('http://sdb.admin.uw.edu/timeschd/uwnetid/sln.asp?QTRYR=' +
              this.getQuarterAbbr(section.quarter) + '+' +
              section.year + '&SLN=' + section.sln);
    },
    getTimeScheLinkLable(section) {
      return 'Time Schedule for SLN ' + section.sln;
    },
    selfAnchoredOnce(section) {
      // anchor on the section uw-card where div id is section.anchor
      if (firstSelfAnchored) {
        const el = document.getElementById(section.anchor);
        if (el) {
          el.scrollIntoView({behavior: 'smooth'});
        }
        firstSelfAnchored = false;
      }
    },
  },
}
