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

    //sorts strings correctly
    expect(sortc.methods.defaultSortCompare({ a: 'a' }, { a: 'b' }, options)).toBe(-1);
    expect(sortc.methods.defaultSortCompare({ a: 'Bao' }, { a: 'Ab' }, options)).toBe(1);
    expect(sortc.methods.defaultSortCompare({ a: 'A' }, { a: 'a' }, options)).toBe(-1);
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
    expect(utils.methods.titleCaseName(null)).toEqual("");
    expect(utils.methods.titleCaseName("")).toEqual("");
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
  it('toFriendlyDate', () => {
    expect(
      utils.methods.toFriendlyDate('2020-08-24 00:00:00-08:00')
    ).toEqual('Mon, Aug 24');
    expect(
      utils.methods.toFriendlyDate(undefined)
    ).toEqual('');
    expect(
      utils.methods.toFriendlyDate('')
    ).toEqual('');
  });
  it('toFriendlyDatetime', () => {
    expect(
      utils.methods.toFriendlyDatetime('2013-04-17 16:00:00-08:00')
    ).toEqual('Thu, Apr 18, 12:00AM');
    expect(
      utils.methods.toFriendlyDatetime(undefined)
    ).toEqual('');
    expect(
      utils.methods.toFriendlyDatetime('')
    ).toEqual('');
  });
  it('timeDeltaFrom', async () => {
    const now = utils.methods.dayjs();
    expect(utils.methods.timeDeltaFrom(now.add(1, 'h').toISOString(), 'day', false)).toEqual(1);
    expect(utils.methods.timeDeltaFrom(now.add(24, 'h').toISOString(), 'day', false)).toEqual(1);
    expect(utils.methods.timeDeltaFrom(now.add(25, 'h').toISOString(), 'day', false)).toEqual(2);
    expect(
      utils.methods.timeDeltaFrom(now.subtract(1, 'd').toISOString(), 'day', false)).toEqual(-1);
  });
  it('toFromNowDate', async () => {
    expect(utils.methods.toFromNowDate()).toEqual('');
    expect(utils.methods.toFromNowDate('')).toEqual('');

    const now = utils.methods.dayjs();
    expect(utils.methods.toFromNowDate(now.subtract(1, 'd').toISOString(), false))
      .toEqual('a day ago');
    expect(utils.methods.toFromNowDate(now.toISOString(), false))
      .toEqual('Today');
    expect(utils.methods.toFromNowDate(now.add(1, 'd').toISOString(), false))
      .toEqual('Tomorrow');
    expect(utils.methods.toFromNowDate(now.subtract(5, 'd').toISOString(), false))
      .toEqual('5 days ago');
    expect(utils.methods.toFromNowDate(now.add(5, 'd').toISOString(), false))
      .toEqual('in 4 days');
  });

  it('hasPassed', async () => {
    expect(utils.methods.hasPassed()).toEqual(false);
    expect(utils.methods.hasPassed('')).toEqual(false);
    const now = utils.methods.dayjs();
    expect(utils.methods.hasPassed(now.subtract(1, 'd').toISOString(), false))
      .toEqual(true);
    expect(utils.methods.hasPassed(now.add(1, 'd').toISOString(), false))
      .toEqual(false);
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
  it('isPreMajor', () => {
    expect(utils.methods.isPreMajor("PRE ARTS")).toBe(true);
    expect(utils.methods.isPreMajor("EXTND PREMAJOR (BOTHELL)")).toBe(true);
    expect(utils.methods.isPreMajor("PREMAJOR (TACOMA)")).toBe(true);
    expect(utils.methods.isPreMajor("EXTENDED PRE ENGINEERING")).toBe(true);
    expect(utils.methods.isPreMajor("PRE-HLTHCARE LD (TACOMA)")).toBe(true);
    expect(utils.methods.isPreMajor("WOMEN STUDIES")).toBe(false);
  }),
  it('noDeclaredMajor', () => {
    expect(utils.methods.noDeclaredMajor(null)).toBe(true);
    let TermMajors = [
      {
        "quarter": "summer",
        "year": 2023,
        "majors": [
          {
            "name": "BIOLOGY",
            "full_name": "Biology",
            "short_name": "BIOL"
          }
        ]
      },
      {
        "quarter": "autumn",
        "year": 2023,
        "majors": [
          {
            "name": "EXTENDED PRE MAJOR",
            "full_name": "Extended Pre Major",
            "short_name": "EXT PRE MAJ"
          }
        ]
      }
    ];
    expect(utils.methods.noDeclaredMajor(TermMajors)).toBe(true);
    TermMajors.push(
      {
        "quarter": "summer",
        "year": 2023,
        "majors": [
          {
            "name": "STATISTICS",
            "full_name": "Statistics",
            "short_name": "STATISTICS"
          }
        ]
      }
    );
    expect(utils.methods.noDeclaredMajor(TermMajors)).toBe(false);
  });
  it('buildClasslistCsv', () => {
  {
    const section = {
      "has_linked_sections": true,
      "registrations": [
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
        },
        {
          "netid": "q1",
          "student_number": "0000005",
          "credits": "5.0",
          "is_auditor": false,
          "class_level": "SENIOR",
          "email": "q1@uw.edu",
          "first_name": "Ha Pe",
          "surname": "Ru",
          "pronouns": "his",
          "majors": [
            {"degree_abbr": null,
            "college_abbr": "BOTHL",
            "college_full_name": "BOTHL",
            "degree_level": 1,
            "degree_name": null,
            "campus": "Bothell",
            "name": null,
            "full_name": null,
            "short_name": null
            }],
          "class_code": 4,
          "linked_sections": ""
        }
      ]
    };
    const csvD = courses.methods.buildClasslistCsv(section, false);
    expect(csvD).toEqual(
      "StudentNo,UWNetID,LastName,FirstName,Pronouns,LinkedSection,Credits,Class,Major,Email\n" +
      "\"\t0000001\",\"w1\",\"We\",\"Ma El\",\"\",\"AA\",\"5.0\",\"SENIOR\",\"Sociology\",\"w1@uw.edu\"\n" +
      "\"\t0000002\",\"f1\",\"Or\",\"Fa\",\"\",\"AB\",\"5.0\",\"SENIOR\",\"Bioengineering, Sociology\",\"f1@uw.edu\"\n" +
      "\"\t0000003\",\"a1\",\"Di\",\"Al\",\"her\",\"AA\",\"5.0\",\"SENIOR\",\"Sociology\",\"a1@uw.edu\"\n" +
      "\"\t0000004\",\"h1\",\"Ru\",\"Ha Pe\",\"his\",\"AC\",\"5.0\",\"SENIOR\",\"Political Science, Sociology\",\"h1@uw.edu\"\n" +
      "\"\t0000005\",\"q1\",\"Ru\",\"Ha Pe\",\"his\",\"\",\"5.0\",\"SENIOR\",\"\",\"q1@uw.edu\""
      );
    }
  });

  it('classesToClassDict', () => {
    expect(utils.methods.classesToClassDict("mock-class-1 mock-class-2")).toStrictEqual(
      {"mock-class-1": true, "mock-class-2": true}
    );
    expect(utils.methods.classesToClassDict(["mock-class-1", "mock-class-2"])).toStrictEqual(
      {"mock-class-1": true, "mock-class-2": true}
    );
    let mockClasses = {"mock-class-1": true, "mock-class-2": true}
    expect(utils.methods.classesToClassDict(mockClasses)).toStrictEqual(
      {"mock-class-1": true, "mock-class-2": true}
    );
  });
})
