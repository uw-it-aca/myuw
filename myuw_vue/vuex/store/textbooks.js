import {fetchBuilder, extractData, buildWith} from './model_builder';
import {
  bothellCampus,
  tacomaCampus,
  termId,
} from './common';
const customActions = {
  fetch: fetchBuilder('/api/v1/book/', extractData, 'json'),
};

const customGetters = {
  getProcessedData: (state) => (courseData, instructedCourseData) => {
    let bookData = state.value;
    const processedData = {
      teachingSections: [],
      enrolledSections: [],
      sections: [],
      quarter: courseData ? courseData.quarter : instructedCourseData.quarter,
      year: courseData ? courseData.year: instructedCourseData.year,
      summerTerm: courseData ? courseData.summer_term : instructedCourseData.summer_term,
      orderUrl: bookData.order_url
    }

    function makeSectionData(i, section, isInstructor) {
      return {
        index: i,
        sectionTitle: section.course_title,
        curriculum: section.curriculum_abbr,
        courseNumber: section.course_number,
        sectionId: section.section_id,
        colorId: section.color_id,
        sln: section.sln,
        bookData: bookData ? bookData[section.sln] : {},
        isInstructor: isInstructor,
        bothellCampus: bothellCampus(section),
        tacomaCampus: tacomaCampus(section),
        term: String(section.year) + termId(section.quarter),
      }
    }

    if (courseData) {
      courseData.sections.forEach((section, i) => {
        const sectionBook = makeSectionData(i, section, false);
        processedData.enrolledSections.push(sectionBook);
        processedData.sections.push(sectionBook);
      })
    }

    if (instructedCourseData) {
      instructedCourseData.sections.forEach((section, i) => {
        const sectionBook = makeSectionData(i, section, true);
        processedData.teachingSections.push(sectionBook);
        processedData.sections.push(sectionBook);
      })
    }

    // Determine if we need to collapse the textbook sections and whether the user is teaching
    const numSections = (
      processedData.enrolledSections.length +
      processedData.teachingSections.length
    )
    processedData.collapseSections = numSections > 10;
    processedData.hasTeachingSections = processedData.teachingSections.length > 0;
    return processedData;
  }
}

export default buildWith(
  {customActions, customGetters}
);