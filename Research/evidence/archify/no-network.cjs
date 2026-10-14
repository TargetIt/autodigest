// Research-only guard. Not an upstream Archify component or a security sandbox.
const fs = require('node:fs');
const { syncBuiltinESMExports } = require('node:module');
function deny(api) {
  return function () {
    fs.appendFileSync(process.env.ARCHIFY_RESEARCH_NETWORK_LOG, JSON.stringify({ api }) + '\n');
    throw new Error(`Research run prohibited network API: ${api}`);
  };
}
globalThis.fetch = deny('fetch');
for (const name of ['http', 'https']) {
  const mod = require('node:' + name);
  mod.request = deny(name + '.request');
  mod.get = deny(name + '.get');
}
require('node:net').Socket.prototype.connect = deny('net.Socket.connect');
require('node:dns').lookup = deny('dns.lookup');
require('node:dns/promises').lookup = deny('dns.promises.lookup');
syncBuiltinESMExports();
