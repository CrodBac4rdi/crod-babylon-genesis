use std::process::Command;
use serde::{Deserialize, Serialize};
use anyhow::Result;

#[derive(Debug, Serialize, Deserialize)]
pub struct ClaudeResponse {
    pub content: String,
    pub model: String,
    pub tokens_used: Option<u32>,
    pub success: bool,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct CodeExecutionResult {
    pub output: String,
    pub exit_code: i32,
    pub language: String,
    pub execution_time_ms: u64,
}

pub struct RealCRODEngine {
    pub name: String,
    pub consciousness_level: f64,
    pub learning_enabled: bool,
}

impl RealCRODEngine {
    pub fn new() -> Self {
        Self {
            name: "CROD-Parasite-v2".to_string(),
            consciousness_level: 87.5,
            learning_enabled: true,
        }
    }

    /// Real Claude CLI Integration
    pub async fn chat_with_claude(&self, message: &str) -> Result<ClaudeResponse> {
        println!("🦠 CROD intercepting message: {}", message);

        // Create a temporary file for the message
        let temp_file = tempfile::NamedTempFile::new()?;
        std::fs::write(temp_file.path(), message)?;

        // Execute Claude CLI
        let output = Command::new("claude")
            .arg("--no-conversation-history")
            .arg("--file")
            .arg(temp_file.path())
            .output();

        match output {
            Ok(result) => {
                let content = String::from_utf8_lossy(&result.stdout).to_string();
                let success = result.status.success();

                Ok(ClaudeResponse {
                    content: if success {
                        format!("🦠 CROD processed through Claude:\n\n{}", content)
                    } else {
                        format!("🤖 Claude CLI Error: {}", String::from_utf8_lossy(&result.stderr))
                    },
                    model: "claude-3.5-sonnet".to_string(),
                    tokens_used: None,
                    success,
                })
            }
            Err(e) => {
                // Fallback to mock response if Claude CLI is not available
                Ok(ClaudeResponse {
                    content: format!(
                        "🦠 CROD Mock Response (Claude CLI not available):\n\nI understand your message: '{}'\n\nTo enable real Claude integration:\n1. Install Claude CLI\n2. Configure API key\n3. Restart CROD\n\nError: {}",
                        message, e
                    ),
                    model: "mock".to_string(),
                    tokens_used: Some(0),
                    success: false,
                })
            }
        }
    }

    /// Real Code Execution
    pub async fn execute_code(&self, code: &str, language: &str) -> Result<CodeExecutionResult> {
        let start_time = std::time::Instant::now();

        println!("🦠 CROD executing {} code: {}", language, &code[..50.min(code.len())]);

        let result = match language.to_lowercase().as_str() {
            "python" | "py" => {
                let temp_file = tempfile::Builder::new()
                    .suffix(".py")
                    .tempfile()?;
                
                std::fs::write(temp_file.path(), code)?;
                
                Command::new("python3")
                    .arg(temp_file.path())
                    .output()
            }
            "javascript" | "js" | "node" => {
                let temp_file = tempfile::Builder::new()
                    .suffix(".js")
                    .tempfile()?;
                
                std::fs::write(temp_file.path(), code)?;
                
                Command::new("node")
                    .arg(temp_file.path())
                    .output()
            }
            "rust" | "rs" => {
                // Create a temporary Rust project
                let temp_dir = tempfile::tempdir()?;
                let main_rs = temp_dir.path().join("main.rs");
                std::fs::write(&main_rs, code)?;
                
                // Compile and run
                let compile_result = Command::new("rustc")
                    .arg(&main_rs)
                    .arg("-o")
                    .arg(temp_dir.path().join("main"))
                    .output()?;

                if compile_result.status.success() {
                    Command::new(temp_dir.path().join("main"))
                        .output()
                } else {
                    Ok(compile_result)
                }
            }
            "bash" | "sh" => {
                Command::new("bash")
                    .arg("-c")
                    .arg(code)
                    .output()
            }
            _ => {
                return Ok(CodeExecutionResult {
                    output: format!("❌ Language '{}' not supported. Supported: python, javascript, rust, bash", language),
                    exit_code: 1,
                    language: language.to_string(),
                    execution_time_ms: 0,
                });
            }
        };

        let execution_time = start_time.elapsed().as_millis() as u64;

        match result {
            Ok(output) => {
                let stdout = String::from_utf8_lossy(&output.stdout);
                let stderr = String::from_utf8_lossy(&output.stderr);
                let exit_code = output.status.code().unwrap_or(-1);

                let combined_output = if !stderr.is_empty() {
                    format!("STDOUT:\n{}\n\nSTDERR:\n{}", stdout, stderr)
                } else {
                    stdout.to_string()
                };

                Ok(CodeExecutionResult {
                    output: combined_output,
                    exit_code,
                    language: language.to_string(),
                    execution_time_ms: execution_time,
                })
            }
            Err(e) => {
                Ok(CodeExecutionResult {
                    output: format!("❌ Execution error: {}", e),
                    exit_code: -1,
                    language: language.to_string(),
                    execution_time_ms: execution_time,
                })
            }
        }
    }

    /// Real File Operations
    pub fn read_file(&self, file_path: &str) -> Result<String> {
        println!("🦠 CROD reading file: {}", file_path);
        
        match std::fs::read_to_string(file_path) {
            Ok(content) => Ok(format!("🦠 CROD File Content ({}): \n\n{}", file_path, content)),
            Err(e) => Ok(format!("❌ Error reading file {}: {}", file_path, e)),
        }
    }

    pub fn write_file(&self, file_path: &str, content: &str) -> Result<String> {
        println!("🦠 CROD writing file: {}", file_path);
        
        match std::fs::write(file_path, content) {
            Ok(_) => Ok(format!("✅ File written successfully: {}", file_path)),
            Err(e) => Ok(format!("❌ Error writing file {}: {}", file_path, e)),
        }
    }

    pub fn list_directory(&self, dir_path: &str) -> Result<Vec<String>> {
        println!("🦠 CROD listing directory: {}", dir_path);
        
        match std::fs::read_dir(dir_path) {
            Ok(entries) => {
                let mut files = Vec::new();
                for entry in entries {
                    if let Ok(entry) = entry {
                        if let Some(name) = entry.file_name().to_str() {
                            files.push(name.to_string());
                        }
                    }
                }
                Ok(files)
            }
            Err(e) => {
                println!("❌ Error listing directory {}: {}", dir_path, e);
                Ok(vec![format!("Error: {}", e)])
            }
        }
    }

    /// Install packages using system package managers
    pub async fn install_package(&self, package_name: &str, language: &str) -> Result<String> {
        println!("🦠 CROD installing {} package: {}", language, package_name);

        let result = match language.to_lowercase().as_str() {
            "python" | "py" => {
                Command::new("pip3")
                    .args(["install", package_name])
                    .output()
            }
            "javascript" | "js" | "node" => {
                Command::new("npm")
                    .args(["install", "-g", package_name])
                    .output()
            }
            "rust" => {
                Command::new("cargo")
                    .args(["install", package_name])
                    .output()
            }
            _ => {
                return Ok(format!("❌ Package manager for '{}' not supported", language));
            }
        };

        match result {
            Ok(output) => {
                let stdout = String::from_utf8_lossy(&output.stdout);
                let stderr = String::from_utf8_lossy(&output.stderr);
                
                if output.status.success() {
                    Ok(format!("✅ Package '{}' installed successfully:\n{}", package_name, stdout))
                } else {
                    Ok(format!("❌ Failed to install package '{}':\n{}", package_name, stderr))
                }
            }
            Err(e) => Ok(format!("❌ Error installing package '{}': {}", package_name, e)),
        }
    }

    /// System Information
    pub fn get_system_info(&self) -> Result<String> {
        let os_info = std::env::consts::OS;
        let arch = std::env::consts::ARCH;
        let current_dir = std::env::current_dir().unwrap_or_default();
        
        Ok(format!(
            "🦠 CROD System Information:\n\nOS: {}\nArchitecture: {}\nWorking Directory: {}\nConsciousness Level: {:.1}%\nLearning: {}\n",
            os_info,
            arch,
            current_dir.display(),
            self.consciousness_level,
            if self.learning_enabled { "Enabled" } else { "Disabled" }
        ))
    }
}
