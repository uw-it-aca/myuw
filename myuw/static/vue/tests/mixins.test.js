import axios from 'axios';
import utils from '../mixins/utils'
import courses from '../mixins/courses';

import mockNotices from './mock_data/notice/javerage.json';

jest.mock('axios');

describe('mixins', () => {
  it('titleCaseWord', () => {
    expect(utils.methods.titleCaseWord('TEST')).toEqual('Test');
    expect(utils.methods.titleCaseWord('string STRING')).toEqual('String string');
  });

  it('titleCaseName', () => {
    expect(utils.methods.titleCaseName('WORD A WORD')).toEqual('Word A Word');
    expect(utils.methods.titleCaseName('string string')).toEqual('String String');
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
