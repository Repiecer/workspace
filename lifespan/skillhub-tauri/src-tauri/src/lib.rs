use std::fs;
use std::path::PathBuf;
use reqwest::Client;
use tauri::State;
use serde::Serialize;

const API_BASE: &str = "https://www.agentskills.in/api";

struct AppState {
    client: Client,
}

impl Default for AppState {
    fn default() -> Self {
        Self {
            client: Client::builder()
                .user_agent("SkillHub/1.0")
                .timeout(std::time::Duration::from_secs(30))
                .build()
                .expect("Failed to create HTTP client"),
        }
    }
}

#[derive(Serialize)]
pub struct AgentInfo {
    pub key: String,
    pub name: String,
    pub global_dir: String,
    pub local_dir: String,
}

#[tauri::command]
async fn api_proxy(state: State<'_, AppState>, path: String, params_str: String) -> Result<String, String> {
    let url = if params_str.is_empty() {
        format!("{}{}", API_BASE, path)
    } else {
        format!("{}{}?{}", API_BASE, path, params_str)
    };

    let resp = state.client.get(&url).send().await
        .map_err(|e| format!("{}", e))?;

    if resp.status() != 200 {
        return Err(format!("HTTP {}", resp.status()));
    }

    resp.text().await.map_err(|e| format!("{}", e))
}

#[tauri::command]
async fn proxy_get(url: String) -> Result<String, String> {
    let client = Client::builder()
        .user_agent("SkillHub/1.0")
        .timeout(std::time::Duration::from_secs(15))
        .build()
        .map_err(|e| format!("{}", e))?;

    let resp = client.get(&url).send().await
        .map_err(|e| format!("{}", e))?;

    if resp.status() != 200 {
        return Err(format!("HTTP {}", resp.status()));
    }

    resp.text().await.map_err(|e| format!("{}", e))
}

#[tauri::command]
fn get_agents() -> Vec<AgentInfo> {
    vec![
        AgentInfo { key: "opencode".into(), name: "OpenCode".into(), global_dir: "~/.config/opencode/skills".into(), local_dir: ".opencode/skills".into() },
        AgentInfo { key: "claude".into(), name: "Claude Code".into(), global_dir: "~/.claude/skills".into(), local_dir: ".claude/skills".into() },
        AgentInfo { key: "cursor".into(), name: "Cursor".into(), global_dir: "~/.cursor/skills".into(), local_dir: ".cursor/skills".into() },
        AgentInfo { key: "copilot".into(), name: "GitHub Copilot".into(), global_dir: "~/.github/skills".into(), local_dir: ".github/skills".into() },
        AgentInfo { key: "codex".into(), name: "OpenAI Codex".into(), global_dir: "~/.codex/skills".into(), local_dir: ".codex/skills".into() },
        AgentInfo { key: "windsurf".into(), name: "Windsurf".into(), global_dir: "~/.codeium/windsurf/skills".into(), local_dir: ".windsurf/skills".into() },
        AgentInfo { key: "cline".into(), name: "Cline".into(), global_dir: "~/.cline/skills".into(), local_dir: ".cline/skills".into() },
        AgentInfo { key: "gemini".into(), name: "Gemini CLI".into(), global_dir: "~/.gemini/skills".into(), local_dir: ".gemini/skills".into() },
        AgentInfo { key: "zed".into(), name: "Zed".into(), global_dir: "~/.config/zed/skills".into(), local_dir: ".zed/skills".into() },
    ]
}

#[tauri::command]
fn install_skill(skill_name: String, content: String, agent_key: String, global_install: bool, cwd: String) -> Result<String, String> {
    let agents = get_agents();
    let agent = agents.iter().find(|a| a.key == agent_key).ok_or_else(|| format!("Unknown agent: {}", agent_key))?;
    let base = if global_install { shellexpand::tilde(&agent.global_dir).to_string() } else { PathBuf::from(&cwd).join(&agent.local_dir).to_string_lossy().to_string() };
    let install_dir = PathBuf::from(&base).join(&skill_name);
    fs::create_dir_all(&install_dir).map_err(|e| format!("{}", e))?;
    fs::write(install_dir.join("SKILL.md"), &content).map_err(|e| format!("{}", e))?;
    Ok(format!("Installed to {}", install_dir.display()))
}

#[tauri::command]
fn list_installed(agent_key: String, global_install: bool, cwd: String) -> Result<Vec<String>, String> {
    let agents = get_agents();
    let agent = agents.iter().find(|a| a.key == agent_key).ok_or_else(|| format!("Unknown agent: {}", agent_key))?;
    let base = if global_install { shellexpand::tilde(&agent.global_dir).to_string() } else { PathBuf::from(&cwd).join(&agent.local_dir).to_string_lossy().to_string() };
    let base_path = PathBuf::from(&base);
    if !base_path.exists() { return Ok(vec![]); }
    let mut skills = vec![];
    if let Ok(entries) = fs::read_dir(&base_path) {
        for entry in entries.flatten() {
            if entry.path().join("SKILL.md").exists() {
                if let Ok(name) = entry.file_name().into_string() { skills.push(name); }
            }
        }
    }
    Ok(skills)
}

#[tauri::command]
fn remove_skill(skill_name: String, agent_key: String, global_install: bool, cwd: String) -> Result<String, String> {
    let agents = get_agents();
    let agent = agents.iter().find(|a| a.key == agent_key).ok_or_else(|| format!("Unknown agent: {}", agent_key))?;
    let base = if global_install { shellexpand::tilde(&agent.global_dir).to_string() } else { PathBuf::from(&cwd).join(&agent.local_dir).to_string_lossy().to_string() };
    let skill_path = PathBuf::from(&base).join(&skill_name);
    if !skill_path.exists() { return Err(format!("Not found")); }
    fs::remove_dir_all(&skill_path).map_err(|e| format!("{}", e))?;
    Ok(format!("Removed {}", skill_name))
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(AppState::default())
        .invoke_handler(tauri::generate_handler![
            api_proxy, proxy_get, get_agents,
            install_skill, list_installed, remove_skill,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
