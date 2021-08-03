import axios from 'axios';
import utils from '../mixins/utils'
import courses from '../mixins/courses';
import sortc from '../mixins/sort-compare';

import mockNotices from './mock_data/notice/javerage.json';

jest.mock('axios');

describe('mixins', () => {
  it('isUndefinedOrNull', () => {
    expect(sortc.methods.isUndefinedOrNull(null)).toEqual(true);
    expect(sortc.methods.isUndefinedOrNull(undefined)).toEqual(true);
    expect(sortc.methods.isUndefinedOrNull(1)).toEqual(false);
    expect(sortc.methods.isUndefinedOrNull('abc')).toEqual(false);
  });

  it('normalizeValue', () => {
    expect(sortc.methods.normalizeValue(null)).toEqual("");
    expect(sortc.methods.normalizeValue(undefined)).toEqual("");
    expect(sortc.methods.normalizeValue(1)).toEqual(1.00);
    expect(sortc.methods.normalizeValue("1,000")).toEqual(1000.00);
    expect(sortc.methods.normalizeValue('abc')).toEqual("abc");
  });

  it('defaultSortCompare', () => {
    const options = { sortByField: 'a' };
    // sorts numbers correctly
    expect(sortc.methods.defaultSortCompare({ a: 1 }, { a: 2 }, options)).toBe(-1);
    expect(sortc.methods.defaultSortCompare({ a: 2 }, { a: 1 }, options)).toBe(1);
    expect(sortc.methods.defaultSortCompare({ a: 1 }, { a: 1 }, options)).toBe(0);
    expect(sortc.methods.defaultSortCompare({ a: -1 }, { a: 1 }, options)).toBe(-1);
    expect(sortc.methods.defaultSortCompare({ a: 1 }, { a: -1 }, options)).toBe(1);
    expect(sortc.methods.defaultSortCompare({ a: 0 }, { a: 0 }, options)).toBe(0);
    expect(sortc.methods.defaultSortCompare({ a: 1.234 }, { a: 1.567 }, options)).toBe(-1);
    expect(sortc.methods.defaultSortCompare({ a: 1.561 }, { a: 1.234 }, options)).toBe(1);

    // sorts date strings correctly
    const date1 = { a: new Date(2020, 1, 1).toISOString() };
    console.log(date1);
    const date2 = { a: new Date(1999, 11, 31).toISOString() };
    const date3 = { a: new Date(1999, 1, 1).toISOString() };
    const date4 = { a: new Date(1999, 1, 1, 12, 12, 12, 12).toISOString() };
    expect(sortc.methods.defaultSortCompare(date1, date2, options)).toBe(1);
    expect(sortc.methods.defaultSortCompare(date1, date1, options)).toBe(0);
    expect(sortc.methods.defaultSortCompare(date2, date1, options)).toBe(-1);
    expect(sortc.methods.defaultSortCompare(date2, date3, options)).toBe(1);
    expect(sortc.methods.defaultSortCompare(date3, date2, options)).toBe(-1);
    expect(sortc.methods.defaultSortCompare(date3, date4, options)).toBe(-1);
    expect(sortc.methods.defaultSortCompare(date4, date3, options)).toBe(1);
    expect(sortc.methods.defaultSortCompare(date4, date4, options)).toBe(0);

    //sorts strings correctly
    expect(sortc.methods.defaultSortCompare({ a: 'a' }, { a: 'b' }, options)).toBe(-1);
    expect(sortc.methods.defaultSortCompare({ a: 'b' }, { a: 'a' }, options)).toBe(1);
    expect(sortc.methods.defaultSortCompare({ a: 'a' }, { a: 'a' }, options)).toBe(0);
    expect(sortc.methods.defaultSortCompare({ a: 'a' }, { a: 'aaa' }, options)).toBe(-1);
    expect(sortc.methods.defaultSortCompare({ a: 'aaa' }, { a: 'a' }, options)).toBe(1);

    //sorts nulls always last
    options.nullLast = true;
    expect(sortc.methods.defaultSortCompare({ a: 'a' }, { a: undefined }, options)).toBe(-1);
    expect(sortc.methods.defaultSortCompare({ a: null }, { a: 'a' }, options)).toBe(1);
  });

  it('titleCaseWord', () => {
    expect(utils.methods.titleCaseWord(null)).toEqual("");
    expect(utils.methods.titleCaseWord('TEST')).toEqual('Test');
    expect(utils.methods.titleCaseWord('string STRING')).toEqual('String string');
  });

  it('titleCaseName', () => {
    expect(utils.methods.titleCaseName('WORD A WORD')).toEqual('Word A Word');
    expect(utils.methods.titleCaseName('string string')).toEqual('String String');
  });

  it('capitalizeString', () => {
    expect(utils.methods.capitalizeString('b-term')).toEqual('B-Term');
    expect(utils.methods.capitalizeString('spring')).toEqual('Spring');
    expect(utils.methods.capitalizeString('SPRING')).toEqual('Spring');
    expect(utils.methods.capitalizeString('')).toEqual('');
    expect(utils.methods.capitalizeString(null)).toEqual('');
  });

  it('pageTitleFromTerm', () => {
    expect(utils.methods.pageTitleFromTerm('2013,summer,a-term')).toEqual("Summer 2013 A-Term");
    expect(utils.methods.pageTitleFromTerm("2013,spring")).toEqual('Spring 2013');
    expect(utils.methods.pageTitleFromTerm(null)).toEqual('');
  });

  it('formatDateRange', () => {
    expect(utils.methods.formatDateRange(
      utils.methods.dayjs("2021-04-12"),
      utils.methods.dayjs("2021-04-12"))
    ).toEqual('Apr 12');
    expect(utils.methods.formatDateRange(
      utils.methods.dayjs("2021-04-12"),
      utils.methods.dayjs("2021-04-14"))
    ).toEqual('Apr 12 - 14');
    expect(utils.methods.formatDateRange(
      utils.methods.dayjs("2021-04-12"),
      utils.methods.dayjs("2021-05-14"))
    ).toEqual('Apr 12 - May 14');
    expect(utils.methods.formatDateRange(
      utils.methods.dayjs("2021-04-12"), null)
    ).toEqual('Apr 12');
  });

  it('toFromNowDate', async () => {
    axios.get.mockResolvedValue({data: mockNotices});
    expect(utils.methods.toFromNowDate()).toEqual('');
    expect(utils.methods.toFromNowDate('')).toEqual('');

    const now = utils.methods.dayjs();
    const format = 'YYYY-MM-DD';
    expect(utils.methods.toFromNowDate(now.subtract(1, 'd').format(format)))
      .toEqual('a day ago');
    expect(utils.methods.toFromNowDate(now.add(1, 'd').format(format)))
      .toEqual('in a day');
    expect(utils.methods.toFromNowDate(now.subtract(5, 'd').format(format)))
      .toEqual('5 days ago');
    expect(utils.methods.toFromNowDate(now.add(5, 'd').format(format)))
      .toEqual('in 5 days');
    expect(utils.methods.toFromNowDate(now.subtract(1, 'M').format(format)))
      .toEqual('a month ago');
    expect(utils.methods.toFromNowDate(now.add(1, 'M').format(format)))
      .toEqual('in a month');
    expect(utils.methods.toFromNowDate(now.subtract(5, 'M').format(format)))
      .toEqual('5 months ago');
    expect(utils.methods.toFromNowDate(now.add(5, 'M').format(format)))
      .toEqual('in 5 months');
  });

  it('formatPhoneNumberLink', () => {
    expect(utils.methods.formatPhoneNumberLink("+1 206 543-0000")).toEqual('+1-206-543-0000');
    expect(utils.methods.formatPhoneNumberLink("425-666-6666")).toEqual('+1-425-666-6666');
    expect(utils.methods.formatPhoneNumberLink("")).toEqual("");
  });

  it('formatMeetingTime', () => {
    expect(utils.methods.formatMeetingTime("09:30")).toEqual("9:30 AM");
    expect(utils.methods.formatMeetingTime("14:00")).toEqual('2:00 PM');
  });

  it('toCalendar', () => {
    expect(utils.methods.toCalendar("20130301")).toEqual("03/01/2013");
    expect(utils.methods.toCalendar("10/01/2013")).toEqual("10/01/2013");
    expect(utils.methods.toCalendar("")).toEqual("");
  });

  it('formatPrice', () => {
    expect(utils.methods.formatPrice("0.1")).toEqual("0.10");
    expect(utils.methods.formatPrice("12")).toEqual('12.00');
  });

  it('hasAnyKeys', () => {
    const object1 = {
      a: 'somestring',
      b: 42
    };
    expect(utils.methods.hasAnyKeys(object1)).toBe(true);
    expect(utils.methods.hasAnyKeys({})).toEqual(false);
  });
  it('degreeListString', () => {
    const majors = [
      {"abbr": "ASL",
       "campus": "Tacoma",
       "name": "AMERICAN SIGN LANGUAGE",
       "full_name": "American Sign Language",
       "short_name": "ASL"},
     {"abbr": "POL SCI",
      "campus": "Tacoma",
      "name": "POLITICAL SCIENCE",
      "full_name": "Political Science",
      "short_name": "POL SCI"}
    ];
    expect(utils.methods.degreeListString(majors)).toBe(
      "American Sign Language, Political Science"
    );
  });
  it('buildClasslistCsv', () => {
  {
    const registrations = [
      {
        "netid": "w1",
        "student_number": "0000001",
        "credits": "5.0",
        "is_auditor": false,
        "class_level": "SENIOR",
        "email": "w1@uw.edu",
        "first_name": "Ma El",
        "surname": "We",
        "pronouns": null,
        "majors": [
          {
            "name": "SOCIOLOGY",
            "full_name": "Sociology",
          }
        ],
        "linked_sections": "AA"
      },
      {
        "netid": "f1",
        "student_number": "0000002",
        "credits": "5.0",
        "is_auditor": false,
        "class_level": "SENIOR",
        "email": "f1@uw.edu",
        "first_name": "Fa",
        "surname": "Or",
        "pronouns": null,
        "majors": [
          {
            "name": "BIOENGINEERING",
          },
          {
            "full_name": "Sociology",
          }
        ],
        "linked_sections": "AB"
      },
      {
        "netid": "a1",
        "student_number": "0000003",
        "credits": "5.0",
        "is_auditor": false,
        "class_level": "SENIOR",
        "email": "a1@uw.edu",
        "first_name": "Al",
        "surname": "Di",
        "pronouns": "her",
        "majors": [
          {
            "full_name": "Sociology",
          }
        ],
        "linked_sections": "AA"
      },
      {
        "netid": "h1",
        "student_number": "0000004",
        "credits": "5.0",
        "is_auditor": false,
        "class_level": "SENIOR",
        "email": "h1@uw.edu",
        "first_name": "Ha Pe",
        "surname": "Ru",
        "pronouns": "his",
        "majors": [
      {
      "name": "POLITICAL SCIENCE",
      "full_name": "Political, Science",
      },
          {
            "name": "SOCIOLOGY"
          }
        ],
        "linked_sections": "AC"
      }
    ];
    const csvD = courses.methods.buildClasslistCsv(registrations, true);
    expect(csvD).toEqual(
      "StudentNo,UWNetID,LastName,FirstName,Pronouns,LinkedSection,Credits,Class,Major,Email\n" +
      "\"\t0000001\",\"w1\",\"We\",\"Ma El\",\"\",\"AA\",\"5.0\",\"SENIOR\",\"Sociology\",\"w1@uw.edu\"\n" +
      "\"\t0000002\",\"f1\",\"Or\",\"Fa\",\"\",\"AB\",\"5.0\",\"SENIOR\",\"Bioengineering, Sociology\",\"f1@uw.edu\"\n" +
      "\"\t0000003\",\"a1\",\"Di\",\"Al\",\"her\",\"AA\",\"5.0\",\"SENIOR\",\"Sociology\",\"a1@uw.edu\"\n" +
      "\"\t0000004\",\"h1\",\"Ru\",\"Ha Pe\",\"his\",\"AC\",\"5.0\",\"SENIOR\",\"Political Science, Sociology\",\"h1@uw.edu\""
      );
    }
  });
})
