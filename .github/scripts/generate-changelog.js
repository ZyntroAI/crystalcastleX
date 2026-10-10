#!/usr/bin/env node
/**
 * Update docs/CHANGELOG.md from recent git commits.
 * Usage: node update-changelog.js [commitCount]
 */
const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const COMMIT_COUNT = Number(process.argv[2]) || 10;
const OUTPUT_FILE = path.resolve(process.cwd(), "docs", "CHANGELOG.md");
const TODAY = new Date().toISOString().slice(0, 10);

function runGit(cmd) {
  try {
    return execSync(cmd, {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
    }).trim();
  } catch (err) {
    console.error("Git error:", err.stderr || err.message);
    process.exit(1);
  }
}

// --no-merges skips merge commits; tab-separate subject + hash for safe parsing
const raw = runGit(
  `git log --no-merges --pretty=format:"%s%x09%h" -n ${COMMIT_COUNT}`
);

if (!raw) {
  console.log("No commits found — nothing to update.");
  process.exit(0);
}

const entries = raw
  .split("\n")
  .map((line) => {
    const [subject, hash] = line.split("\t");
    const safe = subject.replace(/`/g, "\\`"); // avoid breaking markdown
    return `- ${safe} (\`${hash}\`)`;
  })
  .join("\n");

const newSection = `## ${TODAY}\n\n${entries}\n`;

// Load existing log, strip header + any older section for today
let rest = "";
if (fs.existsSync(OUTPUT_FILE)) {
  const existing = fs.readFileSync(OUTPUT_FILE, "utf8");
  rest = existing
    .replace(/^# CHANGELOG\s*\n?/, "")
    .replace(new RegExp(`## ${TODAY}[\\s\\S]*?(?=\\n## |$)`), "")
    .trim();
}

fs.mkdirSync(path.dirname(OUTPUT_FILE), { recursive: true });

const content = `# CHANGELOG\n\n${newSection}${rest ? "\n" + rest + "\n" : ""}`;
fs.writeFileSync(OUTPUT_FILE, content, "utf8");

console.log(`Updated ${OUTPUT_FILE} with ${COMMIT_COUNT} commit(s).`);
