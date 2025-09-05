// lighthouserc.cjs
require("dotenv").config();
const port = process.env.RUNSERVER_PORT;

module.exports = {
  ci: {
    collect: {
      settings: {
        //set which categories you want to run
        onlyCategories: ["accessibility"],
      },
      url: [
        // add URLs to be tested (usually matches /pages structure)
        `http://localhost:${port}/`,
        `http://localhost:${port}/academics`,
        `http://localhost:${port}/husky_experience`,
        `http://localhost:${port}/accounts`,
        `http://localhost:${port}/notices`,
        `http://localhost:${port}/profile`,
        `http://localhost:${port}/academic_calendar`,
        `http://localhost:${port}/resources`,
      ],
      // specify other options like numberOfRuns, staticDistDir, etc.
      numberOfRuns: 1,
    },
    // add assert, upload, and other configuration as required
    assert: {},
    upload: {},
    server: {},
    wizard: {},
  },
};
