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
