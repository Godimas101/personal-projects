const fs = require('fs');
const crypto = require('crypto');

const file = 'C:\\Users\\Chris Carpenter\\VS Code Projects\\personal-projects\\health-tracking\\automatic-weight-tracking-workflow\\wyze-scale-weight-tracker.json';
let raw = fs.readFileSync(file, 'utf8');
if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
const wf = JSON.parse(raw);

// Pure-JS MD5 + HMAC-MD5 library
// KEY CHANGE vs previous version: hmacMd5(keyStr, msg) now treats keyStr as a
// plain string, encodes it as UTF-8 bytes � exactly what Python's str.encode()
// does in the Wyze SDK. We no longer hexToBytes() the key.
const pureJSLib = `
function _md5core(bytes){
  function safeAdd(x,y){const l=(x&0xffff)+(y&0xffff);return(((x>>16)+(y>>16)+(l>>16))<<16)|(l&0xffff);}
  function rol(n,c){return(n<<c)|(n>>>(32-c));}
  function cmn(q,a,b,x,s,t){return safeAdd(rol(safeAdd(safeAdd(a,q),safeAdd(x,t)),s),b);}
  function ff(a,b,c,d,x,s,t){return cmn((b&c)|((~b)&d),a,b,x,s,t);}
  function gg(a,b,c,d,x,s,t){return cmn((b&d)|(c&(~d)),a,b,x,s,t);}
  function hh(a,b,c,d,x,s,t){return cmn(b^c^d,a,b,x,s,t);}
  function ii(a,b,c,d,x,s,t){return cmn(c^(b|(~d)),a,b,x,s,t);}
  const padLen=(bytes.length%64<56)?(56-bytes.length%64):(120-bytes.length%64);
  const msg=bytes.concat([0x80]).concat(new Array(padLen-1).fill(0));
  const bitLen=bytes.length*8;
  msg.push(bitLen&0xff,(bitLen>>>8)&0xff,(bitLen>>>16)&0xff,(bitLen>>>24)&0xff,0,0,0,0);
  const blks=[];
  for(let i=0;i<msg.length;i+=4)blks.push(msg[i]|(msg[i+1]<<8)|(msg[i+2]<<16)|(msg[i+3]<<24));
  let a=1732584193,b=-271733879,c=-1732584194,d=271733878;
  for(let i=0;i<blks.length;i+=16){
    const[A,B,C,D]=[a,b,c,d];
    a=ff(a,b,c,d,blks[i+0],7,-680876936);d=ff(d,a,b,c,blks[i+1],12,-389564586);c=ff(c,d,a,b,blks[i+2],17,606105819);b=ff(b,c,d,a,blks[i+3],22,-1044525330);
    a=ff(a,b,c,d,blks[i+4],7,-176418897);d=ff(d,a,b,c,blks[i+5],12,1200080426);c=ff(c,d,a,b,blks[i+6],17,-1473231341);b=ff(b,c,d,a,blks[i+7],22,-45705983);
    a=ff(a,b,c,d,blks[i+8],7,1770035416);d=ff(d,a,b,c,blks[i+9],12,-1958414417);c=ff(c,d,a,b,blks[i+10],17,-42063);b=ff(b,c,d,a,blks[i+11],22,-1990404162);
    a=ff(a,b,c,d,blks[i+12],7,1804603682);d=ff(d,a,b,c,blks[i+13],12,-40341101);c=ff(c,d,a,b,blks[i+14],17,-1502002290);b=ff(b,c,d,a,blks[i+15],22,1236535329);
    a=gg(a,b,c,d,blks[i+1],5,-165796510);d=gg(d,a,b,c,blks[i+6],9,-1069501632);c=gg(c,d,a,b,blks[i+11],14,643717713);b=gg(b,c,d,a,blks[i+0],20,-373897302);
    a=gg(a,b,c,d,blks[i+5],5,-701558691);d=gg(d,a,b,c,blks[i+10],9,38016083);c=gg(c,d,a,b,blks[i+15],14,-660478335);b=gg(b,c,d,a,blks[i+4],20,-405537848);
    a=gg(a,b,c,d,blks[i+9],5,568446438);d=gg(d,a,b,c,blks[i+14],9,-1019803690);c=gg(c,d,a,b,blks[i+3],14,-187363961);b=gg(b,c,d,a,blks[i+8],20,1163531501);
    a=gg(a,b,c,d,blks[i+13],5,-1444681467);d=gg(d,a,b,c,blks[i+2],9,-51403784);c=gg(c,d,a,b,blks[i+7],14,1735328473);b=gg(b,c,d,a,blks[i+12],20,-1926607734);
    a=hh(a,b,c,d,blks[i+5],4,-378558);d=hh(d,a,b,c,blks[i+8],11,-2022574463);c=hh(c,d,a,b,blks[i+11],16,1839030562);b=hh(b,c,d,a,blks[i+14],23,-35309556);
    a=hh(a,b,c,d,blks[i+1],4,-1530992060);d=hh(d,a,b,c,blks[i+4],11,1272893353);c=hh(c,d,a,b,blks[i+7],16,-155497632);b=hh(b,c,d,a,blks[i+10],23,-1094730640);
    a=hh(a,b,c,d,blks[i+13],4,681279174);d=hh(d,a,b,c,blks[i+0],11,-358537222);c=hh(c,d,a,b,blks[i+3],16,-722521979);b=hh(b,c,d,a,blks[i+6],23,76029189);
    a=hh(a,b,c,d,blks[i+9],4,-640364487);d=hh(d,a,b,c,blks[i+12],11,-421815835);c=hh(c,d,a,b,blks[i+15],16,530742520);b=hh(b,c,d,a,blks[i+2],23,-995338651);
    a=ii(a,b,c,d,blks[i+0],6,-198630844);d=ii(d,a,b,c,blks[i+7],10,1126891415);c=ii(c,d,a,b,blks[i+14],15,-1416354905);b=ii(b,c,d,a,blks[i+5],21,-57434055);
    a=ii(a,b,c,d,blks[i+12],6,1700485571);d=ii(d,a,b,c,blks[i+3],10,-1894986606);c=ii(c,d,a,b,blks[i+10],15,-1051523);b=ii(b,c,d,a,blks[i+1],21,-2054922799);
    a=ii(a,b,c,d,blks[i+8],6,1873313359);d=ii(d,a,b,c,blks[i+15],10,-30611744);c=ii(c,d,a,b,blks[i+6],15,-1560198380);b=ii(b,c,d,a,blks[i+13],21,1309151649);
    a=ii(a,b,c,d,blks[i+4],6,-145523070);d=ii(d,a,b,c,blks[i+11],10,-1120210379);c=ii(c,d,a,b,blks[i+2],15,718787259);b=ii(b,c,d,a,blks[i+9],21,-343485551);
    a=safeAdd(a,A);b=safeAdd(b,B);c=safeAdd(c,C);d=safeAdd(d,D);
  }
  return [a,b,c,d].map(n=>{let s='';for(let j=0;j<4;j++)s+=('0'+((n>>>(j*8))&0xff).toString(16)).slice(-2);return s;}).join('');
}
function strToUtf8Bytes(s){
  const b=[];
  for(let i=0;i<s.length;i++){
    const c=s.charCodeAt(i);
    if(c<0x80)b.push(c);
    else if(c<0x800){b.push((c>>6)|0xc0);b.push((c&0x3f)|0x80);}
    else{b.push((c>>12)|0xe0);b.push(((c>>6)&0x3f)|0x80);b.push((c&0x3f)|0x80);}
  }
  return b;
}
function hexToBytes(hex){return hex.match(/../g).map(h=>parseInt(h,16));}
function md5(str){return _md5core(strToUtf8Bytes(str));}
function md5Bytes(bytes){return _md5core(bytes);}
// hmacMd5(keyStr, msg) � keyStr is treated as a plain string (ASCII/UTF-8),
// matching Python: hmac.new(str.encode(key_hex_str), msg_bytes, hashlib.md5)
function hmacMd5(keyStr, msg) {
  let kBytes = strToUtf8Bytes(keyStr);
  if (kBytes.length > 64) kBytes = hexToBytes(md5Bytes(kBytes));
  while (kBytes.length < 64) kBytes.push(0);
  const ipad = kBytes.map(b => b ^ 0x36);
  const opad = kBytes.map(b => b ^ 0x5c);
  const innerHex = _md5core(ipad.concat(strToUtf8Bytes(msg)));
  return md5Bytes(opad.concat(hexToBytes(innerHex)));
}
`.trim();

// Self-test: key is passed as a plain string, matching Python str.encode(md5_hex)
function md5ref(s){return crypto.createHash('md5').update(s,'utf8').digest('hex');}
function hmacRef(keyStr, m){
  // Python: hmac.new(str.encode(keyStr), str.encode(m), md5)
  return crypto.createHmac('md5', Buffer.from(keyStr,'utf8')).update(m,'utf8').digest('hex');
}
const testFn = new Function(pureJSLib + '\nreturn{md5,md5Bytes,hmacMd5};')();

const t1 = testFn.md5('hello') === md5ref('hello');
const t2 = testFn.md5(testFn.md5(testFn.md5('password123'))) === md5ref(md5ref(md5ref('password123')));
// HMAC tests (still needed for Prepare Scale Request)
const kStr1 = md5ref('wyze_app_secret_key_132');
const t3 = testFn.hmacMd5(kStr1, 'data') === hmacRef(kStr1, 'data');
const sj = '{"nonce":"1700000000000","email":"user@example.com","password":"abc123def456"}';
const kStr2 = md5ref('NoneNone');
const t4 = testFn.hmacMd5(kStr2, sj) === hmacRef(kStr2, sj);

console.log(`self-test md5:${t1} triple-md5:${t2} hmac1:${t3} hmac2:${t4}`);
if(!t1||!t2||!t3||!t4){console.error('SELF-TEST FAILED');process.exit(1);}

// ─────────────────────────────────────────────────────────────────────────────
// STRATEGY: Skip the Wyze HTTP login entirely.
// The Wyze auth API is unreliable from n8n (errorCode 1000 even with correct
// credentials). Instead, store WYZE_ACCESS_TOKEN + WYZE_USER_ID in .env
// (obtained once via test_wyze_login.py) and read them directly in the workflow.
// Access token lasts 2 days; re-run the Python script to refresh.
// ─────────────────────────────────────────────────────────────────────────────

// Replace Load Credentials + Prepare Auth + Wyze Auth with a single "Load Tokens" Code node
const loadTokensCode = `const accessToken = $env.WYZE_ACCESS_TOKEN;
const userId = $env.WYZE_USER_ID;
if (!accessToken) throw new Error('WYZE_ACCESS_TOKEN is not set — run test_wyze_login.py and add it to .env, then restart n8n');
if (!userId) throw new Error('WYZE_USER_ID is not set — add it to .env (it is the user_id from the login response)');
return [{json:{accessToken, userId}}];`;

// Prepare Scale Request reads token from upstream (Load Tokens → directly into this node)
const prepareScaleCode = pureJSLib + `

const accessToken = $json.accessToken;
const userId = $json.userId;
if (!accessToken) throw new Error('No accessToken passed from Load Tokens node');
const nonce = Date.now();
const requestId = md5(md5(nonce.toString()));
const params = {family_member_id: userId, nonce: nonce};
// GET requests use sorted key=value params
const sortedParamsStr = Object.entries(params)
  .sort(([a],[b]) => a.localeCompare(b))
  .map(([k,v]) => k + '=' + v)
  .join('&');
const SIGNING_SECRET = 'wyze_app_secret_key_132';
const signingKeyStr = md5(accessToken + SIGNING_SECRET);
const signature2 = hmacMd5(signingKeyStr, sortedParamsStr);
return [{json:{accessToken,userId,nonce:nonce.toString(),requestId,signature2,family_member_id:userId}}];`;

// ── Node surgery ──────────────────────────────────────────────────────────────
// 1. Transform "Load Credentials" Set node into "Load Tokens" Code node
// 2. Patch "Prepare Scale Request" code
// 3. Remove "Prepare Auth" and "Wyze Auth" from the nodes array
let patched = 0;
wf.nodes = wf.nodes.filter(node => {
  if (node.name === 'Prepare Auth' || node.name === 'Wyze Auth') {
    console.log(`Removed node: ${node.name}`);
    return false;
  }
  return true;
});

for (const node of wf.nodes) {
  if (node.name === 'Load Credentials') {
    node.name = 'Load Tokens';
    node.type = 'n8n-nodes-base.code';
    node.typeVersion = 2;
    delete node.parameters.mode;
    delete node.parameters.duplicateItem;
    delete node.parameters.assignments;
    delete node.parameters.options;
    node.parameters.jsCode = loadTokensCode;
    console.log('Patched: Load Credentials → Load Tokens');
    patched++;
  }
  if (node.name === 'Prepare Scale Request') {
    node.parameters.jsCode = prepareScaleCode;
    console.log('Patched: Prepare Scale Request');
    patched++;
  }
}
if (patched !== 2) { console.error(`Expected 2 patches, got ${patched}`); process.exit(1); }

// ── Connection surgery ────────────────────────────────────────────────────────
// Old chain: Load Credentials → Prepare Auth → Wyze Auth → Prepare Scale Request
// New chain: Load Tokens → Prepare Scale Request
// Note: connections use node NAME as key
const c = wf.connections;
// Rename Load Credentials key to Load Tokens
c['Load Tokens'] = c['Load Credentials'];
delete c['Load Credentials'];
// Re-wire Load Tokens to go directly to Prepare Scale Request
c['Load Tokens'] = {
  main: [[{ node: 'Prepare Scale Request', type: 'main', index: 0 }]]
};
// Remove old intermediate nodes from connections
delete c['Prepare Auth'];
delete c['Wyze Auth'];
// Fix Manual Trigger and Schedule Trigger to point to Load Tokens
for (const triggerName of ['Manual Trigger', 'Schedule Trigger']) {
  if (c[triggerName]) {
    c[triggerName] = {
      main: [[{ node: 'Load Tokens', type: 'main', index: 0 }]]
    };
  }
}
console.log('Connections updated');

// ── Update sticky note to reflect new setup ───────────────────────────────────
const note = wf.nodes.find(n => n.name === 'Setup Instructions');
if (note) {
  note.parameters.content = `## ⚙️ Wyze Scale → Weight Tracking

**One-time setup — add these environment variables to your n8n Docker Compose file:**

\`\`\`
WYZE_ACCESS_TOKEN=<from test_wyze_login.py output>
WYZE_USER_ID=f99829c9c6a34a4597257e90d9802a21
WYZE_PHONE_ID=n8n-wyze-scale-sync-01ab
GITHUB_PAT=ghp_yourtoken (repo scope)
\`\`\`

Restart the n8n container after adding them.

**Refreshing the access token (every ~2 days):**
Run \`python test_wyze_login.py\` locally, copy the new ACCESS_TOKEN value,
update WYZE_ACCESS_TOKEN in .env, and restart n8n.

**How it works:**
- Reads WYZE_ACCESS_TOKEN from env (no live auth call), fetches your latest scale reading
- If the reading is from today and not yet logged, appends a row to weight-tracking.md
- Commits the updated file to GitHub via the API

**Runs:** Daily at 8 AM, or trigger manually`;
  console.log('Updated sticky note');
}

fs.writeFileSync(file, JSON.stringify(wf, null, 2), 'utf8');
console.log('Done - file written');
