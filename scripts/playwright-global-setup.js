const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const root = path.resolve(__dirname, '..');
const logsDir = path.join(root, 'lab15_deliverables');
const stateFile = path.join(logsDir, 'playwright-server-pids.json');
const python = path.join(root, '.venv', 'Scripts', 'python.exe');

async function waitUrl(url, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(url);
      if (response.ok) return true;
    } catch (_) {
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  }
  throw new Error(`Server belum siap: ${url}`);
}

async function isReachable(url) {
  try {
    const response = await fetch(url);
    return response.ok;
  } catch (_) {
    return false;
  }
}

function startProcess(name, args, cwd, stdoutName, stderrName) {
  fs.mkdirSync(logsDir, { recursive: true });
  const stdout = fs.openSync(path.join(logsDir, stdoutName), 'a');
  const stderr = fs.openSync(path.join(logsDir, stderrName), 'a');
  const child = spawn(python, args, {
    cwd,
    detached: false,
    stdio: ['ignore', stdout, stderr],
    windowsHide: true,
  });

  return child.pid;
}

module.exports = async () => {
  const started = [];
  const backendUrl = 'http://127.0.0.1:8000/accounts/login/';
  const frontendUrl = 'http://127.0.0.1:5500/smartcity_citizen_spa_24782087/index.html';

  if (!(await isReachable(backendUrl))) {
    const pid = startProcess(
      'backend',
      ['manage.py', 'runserver', '127.0.0.1:8000', '--noreload'],
      path.join(root, 'server_smartcity'),
      'backend_server.log',
      'backend_server.err'
    );
    started.push(pid);
  }

  if (!(await isReachable(frontendUrl))) {
    const pid = startProcess(
      'frontend',
      ['-m', 'http.server', '5500', '--bind', '127.0.0.1'],
      root,
      'frontend_server.log',
      'frontend_server.err'
    );
    started.push(pid);
  }

  fs.writeFileSync(stateFile, JSON.stringify({ pids: started }, null, 2));
  await waitUrl(backendUrl, 90000);
  await waitUrl(frontendUrl, 30000);
};
