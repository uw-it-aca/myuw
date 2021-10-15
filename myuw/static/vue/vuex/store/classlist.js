import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

function compareFn (a, b) {
  // sort by Last name then First name
  let aLname = a.surname.toUpperCase();
  let bLname = b.surname.toUpperCase();
  if (aLname < bLname) {
      return -1;
  }
  if(aLname > bLname) {
      return 1;
  }
  let aFname = a.first_name.toUpperCase();
  let bFname = b.first_name.toUpperCase();
  if (aFname < bFname) {
      return -1;
  }
  if(aFname > bFname) {
      return 1;
  }
  return 0;
}

function postProcess(response, sectionLabel) {
  const urlExtra = sectionLabel.replace(/&amp;/g, '%26');
  let data = setTermAndExtractData(response, urlExtra);

  const sectionData = data[urlExtra];
  const section = sectionData.sections[0];
  section.year = sectionData.year;
  section.quarter = sectionData.quarter;
  sectionData.currAbbr = section.curriculum_abbr;
  sectionData.courseNum = section.course_number;
  sectionData.sectionId = section.section_id;
  sectionData.sln = section.sln;
  section.anchor = (section.course_abbr_slug + "-" +
    section.course_number + "-" + section.section_id);
  section.label = (section.curriculum_abbr + ' ' +
    section.course_number + ' ' + section.section_id);

  if("joint_sections" in section) {
    let jointRegistrations = [];
    for (let i = 0; i < section.joint_sections.length; i++) {
      const jsection = section.joint_sections[i];
      jsection.label = (jsection.course_abbr + ' ' +
        jsection.course_number + ' ' + jsection.section_id);
      jsection.url = (section.year + ',' + section.quarter + ',' +
        jsection.course_abbr + "," + jsection.course_number + "/" +
        jsection.section_id).replace(/&amp;/g, '%26');
      jsection.registrations.forEach(function(reg){
        reg.isJoint = true;
        reg.sectionLabel = jsection.label;
      });
      jointRegistrations = jointRegistrations.concat(jsection.registrations);
    }
    section.registrations = section.registrations.concat(jointRegistrations);
  }
  section.registrations = section.registrations.sort(compareFn);
  return data;
}

const customActions = {
  fetch: fetchBuilder(
    "/api/v1/instructor_section_details/",
    postProcess,
    'json'
  ),
};

export default buildWith(
  { customActions },
);
