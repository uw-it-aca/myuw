import utils from './utils';

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
        if (mj.full_name || mj.name) {
          let v = mj.full_name ? mj.full_name : utils.methods.titleCaseName(mj.name);
          rmajors.push(v.replace(/, /g, ' '));
        }
      }
      return rmajors.length > 1 ? rmajors.join(', ') : rmajors[0];
    },
    buildClasslistCsv(section, showJointCourse) {
        const registrations = section.registrations;
        const hasLinkedSections = section.has_linked_sections;
        const lines = [];
        const header = ["StudentNo","UWNetID","LastName","FirstName","Pronouns"];
        if (showJointCourse) {  // MUWM-4348
          header.push("Joint Course");
        }
        if (hasLinkedSections) {
            header.push("LinkedSection");
            }
        header.push("Credits","Class","Major","Email");
        lines.push(header.join(","));

        for (let i = 0; i < registrations.length; i++) {
            const reg = registrations[i];
            if (reg.isJoint && !showJointCourse) {  //MUWM-4371, // MUWM-4348
                continue;
            }
            const fields = [
              "\t" + reg.student_number,  // MUWM-3978
              reg.netid,
              reg.surname,
              reg.first_name,
              reg.pronouns];
            if (showJointCourse) {  // MUWM-4348
              fields.push(reg.isJoint ? reg.sectionLabel : section.label);
            }
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
    classlistFileName(section, showJointCourse) {
      let fn = section.section_label;
      if (showJointCourse) {
        fn += "_joint";
      } 
      fn += '_students.csv';
      return fn.replace(/[^a-z0-9._]/ig, '_');
    },
    downloadClassList(section, showJointCourse) {
      const hiddenElement = document.createElement('a');
      const csvData = this.buildClasslistCsv(section, showJointCourse);
      hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvData); // MUWM-5004
      hiddenElement.target = '_blank';
      hiddenElement.download = this.classlistFileName(section, showJointCourse);
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
      const el = document.getElementById(section.anchor);
      // console.log('Scrolling into view:', el);
      if (el && !el.classList.contains('scrolled')) {
        // MUWM-5320
        requestAnimationFrame(() => {
          el.scrollIntoView({ behavior: 'smooth' });
          el.classList.add('scrolled'); // mark it as scrolled
        });
      }
    },
    viewUWTBookUrl(bookSection) {
      // MUWM-5311, MUWM-5326
      return ("https://www.bkstr.com/webApp/discoverView?" +
        "bookstore_id-1=2335&div-1=" +
        "&term_id-1=" + bookSection.term +
        "&dept-1=" + encodeURIComponent(bookSection.curriculum.replace(" ", "-")) +
        "&course-1=" + bookSection.courseNumber +
        "&section-1=" + bookSection.sectionId);
    }
  },
}
