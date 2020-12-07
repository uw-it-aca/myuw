import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

function postProcess(response, urlExtra) {
  let data = setTermAndExtractData(
    response, urlExtra.replace(/&amp;/g, "%26"));

  const sectionData = data[urlExtra];
  
  let section = sectionData.sections[0];
  sectionData.curric = section.curriculum_abbr;
  sectionData.courseNumber = section.course_number;
  sectionData.sectionId = section.section_id;
  
  if("joint_sections" in section) {
    let jointRegistrations = [];
  
    for (let i = 0; i < section.joint_sections.length; i++) {
      let jsection = section.joint_sections[i];
      for (let j = 0; j < jsection.registrations; j++) {
        let registration = jsection.registrations[j];
        registration.isJoint = true;
        registration.jointCurric = jsection.course_abbr;
        registration.jointCourseNumber = jsection.course_number;
        registration.jointSectionId = jsection.section_id;
      }
      jointRegistrations = jointRegistrations.concat(jsection.registrations);
    }
    section.registrations = section.registrations.concat(jointRegistrations);
  }
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
