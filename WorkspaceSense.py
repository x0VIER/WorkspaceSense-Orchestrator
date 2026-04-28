"""
WorkspaceSense - High-fidelity repository state tracking and file indexing.
"""
import os
import json
import hashlib
import logging
import argparse
from pathlib import Path

LOG_FILE = "codex_redundancy.log"
STATE_FILE = "workspace_state.json"

# Configure logging to provide forensic-grade metrics
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] %(message)s'
)

def calculate_file_hash(filepath, chunk_size=8192):
    """Calculates the SHA-256 hash of a file for exact tracking."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Failed to hash {filepath}: {e}")
        return None

def scan_directory(directory_path, exclude_dirs=None):
    """Recursively scans a directory and computes file hashes."""
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.env', '.codex'}
    
    file_manifest = {}
    base_path = Path(directory_path).resolve()
    
    for root, dirs, files in os.walk(base_path):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            # Ignore log and state files to prevent recursive tracking
            if file in [LOG_FILE, STATE_FILE]:
                continue
                
            filepath = Path(root) / file
            try:
                rel_path = str(filepath.relative_to(base_path))
                file_hash = calculate_file_hash(filepath)
                
                if file_hash:
                    file_manifest[rel_path] = {
                        "hash": file_hash,
                        "size": filepath.stat().st_size,
                        "mtime": filepath.stat().st_mtime
                    }
            except Exception as e:
                logging.error(f"Error processing {filepath}: {e}")
                
    return file_manifest

def load_previous_state(state_file):
    """Loads previous manifest for drift detection."""
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load state file: {e}")
    return {}

def save_current_state(state_file, state_data):
    """Saves current manifest."""
    try:
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to save state file: {e}")

def compare_states(old_state, new_state):
    """Compares old and new state to find added, modified, and deleted files."""
    added = []
    modified = []
    deleted = []
    
    for filepath, data in new_state.items():
        if filepath not in old_state:
            added.append(filepath)
        elif old_state[filepath]['hash'] != data['hash']:
            modified.append(filepath)
            
    for filepath in old_state.keys():
        if filepath not in new_state:
            deleted.append(filepath)
            
    return {"added": added, "modified": modified, "deleted": deleted}

def run_workspace_sense(directory_path):
    """
    Main function to execute repository state tracking.
    """
    try:
        logging.info(f"Initiating WorkspaceSense indexer for directory: {directory_path}")
        print(f"Scanning repository structure at {directory_path}...")
        
        current_manifest = scan_directory(directory_path)
        file_count = len(current_manifest)
        
        print(f"Indexing {file_count} source files... [OK]")
        
        previous_state = load_previous_state(STATE_FILE)
        
        if previous_state:
            print("Validating technical manifests against hash-sum database...")
            drift = compare_states(previous_state, current_manifest)
            
            total_drift = len(drift['added']) + len(drift['modified']) + len(drift['deleted'])
            if total_drift == 0:
                print("Repository health status: PERFECT (No environment drift detected).")
                logging.info("No environment drift detected.")
            else:
                print(f"\n[!] ALERT: Environment drift detected! ({total_drift} changes)")
                print(f"  - Added: {len(drift['added'])}")
                print(f"  - Modified: {len(drift['modified'])}")
                print(f"  - Deleted: {len(drift['deleted'])}")
                logging.warning(f"Environment drift detected: {drift}")
        else:
            print("Initial technical manifest created.")
            
        save_current_state(STATE_FILE, current_manifest)
        print("Technical manifest verified.")
        logging.info("WorkspaceSense indexing completed successfully.")
        
    except Exception as e:
        logging.error(f"WorkspaceSense failure: {str(e)}")
        print("Error detected. Check codex_redundancy.log for forensic details.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WorkspaceSense - High-fidelity repository state tracking")
    parser.add_argument("--dir", type=str, default=".", help="Directory to scan (default: current directory)")
    args = parser.parse_args()
    
    run_workspace_sense(args.dir)
