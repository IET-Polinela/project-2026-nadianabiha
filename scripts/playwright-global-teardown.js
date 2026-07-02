const fs = require('fs');
const path = require('path');

const stateFile = path.join(__dirname, '..', 'lab15_deliverables', 'playwright-server-pids.json');

module.exports = async () => {
  if (!fs.existsSync(stateFile)) return;
  const { pids = [] } = JSON.parse(fs.readFileSync(stateFile, 'utf8'));

  for (const pid of pids) {
    try {
      process.kill(pid);
    } catch (_) {
      // Process may already have exited.
    }
  }

  fs.rmSync(stateFile, { force: true });
};
