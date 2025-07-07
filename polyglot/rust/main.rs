use std::io::{self, Read};
use std::process::{Command, Stdio};
use std::time::{Duration, Instant};
use serde::{Deserialize, Serialize};
use tempfile::NamedTempFile;
use std::io::Write;

#[derive(Debug, Deserialize)]
struct CodeExecutionRequest {
    code: String,
    language: String,
}

#[derive(Debug, Serialize)]
struct CodeExecutionResult {
    output: String,
    exit_code: i32,
    language: String,
    execution_time_ms: u64,
    success: bool,
}

fn main() -> io::Result<()> {
    // JSON-Eingabe vom Node.js-Server lesen
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;
    
    // JSON parsen
    let request: CodeExecutionRequest = match serde_json::from_str(&input) {
        Ok(req) => req,
        Err(e) => {
            let error_result = CodeExecutionResult {
                output: format!("Fehler beim Parsen der Anfrage: {}", e),
                exit_code: 1,
                language: "unknown".to_string(),
                execution_time_ms: 0,
                success: false,
            };
            println!("{}", serde_json::to_string(&error_result).unwrap());
            return Ok(());
        }
    };
    
    // Code ausführen
    let result = execute_code(&request.code, &request.language);
    
    // Ergebnis als JSON zurückgeben
    println!("{}", serde_json::to_string(&result).unwrap());
    
    Ok(())
}

fn execute_code(code: &str, language: &str) -> CodeExecutionResult {
    let start_time = Instant::now();
    
    match language {
        "javascript" | "js" => execute_javascript(code, start_time),
        "python" | "py" => execute_python(code, start_time),
        "rust" => execute_rust(code, start_time),
        _ => CodeExecutionResult {
            output: format!("Nicht unterstützte Sprache: {}", language),
            exit_code: 1,
            language: language.to_string(),
            execution_time_ms: 0,
            success: false,
        }
    }
}

fn execute_javascript(code: &str, start_time: Instant) -> CodeExecutionResult {
    // Temporäre Datei für den JavaScript-Code erstellen
    let mut temp_file = match NamedTempFile::new() {
        Ok(file) => file,
        Err(e) => {
            return CodeExecutionResult {
                output: format!("Fehler beim Erstellen der temporären Datei: {}", e),
                exit_code: 1,
                language: "javascript".to_string(),
                execution_time_ms: 0,
                success: false,
            };
        }
    };
    
    // Code in die Datei schreiben
    if let Err(e) = temp_file.write_all(code.as_bytes()) {
        return CodeExecutionResult {
            output: format!("Fehler beim Schreiben in die temporäre Datei: {}", e),
            exit_code: 1,
            language: "javascript".to_string(),
            execution_time_ms: 0,
            success: false,
        };
    }
    
    // Node.js-Prozess starten
    let output = Command::new("node")
        .arg(temp_file.path())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output();
    
    process_command_output(output, "javascript", start_time)
}

fn execute_python(code: &str, start_time: Instant) -> CodeExecutionResult {
    // Temporäre Datei für den Python-Code erstellen
    let mut temp_file = match NamedTempFile::new() {
        Ok(file) => file,
        Err(e) => {
            return CodeExecutionResult {
                output: format!("Fehler beim Erstellen der temporären Datei: {}", e),
                exit_code: 1,
                language: "python".to_string(),
                execution_time_ms: 0,
                success: false,
            };
        }
    };
    
    // Code in die Datei schreiben
    if let Err(e) = temp_file.write_all(code.as_bytes()) {
        return CodeExecutionResult {
            output: format!("Fehler beim Schreiben in die temporäre Datei: {}", e),
            exit_code: 1,
            language: "python".to_string(),
            execution_time_ms: 0,
            success: false,
        };
    }
    
    // Python-Prozess starten
    let output = Command::new("python3")
        .arg(temp_file.path())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output();
    
    process_command_output(output, "python", start_time)
}

fn execute_rust(code: &str, start_time: Instant) -> CodeExecutionResult {
    // Temporäres Verzeichnis für Rust-Projekt erstellen
    let temp_dir = match tempfile::tempdir() {
        Ok(dir) => dir,
        Err(e) => {
            return CodeExecutionResult {
                output: format!("Fehler beim Erstellen des temporären Verzeichnisses: {}", e),
                exit_code: 1,
                language: "rust".to_string(),
                execution_time_ms: 0,
                success: false,
            };
        }
    };
    
    // main.rs erstellen
    let main_rs_path = temp_dir.path().join("main.rs");
    if let Err(e) = std::fs::write(&main_rs_path, code) {
        return CodeExecutionResult {
            output: format!("Fehler beim Schreiben der main.rs: {}", e),
            exit_code: 1,
            language: "rust".to_string(),
            execution_time_ms: 0,
            success: false,
        };
    }
    
    // Rust-Code kompilieren
    let compile_output = Command::new("rustc")
        .arg(main_rs_path)
        .arg("-o")
        .arg(temp_dir.path().join("rust_program"))
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output();
    
    match compile_output {
        Ok(output) => {
            if !output.status.success() {
                // Kompilierungsfehler
                let stderr = String::from_utf8_lossy(&output.stderr);
                return CodeExecutionResult {
                    output: format!("Kompilierungsfehler:\n{}", stderr),
                    exit_code: output.status.code().unwrap_or(1),
                    language: "rust".to_string(),
                    execution_time_ms: start_time.elapsed().as_millis() as u64,
                    success: false,
                };
            }
            
            // Ausführbare Datei ausführen
            let run_output = Command::new(temp_dir.path().join("rust_program"))
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .output();
            
            process_command_output(run_output, "rust", start_time)
        },
        Err(e) => {
            CodeExecutionResult {
                output: format!("Fehler beim Ausführen des rustc-Compilers: {}", e),
                exit_code: 1,
                language: "rust".to_string(),
                execution_time_ms: start_time.elapsed().as_millis() as u64,
                success: false,
            }
        }
    }
}

fn process_command_output(
    output: io::Result<std::process::Output>, 
    language: &str, 
    start_time: Instant
) -> CodeExecutionResult {
    match output {
        Ok(output) => {
            let stdout = String::from_utf8_lossy(&output.stdout).to_string();
            let stderr = String::from_utf8_lossy(&output.stderr).to_string();
            
            let result_output = if stderr.is_empty() {
                stdout
            } else if stdout.is_empty() {
                stderr
            } else {
                format!("STDOUT:\n{}\n\nSTDERR:\n{}", stdout, stderr)
            };
            
            CodeExecutionResult {
                output: result_output,
                exit_code: output.status.code().unwrap_or(0),
                language: language.to_string(),
                execution_time_ms: start_time.elapsed().as_millis() as u64,
                success: output.status.success(),
            }
        },
        Err(e) => {
            CodeExecutionResult {
                output: format!("Fehler beim Ausführen des Codes: {}", e),
                exit_code: 1,
                language: language.to_string(),
                execution_time_ms: start_time.elapsed().as_millis() as u64,
                success: false,
            }
        }
    }
}
