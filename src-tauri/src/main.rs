// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Child, Command};
use std::sync::Mutex;
use tauri::{Manager, State};
use rand::Rng;

/// Holds the Python backend process and port info
struct BackendState {
    process: Mutex<Option<Child>>,
    port: Mutex<u16>,
}

/// Start the Python backend process
///
/// In dev mode, this spawns `python backend/main.py --port <port>`
/// In production, this spawns the bundled PyInstaller binary from bin/
#[tauri::command]
async fn start_backend(state: State<'_, BackendState>) -> Result<u16, String> {
    let mut rng = rand::thread_rng();
    let port: u16 = rng.gen_range(8000..9000);

    // Store the port
    *state.port.lock().unwrap() = port;

    // Determine which command to run based on dev vs production
    let backend_cmd = if cfg!(debug_assertions) {
        // Dev mode: run Python directly
        #[cfg(target_os = "windows")]
        let mut cmd = Command::new("python");

        #[cfg(not(target_os = "windows"))]
        let mut cmd = Command::new("python3");

        cmd.arg("backend/main.py")
           .arg("--port")
           .arg(port.to_string())
           .spawn()
    } else {
        // Production mode: run bundled binary
        // TODO: Update this path once PyInstaller packaging is set up
        #[cfg(target_os = "windows")]
        let backend_path = "bin/python_backend.exe";

        #[cfg(not(target_os = "windows"))]
        let backend_path = "bin/python_backend";

        Command::new(backend_path)
            .arg("--port")
            .arg(port.to_string())
            .spawn()
    };

    match backend_cmd {
        Ok(child) => {
            *state.process.lock().unwrap() = Some(child);
            println!("✓ Python backend started on port {}", port);
            Ok(port)
        }
        Err(e) => {
            eprintln!("✗ Failed to start Python backend: {}", e);
            Err(format!("Failed to start backend: {}", e))
        }
    }
}

/// Stop the Python backend process
#[tauri::command]
async fn stop_backend(state: State<'_, BackendState>) -> Result<(), String> {
    if let Some(mut child) = state.process.lock().unwrap().take() {
        match child.kill() {
            Ok(_) => {
                println!("✓ Python backend stopped");
                Ok(())
            }
            Err(e) => Err(format!("Failed to stop backend: {}", e))
        }
    } else {
        Ok(())
    }
}

/// Get the current backend port
#[tauri::command]
async fn get_backend_port(state: State<'_, BackendState>) -> Result<u16, String> {
    let port = *state.port.lock().unwrap();
    if port == 0 {
        Err("Backend not started".to_string())
    } else {
        Ok(port)
    }
}

/// Check if the backend is healthy by pinging /status
#[tauri::command]
async fn check_backend_health(port: u16) -> Result<bool, String> {
    let url = format!("http://127.0.0.1:{}/status", port);
    match reqwest::get(&url).await {
        Ok(response) => Ok(response.status().is_success()),
        Err(_) => Ok(false),
    }
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_shell::init())
        .manage(BackendState {
            process: Mutex::new(None),
            port: Mutex::new(0),
        })
        .invoke_handler(tauri::generate_handler![
            start_backend,
            stop_backend,
            get_backend_port,
            check_backend_health,
        ])
        .setup(|app| {
            // Auto-start backend on launch
            let handle = app.handle().clone();
            tauri::async_runtime::spawn(async move {
                let state = handle.state::<BackendState>();
                if let Err(e) = start_backend(state).await {
                    eprintln!("Failed to auto-start backend: {}", e);
                }
            });
            Ok(())
        })
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::CloseRequested { .. } = event {
                // Clean up backend process on window close
                let app = window.app_handle();
                let state = app.state::<BackendState>();
                let child_option = state.process.lock().unwrap().take();
                if let Some(mut child) = child_option {
                    let _ = child.kill();
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
