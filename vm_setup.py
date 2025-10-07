#!/usr/bin/env python3
"""
Fuzzing101 Exercise 1 - VM Setup Script

DISCLAIMER: This script automates VM creation and package installation on your system.
It will:
- Install Multipass (via Homebrew/winget/snap) if not present
- Create a VM with specified resources (2 CPUs, 4G RAM, 20G disk)
- Install development packages in the VM via apt
- Clone Fuzzing101 repository directly in the VM

Review the source code before running. Use at your own risk.

MANUAL SETUP ALTERNATIVE:
If you prefer not to run this script, follow these steps manually:

1. Install Multipass:
   - macOS:   brew install --cask multipass
   - Windows: winget install Canonical.Multipass
   - Linux:   sudo snap install multipass --classic

2. Create VM:
   multipass launch 20.04 --name fuzzing-vm --cpus 2 --memory 4G --disk 20G

3. Install dependencies:
   multipass exec fuzzing-vm -- sudo apt update
   multipass exec fuzzing-vm -- sudo apt install -y build-essential gcc g++ make wget curl git vim
   multipass exec fuzzing-vm -- sudo apt install -y python3-dev automake flex bison libglib2.0-dev libpixman-1-dev python3-setuptools
   multipass exec fuzzing-vm -- sudo apt install -y lld-11 llvm-11 llvm-11-dev clang-11
   multipass exec fuzzing-vm -- sudo apt install -y gcc-9-plugin-dev libstdc++-9-dev
   multipass exec fuzzing-vm -- sudo apt install -y gdb valgrind

4. Clone repository:
   multipass exec fuzzing-vm -- git clone https://github.com/antonio-morales/Fuzzing101.git

5. Shell into VM:
   multipass shell fuzzing-vm

Target: https://github.com/antonio-morales/Fuzzing101/tree/main/Exercise%201
"""

import os
import sys
import platform
import subprocess
import time
from pathlib import Path


class Colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(msg):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{msg}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.END}\n")


def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")


def print_error(msg):
    print(f"{Colors.FAIL}✗ {msg}{Colors.END}")


def print_info(msg):
    print(f"{Colors.CYAN}ℹ {msg}{Colors.END}")


def print_warning(msg):
    print(f"{Colors.WARNING}⚠ {msg}{Colors.END}")


def run_command(cmd, shell=True, capture_output=False, show_errors=True):  # noqa
    result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)  # noqa
    if result.returncode != 0 and show_errors and not capture_output:
        print_error(f"Command failed: {cmd}")
        if result.stderr:
            print_error(f"stderr: {result.stderr.strip()}")
    return result.stdout.strip() if capture_output else (result.returncode == 0)  # noqa


def detect_os():
    system = platform.system()
    return {"Darwin": "macos", "Windows": "windows", "Linux": "linux"}.get(system, "unsupported")  # noqa


def check_multipass_installed():
    result = run_command("multipass version", capture_output=True, show_errors=False)  # noqa
    return result and "multipass" in result.lower()


def verify_multipass_works():
    result = run_command("multipass list", capture_output=True, show_errors=False)  # noqa
    return result is not None


def install_multipass_macos():
    print_info("Installing Multipass on macOS...")

    if not run_command("brew --version", capture_output=True, show_errors=False):  # noqa
        print_warning("Homebrew not found. Installing...")
        install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'  # noqa
        if not run_command(install_cmd):
            print_error("Failed to install Homebrew")
            return False
        print_success("Homebrew installed")

    if run_command("brew install --cask multipass"):
        print_success("Multipass installed")
        time.sleep(3)
        return verify_multipass_works()
    return False


def install_multipass_windows():
    print_info("Installing Multipass on Windows...")
    if run_command("winget --version", capture_output=True, show_errors=False):  # noqa
        print_info("Attempting installation via winget...")
        if run_command("winget install Canonical.Multipass"):
            print_success("Multipass installed via winget")
            time.sleep(3)
            if verify_multipass_works():
                return True

    print_warning("Please install Multipass manually:")
    print_info("https://canonical.com/multipass/download/windows")
    print_info("\nAfter installation:")
    print_info("1. Restart your terminal")
    print_info("2. Ensure Hyper-V is enabled")
    print_info("3. Run this script again")
    return input("\nInstalled Multipass? (y/n): ").lower() == 'y' and verify_multipass_works()  # noqa


def install_multipass_linux():
    print_info("Installing Multipass on Linux...")
    if run_command("sudo snap install multipass --classic"):
        print_success("Multipass installed")
        time.sleep(3)
        return verify_multipass_works()
    print_error("Failed to install via snap")
    print_info("Visit: https://multipass.run/install")
    return False


def vm_exists(vm_name):
    result = run_command("multipass list", capture_output=True, show_errors=False)  # noqa
    return result and vm_name in result


def get_vm_state(vm_name):
    if not vm_exists(vm_name):
        return None
    result = run_command(f"multipass info {vm_name}", capture_output=True, show_errors=False)  # noqa
    if result and "State:" in result:
        for line in result.split('\n'):
            if "State:" in line:
                return line.split("State:")[-1].strip()
    return None


def ensure_vm_running(vm_name):
    state = get_vm_state(vm_name)
    if state == "Running":
        return True
    if state == "Stopped":
        print_info(f"Starting VM '{vm_name}'...")
        return run_command(f"multipass start {vm_name}")
    return False


def create_vm(vm_name="fuzzing-vm", cpus=2, memory="4G", disk="20G"):
    print_info(f"Creating VM: {vm_name} ({cpus} CPUs, {memory} RAM, {disk} disk)")  # noqa

    if vm_exists(vm_name):
        print_warning(f"VM '{vm_name}' already exists")
        if input("Delete and recreate? (y/n): ").lower() == 'y':
            print_info(f"Deleting VM '{vm_name}'...")
            run_command(f"multipass delete {vm_name}")
            run_command("multipass purge")
            time.sleep(2)
        else:
            return ensure_vm_running(vm_name)

    print_info("Launching VM (this may take a few minutes)...")
    cmd = f"multipass launch 20.04 --name {vm_name} --cpus {cpus} --memory {memory} --disk {disk}"  # noqa
    if run_command(cmd):
        print_success(f"VM '{vm_name}' created")
        time.sleep(5)
        return True
    print_error("Failed to create VM")
    return False


def setup_vm(vm_name="fuzzing-vm"):
    print_info("Setting up development environment in VM...")

    if not ensure_vm_running(vm_name):
        print_error("VM is not running")
        return False

    # Package installation steps with descriptive names
    steps = [
        ("Updating package lists", "sudo apt update"),
        ("Installing build essentials (gcc, g++, make, git, etc.)",
         "sudo apt install -y build-essential gcc g++ make wget curl git vim"),
        ("Installing Python development tools and libraries",
         "sudo apt install -y python3-dev automake flex bison libglib2.0-dev libpixman-1-dev python3-setuptools"),
        ("Installing LLVM/Clang toolchain",
         "sudo apt install -y lld-11 llvm-11 llvm-11-dev clang-11 || sudo apt install -y lld llvm llvm-dev clang"),
        ("Installing GCC plugin development packages",
         "sudo apt install -y gcc-9-plugin-dev libstdc++-9-dev || sudo apt install -y gcc-10-plugin-dev libstdc++-10-dev"),
        ("Installing debugging tools (gdb, valgrind)",
         "sudo apt install -y gdb valgrind"),
    ]

    failed = []
    for description, cmd in steps:
        print_info(description)
        full_cmd = f"multipass exec {vm_name} -- bash -c '{cmd}'"
        if not run_command(full_cmd):
            failed.append(description)
            print_warning(f"Failed: {description}")

    if failed:
        print_warning(f"Some installations failed ({len(failed)}/{len(steps)})")
        return False

    print_success("VM setup complete")
    return True


def clone_fuzzing101(vm_name="fuzzing-vm"):
    print_info("Cloning Fuzzing101 repository in VM...")

    if not ensure_vm_running(vm_name):
        print_error("VM is not running")
        return False

    # Check if repo already exists
    check_cmd = f"multipass exec {vm_name} -- bash -c '[ -d Fuzzing101 ] && echo exists || echo missing'"
    result = run_command(check_cmd, capture_output=True, show_errors=False)

    if result and "exists" in result:
        print_warning("Fuzzing101 directory already exists in VM")
        response = input("Delete and re-clone? (y/n): ").lower()
        if response == 'y':
            print_info("Removing existing directory...")
            run_command(f"multipass exec {vm_name} -- rm -rf Fuzzing101")
        else:
            print_info("Using existing Fuzzing101 directory")
            return True

    clone_cmd = f"multipass exec {vm_name} -- git clone https://github.com/antonio-morales/Fuzzing101.git"
    if run_command(clone_cmd):
        print_success("Fuzzing101 repository cloned successfully")
        return True

    print_error("Failed to clone repository")
    return False


def print_vm_info(vm_name="fuzzing-vm"):
    print_header("Setup Complete!")
    print_success("Fuzzing101 Exercise 1 VM is ready")
    print_warning("Follow exercise instructions at:")
    print_info("https://github.com/antonio-morales/Fuzzing101/tree/main/Exercise%201")  # noqa

    print_header("Commands")
    print_info(f"Shell into VM:  multipass shell {vm_name}")
    print_info(f"Stop VM:        multipass stop {vm_name}")
    print_info(f"Start VM:       multipass start {vm_name}")
    print_info(f"Delete VM:      multipass delete {vm_name} && multipass purge")  # noqa

    print_header("Next Steps")
    print_info(f"1. multipass shell {vm_name}")
    print_info("2. cd Fuzzing101/Exercise\\ 1")
    print_info("3. Follow all exercise instructions step-by-step")


def main():
    print_header("Fuzzing101 Exercise 1 - VM Setup")

    os_type = detect_os()
    print_info(f"Detected OS: {os_type}")

    if os_type == "unsupported":
        print_error("Unsupported OS. Supports: macOS, Windows, Linux")
        sys.exit(1)

    if check_multipass_installed():
        print_success("Multipass installed")
        if not verify_multipass_works():
            print_error("Multipass found but not working correctly")
            sys.exit(1)
    else:
        print_warning("Multipass not found. Installing...")
        install_funcs = {
            "macos": install_multipass_macos,
            "windows": install_multipass_windows,
            "linux": install_multipass_linux
        }
        if not install_funcs[os_type]():
            print_error("Multipass installation failed")
            sys.exit(1)

    vm_name = "fuzzing-vm"
    print_header("VM Configuration")
    print_info(f"VM: {vm_name} | CPUs: 2 | RAM: 4G | Disk: 20G")

    if input("\nProceed? (y/n): ").lower() != 'y':
        sys.exit(0)

    if not create_vm(vm_name):
        sys.exit(1)

    if not setup_vm(vm_name):
        print_warning("VM setup had issues but continuing...")

    if not clone_fuzzing101(vm_name):
        print_error("Failed to clone repository")
        print_info("You can clone it manually later:")
        print_info(f"  multipass shell {vm_name}")
        print_info("  git clone https://github.com/antonio-morales/Fuzzing101.git")

    print_vm_info(vm_name)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n\nCancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)