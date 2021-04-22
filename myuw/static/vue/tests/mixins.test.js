import utils from '../mixins/utils'
import courses from '../mixins/courses';

it('titleCaseWord', () => {
  expect(utils.methods.titleCaseWord('TEST')).toEqual('Test');
  expect(utils.methods.titleCaseWord('string STRING')).toEqual('String string');
});

it('titleCaseName', () => {
  expect(utils.methods.titleCaseName('WORD A WORD')).toEqual('Word A Word');
  expect(utils.methods.titleCaseName('string string')).toEqual('String String');
});

it('strToDayjs', () => {
	expect(utils.methods.strToDayjs("2021-04-22T15:30:00-07:00").toISOString()
	).toEqual("2021-04-22T22:30:00.000Z");
	expect(utils.methods.strToDayjs("2013-04-10").toISOString()
	).toEqual("2013-04-10T07:00:00.000Z");
});
it('formatDateRange', () => {
  expect(utils.methods.formatDateRange(
		utils.methods.strToDayjs("2021-04-12"),
		utils.methods.strToDayjs("2021-04-12"))
	).toEqual('Apr 12');
	expect(utils.methods.formatDateRange(
		utils.methods.strToDayjs("2021-04-12"),
		utils.methods.strToDayjs("2021-04-14"))
	).toEqual('Apr 12 - 14');
	expect(utils.methods.formatDateRange(
		utils.methods.strToDayjs("2021-04-12"),
		utils.methods.strToDayjs("2021-05-14"))
	).toEqual('Apr 12 - May 14');
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

