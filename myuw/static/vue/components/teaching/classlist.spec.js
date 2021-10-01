import { mount } from '@cypress/vue';
import faker from 'faker';
import Vuex from 'vuex';

import classlist from '../../vuex/store/classlist';

import courseMixin from '../../mixins/courses';

import StudentList from './classlist/class-student-list.vue';

faker.seed(0);

function generatePerson() {
  // Need more? It think there is also a third slash there
  const PRONOUNS = [
    'he/him',
    'she/her',
    'them/they',
  ];
  const CLASSLEVELS = [
    'FRESHMAN',
    'SOPHOMORE',
    'JUNIOR',
    'SENIOR',
    // 'GRADUATE', is this one valid?
  ];

  let person = {
    firstName: faker.name.firstName(),
    lastName: faker.name.lastName(),
    pronouns: faker.random.arrayElement(PRONOUNS),
    studentNumber: faker.datatype.number(),
    classLevel: faker.random.arrayElement(CLASSLEVELS),
    email: faker.internet.email(),
    avatar: faker.internet.avatar(),
  };

  person.netid = (
    person.firstName.substr(0, 3) +
    person.lastName.substr(0, 3)
  ).toLocaleLowerCase();

  return person;
}

function generateMajor() {
  const MAJORS = [
    'Premajor',
    'UPCOM',
    'PHYS',
    'ESS',
    'CSE',
  ];
  const CAMPUS = [
    'Seattle Campus',
    'Tacoma Campus',
    'Bothell Campus',
  ];

  let major = faker.random.arrayElement(MAJORS);
  return {
    name: major,
    full_name: `${major} (${faker.random.arrayElement(CAMPUS)})`,
  };
}

/**
 * Generates the following schema
 * {
 *   netid: string,
 *   pronouns: string,
 *   student_number: string,
 *   credits: string,
 *   is_auditor: boolean,
 *   is_independent_start: boolean,
 *   class_level: string,
 *   email: string,
 *   start_date: string,
 *   end_date: string,
 *   first_name: string,
 *   surname: string,
 *   majors: [
 *     {
 *       name: string,
 *       full_name: string,
 *     },
 *     ...
 *   ],
 *   linked_sections: string,
 *   url_key: string,
 * }
 */
function generateRegistration(
  person,
  majors,
  credits = 5.0,
  linkedSections = "",
  isAuditor = false,
  independentStart = { startDate: "", endDate: "" },
) {
  let reg = {
    netid: person.netid,
    pronouns: person.pronouns,
    student_number: person.studentNumber.toString(),
    credits: credits,
    is_auditor: isAuditor,
    is_independent_start: !!independentStart.startDate && !!independentStart.endDate,
    class_level: person.classLevel,
    email: person.email,
    start_date: independentStart.startDate,
    end_date: independentStart.endDate,
    first_name: person.firstName,
    surname: person.lastName,
    majors: majors,
    linked_sections: linkedSections,
    url_key: faker.datatype.uuid(),
  };

  return reg;
}

function deepcopy(data) { return JSON.parse(JSON.stringify(data)); }

describe('<CourseCards />', () => {
  let people = Array.from({length: 25}, () => generatePerson());
  let registrations = people.map((person) => {
    return generateRegistration(
      person,
      [generateMajor()],
    );
  });

  beforeEach(() => {
    cy.viewport(1280, 720);
  });

  it('Course Cards', () => {
    const SECTION_LABEL = '2013,spring,ESS,102/A';

    cy.fixture('classlist/2013-spring-ESS-102-A.json').then((json) => {
      json.sections[0].registrations = json.sections[0].registrations.concat(deepcopy(registrations));
      cy.intercept('GET', `/api/v1/instructor_section_details/${SECTION_LABEL}`, json);
      json.sections[0].registrations.forEach((reg) => {
        cy.intercept('GET', `/photo/${reg.url_key}`, {fixture: 'images/mock.jpg'});
      });
    });

    cy.createLocalVue(Vuex).then((localVue) => {
      localVue.mixin(courseMixin);
      let store = new Vuex.Store({
        modules: {
          classlist,
        },
        state: {
          user: {
            affiliations: {
              instructor: true,
            },
          }
        },
      });

      mount(StudentList, {store, localVue, propsData: {sectionLabel: SECTION_LABEL}}).then(() => {
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);
        // TODO: take image snapshot here
      });
    });
  });
});