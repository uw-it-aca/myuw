export default {
  methods: {
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
