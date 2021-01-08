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
        const header = ["StudentNo","UWNetID","LastName","FirstName"];
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
              reg.first_name];

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
    downloadClassList(classlist) {
      const hiddenElement = document.createElement('a');
      const csvData = this.buildClasslistCsv(
          classlist.registrations, classlist.has_linked_sections);

      hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvData);
      hiddenElement.target = '_blank';
      hiddenElement.download = this.fileName();
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
      return ('SLN ' + section.sln + ': ' + section.curriculum_abbr + ' ' +
             section.course_number + ' ' + section.section_id);
    },
    idForSection(section) {
      return `${section.course_abbr_slug}-${section.course_number}-${section.section_id}`;
    },
    selfAnchored(section) {
      const el = document.getElementById(section.anchor);
      if (el) {
        el.scrollIntoView({behavior: 'smooth'});
      }
    }
  },
}
