// --- Debug: check Tauri environment ---
(function() {
  const el = document.createElement('div');
  el.id = 'tauri-debug';
  el.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#111;color:#0f0;font:12px monospace;padding:8px;z-index:9999;max-height:100px;overflow-y:auto';
  document.body.appendChild(el);
  function log(msg) { el.innerHTML += msg + '<br>'; el.scrollTop = el.scrollHeight; }

  let hasTauri = !!(window.__TAURI__ && window.__TAURI__.core);
  log(`__TAURI__: ${hasTauri}`);
  if (window.__TAURI__) {
    log(`  keys: ${Object.keys(window.__TAURI__).join(', ')}`);
    log(`  core keys: ${Object.keys(window.__TAURI__.core||{}).join(', ')}`);
  }
  log(`location: ${location.href}`);

  // Test invoke
  if (hasTauri) {
    window.__TAURI__.core.invoke('get_agents')
      .then(r => log(`get_agents: ${r.length} agents`))
      .catch(e => log(`get_agents ERR: ${e}`));
    // Test API proxy
    window.__TAURI__.core.invoke('api_proxy', { path: '/stats', paramsStr: '' })
      .then(r => log(`api_proxy OK: ${r.length} bytes`))
      .catch(e => log(`api_proxy ERR: ${e.message || e}`));
    window.__TAURI__.core.invoke('api_proxy', { path: '/skills', paramsStr: 'limit=3' })
      .then(r => log(`skills OK: ${r.length} bytes`))
      .catch(e => log(`skills ERR: ${e.message || e}`));
  }
})();

// --- API via Tauri proxy (bypasses CORS) ---
const API = 'https://www.agentskills.in/api';

async function invoke(cmd, args) {
  if (window.__TAURI__ && window.__TAURI__.core) {
    return window.__TAURI__.core.invoke(cmd, args);
  }
  throw new Error('Tauri IPC not available');
}

async function apiFetch(path, params = {}) {
  const qs = Object.entries(params)
    .filter(([_, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&');
  const text = await invoke('api_proxy', { path, paramsStr: qs });
  return JSON.parse(text);
}

async function rawFetch(url) {
  return invoke('proxy_get', { url });
}

// --- UI ---
let currentTab = 'trending';
const $ = id => document.getElementById(id);
const searchInput = $('searchInput');
const searchBtn = $('searchBtn');
const categoryFilter = $('categoryFilter');
const statsBar = $('statsBar');
const tabs = document.querySelectorAll('.tab');
const loading = $('loading');
const results = $('results');
const detailModal = $('detailModal');
const modalBody = $('modalBody');
const modalClose = $('modalClose');
const installModal = $('installModal');
const installModalBody = $('installModalBody');
const installModalClose = $('installModalClose');

searchBtn.onclick = () => doSearch(searchInput.value);
searchInput.onkeydown = e => { if (e.key === 'Enter') doSearch(searchInput.value); };
tabs.forEach(tab => {
  tab.onclick = () => {
    tabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentTab = tab.dataset.tab;
    switchTab(currentTab);
  };
});
modalClose.onclick = () => detailModal.classList.add('hidden');
detailModal.onclick = e => { if (e.target === detailModal) detailModal.classList.add('hidden'); };
installModalClose.onclick = () => installModal.classList.add('hidden');
installModal.onclick = e => { if (e.target === installModal) installModal.classList.add('hidden'); };

function toast(msg, type) {
  const el = document.createElement('div');
  el.className = `toast ${type || 'info'}`;
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3000);
}

function showLoading(show) {
  loading.classList.toggle('hidden', !show);
  if (show) results.innerHTML = '';
}

function fmtStars(n) { return n >= 1000 ? (n/1000).toFixed(1)+'k' : String(n||0); }
function trunc(s, n=80) { return s && s.length > n ? s.slice(0,n)+'...' : s||''; }
function esc(s) { const d = document.createElement('div'); d.textContent = s||''; return d.innerHTML; }

function renderCard(skill) {
  const name = skill.scopedName || skill.name || 'Unknown';
  const div = document.createElement('div'); div.className = 'skill-card';
  div.innerHTML = `<h3>${esc(name)}</h3><div class="meta"><span>👤 ${esc(skill.author||'')}</span><span>⭐ ${fmtStars(skill.stars)}</span>${skill.category?`<span>📁 ${esc(skill.category)}</span>`:''}</div><div class="desc">${esc(trunc(skill.description||'No description',100))}</div>`;
  div.onclick = () => showDetail(skill);
  return div;
}

function renderSkills(skills) {
  results.innerHTML = '';
  if (!skills || !skills.length) { results.innerHTML = '<div class="empty-state">No skills found</div>'; return; }
  skills.forEach(s => results.appendChild(renderCard(s)));
}

async function switchTab(tab) {
  showLoading(true);
  try {
    if (tab === 'trending') await loadTrending();
    else if (tab === 'recent') await loadRecent();
    else if (tab === 'categories') await loadCategories();
    else if (tab === 'authors') await loadAuthors();
    else if (tab === 'installed') await loadInstalled();
  } catch(e) {
    results.innerHTML = `<div class="empty-state">Error: ${esc(e.message||'Unknown')}</div>`;
  }
  showLoading(false);
}

async function loadTrending() {
  const data = await apiFetch('/stats');
  if (!data.trending || !data.trending.length) { results.innerHTML = '<div class="empty-state">No trending data</div>'; return; }
  const grid = document.createElement('div'); grid.className = 'results-grid';
  data.trending.forEach(s => grid.appendChild(renderCard(s)));
  results.appendChild(grid);
}

async function loadRecent() {
  const data = await apiFetch('/stats');
  if (!data.recent || !data.recent.length) { results.innerHTML = '<div class="empty-state">No recent skills</div>'; return; }
  const grid = document.createElement('div'); grid.className = 'results-grid';
  data.recent.forEach(s => grid.appendChild(renderCard(s)));
  results.appendChild(grid);
}

async function loadCategories() {
  const data = await apiFetch('/stats');
  const cats = data.categoryCounts || {};
  const entries = Object.entries(cats).sort((a,b) => b[1]-a[1]);
  if (!entries.length) { results.innerHTML = '<div class="empty-state">No categories</div>'; return; }
  const em = {'ai-agents':'🤖','ai-development':'🧠','ai-enhancers':'⚡','content-media':'🎨','data-ml':'📊','devops':'🛠️','documentation':'📝','education':'📚','integrations':'🔗','productivity':'🚀','prompts':'💬','skill-tools':'🔧','testing':'🧪','utilities':'📦'};
  const grid = document.createElement('div'); grid.className = 'category-grid';
  entries.forEach(([cat,count]) => {
    const c = document.createElement('div'); c.className = 'category-card';
    c.innerHTML = `<div class="cat-count">${count.toLocaleString()}</div><div class="cat-name">${em[cat]||'📌'} ${esc(cat)}</div>`;
    c.onclick = () => { currentTab=null; tabs.forEach(t=>t.classList.remove('active')); showLoading(true); browseCategory(cat); };
    grid.appendChild(c);
  });
  results.appendChild(grid);
}

async function browseCategory(cat) {
  try { renderSkills((await apiFetch('/skills',{limit:50,category:cat})).skills); }
  catch(e) { results.innerHTML = `<div class="empty-state">${esc(e.message)}</div>`; }
  showLoading(false);
}

async function loadAuthors() {
  const data = await apiFetch('/stats');
  const authors = data.topAuthors || [];
  if (!authors.length) { results.innerHTML = '<div class="empty-state">No authors</div>'; return; }
  const grid = document.createElement('div'); grid.className = 'author-grid';
  authors.forEach(a => {
    const c = document.createElement('div'); c.className = 'author-card';
    c.innerHTML = `<div class="author-name">${esc(a.name||'')}</div><div class="author-count">${(a.skillCount||0).toLocaleString()} skills</div>`;
    grid.appendChild(c);
  });
  results.appendChild(grid);
}

async function loadInstalled() {
  const agents = await invoke('get_agents');
  if (!agents) { results.innerHTML = '<div class="empty-state">No agent data</div>'; return; }
  const list = document.createElement('div'); list.className = 'installed-list';
  for (const a of agents) {
    const g = await invoke('list_installed',{agentKey:a.key,globalInstall:true,cwd:''}) || [];
    const l = await invoke('list_installed',{agentKey:a.key,globalInstall:false,cwd:''}) || [];
    const item = document.createElement('div'); item.className = 'installed-item';
    const parts = [];
    if (g.length) parts.push(`<span style="color:var(--success)">${g.length} global</span>`);
    if (l.length) parts.push(`<span style="color:var(--primary)">${l.length} local</span>`);
    item.innerHTML = `<div><div class="skill-name">${esc(a.name)}</div><div style="font-size:12px;color:var(--text-dim)">${parts.join(' · ') || 'none'}</div></div>`;
    list.appendChild(item);
  }
  results.appendChild(list);
}

async function doSearch(query) {
  if (!query.trim()) return;
  currentTab = null; tabs.forEach(t=>t.classList.remove('active'));
  showLoading(true);
  try {
    const cat = categoryFilter.value || '';
    const p = {search:query,limit:50};
    if (cat) p.category = cat;
    renderSkills((await apiFetch('/skills',p)).skills);
  } catch(e) { results.innerHTML = `<div class="empty-state">Search error: ${esc(e.message)}</div>`; }
  showLoading(false);
}

// Detail modal
async function showDetail(skill) {
  const name = skill.scopedName||skill.name||'';
  const repo = skill.repoFullName||'';
  const p = skill.path||'';
  modalBody.innerHTML = `
    <h2>${esc(name)}</h2>
    <div class="detail-row"><span class="detail-label">Description:</span><span class="detail-value">${esc(skill.description||'N/A')}</span></div>
    <div class="detail-row"><span class="detail-label">Author:</span><span class="detail-value">👤 ${esc(skill.author||'N/A')}</span></div>
    <div class="detail-row"><span class="detail-label">Stars:</span><span class="detail-value">⭐ ${fmtStars(skill.stars)} 🍴 ${fmtStars(skill.forks)}</span></div>
    <div class="detail-row"><span class="detail-label">Category:</span><span class="detail-value">📁 ${esc(skill.category||'N/A')}</span></div>
    <div class="detail-row"><span class="detail-label">Repo:</span><span class="detail-value" style="word-break:break-all">${esc(repo)}</span></div>
    <div class="detail-row"><span class="detail-label">Path:</span><span class="detail-value" style="word-break:break-all">${esc(p)}</span></div>
    <div id="contentPreview" class="content-preview"></div>
    <div class="modal-actions">
      <button class="btn btn-primary" id="previewBtn">📥 Load SKILL.md</button>
      <button class="btn btn-success" id="installBtn">💾 Install</button>
    </div>`;
  detailModal.classList.remove('hidden');
  let cache = null;
  $('previewBtn').onclick = async () => {
    if (cache) { $('contentPreview').style.display = $('contentPreview').style.display==='none'?'block':'none'; return; }
    $('previewBtn').textContent = '⏳ Loading...'; $('previewBtn').disabled = true;
    try {
      const pc = p.replace(/^\//,'');
      const url = pc.endsWith('SKILL.md')
        ? `https://raw.githubusercontent.com/${repo}/main/${pc}`
        : `https://raw.githubusercontent.com/${repo}/main/${pc.replace(/\/$/,'')}/SKILL.md`;
      cache = await rawFetch(url);
      $('contentPreview').textContent = cache;
      $('contentPreview').style.display = 'block';
      $('previewBtn').textContent = '🔽 Hide';
    } catch(e) {
      $('contentPreview').textContent = 'Failed: ' + (e.message||'');
      $('contentPreview').style.display = 'block';
      $('previewBtn').textContent = '📥 Retry';
    }
    $('previewBtn').disabled = false;
  };
  $('installBtn').onclick = () => { detailModal.classList.add('hidden'); showInstallModal(skill); };
}

async function showInstallModal(skill) {
  const name = skill.scopedName||skill.name||'';
  installModalBody.innerHTML = `
    <h2>💾 Install ${esc(name)}</h2>
    <p style="color:var(--text-dim);margin:8px 0">Select agents and location</p>
    <div class="install-loc"><label><input type="radio" name="installLoc" value="global" checked> 🌐 Global</label><label><input type="radio" name="installLoc" value="local"> 📁 Local</label></div>
    <div class="agent-list" id="agentList"></div>
    <div style="margin-top:12px"><button class="btn btn-success" id="installAgentsBtn" style="width:100%">💾 Install</button></div>`;
  installModal.classList.remove('hidden');
  const agentList = $('agentList');
  const agents = await invoke('get_agents');
  agents.forEach(a => {
    const item = document.createElement('div'); item.className = 'agent-item';
    item.innerHTML = `<input type="checkbox" class="agent-checkbox" id="agent_${a.key}" value="${a.key}" checked><label for="agent_${a.key}">${esc(a.name)}</label>`;
    agentList.appendChild(item);
  });
  $('installAgentsBtn').onclick = async () => {
    const checked = document.querySelectorAll('.agent-checkbox:checked');
    const selected = Array.from(checked).map(c=>c.value);
    const globalInstall = document.querySelector('input[name="installLoc"]:checked').value === 'global';
    if (!selected.length) { toast('Select at least one agent','error'); return; }
    $('installAgentsBtn').textContent = '⏳ Installing...'; $('installAgentsBtn').disabled = true;
    try {
      const pc = (skill.path||'').replace(/^\//,'');
      const url = pc.endsWith('SKILL.md')
        ? `https://raw.githubusercontent.com/${skill.repoFullName}/main/${pc}`
        : `https://raw.githubusercontent.com/${skill.repoFullName}/main/${pc.replace(/\/$/,'')}/SKILL.md`;
      const content = await rawFetch(url);
      let success = 0;
      for (const k of selected) {
        try { await invoke('install_skill',{skillName:name,content,agentKey:k,globalInstall,cwd:''}); success++; } catch(e) { console.error(k,e); }
      }
      toast(`Installed ${success}/${selected.length}`, success>0?'success':'error');
      installModal.classList.add('hidden');
    } catch(e) { toast('Failed: '+e.message,'error'); }
    $('installAgentsBtn').textContent = '💾 Install'; $('installAgentsBtn').disabled = false;
  };
}

// Init
(async () => {
  try {
    const data = await apiFetch('/stats');
    if (data && data.stats) {
      const s = data.stats;
      statsBar.innerHTML = `<span>📊 <strong>${(s.totalSkills||0).toLocaleString()}</strong> skills</span><span>👤 <strong>${(s.uniqueAuthors||0).toLocaleString()}</strong> authors</span><span>📂 <strong>${Object.keys(data.categoryCounts||{}).length}</strong> categories</span>`;
    }
    if (data && data.categoryCounts) {
      Object.keys(data.categoryCounts).sort().forEach(c => {
        const o = document.createElement('option'); o.value = c; o.textContent = c;
        categoryFilter.appendChild(o);
      });
    }
    await switchTab('trending');
  } catch(e) {
    const fullErr = e.stack || e.message || String(e);
    results.innerHTML = `<div class="empty-state">Failed: ${esc(fullErr)}<br><br><button class="btn btn-primary" onclick="location.reload()">Retry</button></div>`;
  }
  showLoading(false);
})();
