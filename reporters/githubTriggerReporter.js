// reporters/githubTriggerReporter.js

class GitHubTriggerReporter {
  onBegin(config, suite) {
    console.log(
      `\nGitHub Trigger Reporter: ${suite.allTests().length} tests`
    );
  }

  onEnd(result) {
    console.log(
      `GitHub Trigger Reporter: ${result.status}`
    );
  }
}

module.exports = GitHubTriggerReporter;
