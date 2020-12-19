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
        let mj = majors[j];
        if (mj.name) {
          rmajors.push(this.titleCaseName(mj.name));
        }
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
    getTimeScheHref(section) {
      const qAbb = (!section.quarter || section.quarter.length === 0) ?
            '' : section.quarter.substring(0, 3).toUpperCase();
      return ('http://sdb.admin.uw.edu/timeschd/uwnetid/sln.asp?QTRYR=' +
              qAbb + '+' + section.year + '&SLN=' + section.sln);
    },
    getTimeScheLinkLable(section) {
      return ('SLN ' + section.sln + ': ' + section.curriculum_abbr + ' ' +
             section.course_number + ' ' + section.section_id);
    },
  },
}
