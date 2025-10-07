# CSEC Fuzzing Workshop

A hands-on introduction to AFL++ fuzzing using [Fuzzing101 Exercise 1](https://github.com/antonio-morales/Fuzzing101/tree/main/Exercise%201).

## Prerequisites

- **Python 3.11+** - If not installed, see: https://www.python.org/downloads/
- macOS, Windows (with Hyper-V), or Linux

## Quick Start

The setup script automates VM creation and installs all dependencies:

```bash
python3 fuzzing101_vm_setup.py
```

**What it does:**
- Installs Multipass (if needed)
- Creates Ubuntu 20.04 VM (2 CPUs, 4GB RAM, 20GB disk)
- Installs build tools, LLVM/Clang, debugging tools
- Installs AFL++ fuzzer (via `apt`, not Docker, not from source)
- Configures system for fuzzing (core pattern, etc.)
- Clones Fuzzing101 repository directly in the VM

**Windows Users**: After Multipass installation, you **must close and reopen your terminal** (or open a new tab) to update the PATH environment variable. Then run the script again.

---

## After Setup

```bash
multipass shell fuzzing-vm
cd Fuzzing101/Exercise\ 1
# Follow the exercise instructions
```

---

## Differences from Official Fuzzing101 Guide

This workshop setup differs from the official Fuzzing101 instructions in several ways:

### 1. AFL++ Installation Method
**Official Guide**: Build AFL++ from source using `make distrib` (note: this command doesn't exist - should be `make all`)

**This Workshop**: Use system package
```bash
sudo apt install -y afl++
```

**Why**: More reliable, no build failures, consistent environment. GCC plugin mode works perfectly for all exercises.

### 2. System Configuration
**Official Guide**: Requires manual core pattern configuration

**This Workshop**: Automatically configured during VM setup
```bash
echo core | sudo tee /proc/sys/kernel/core_pattern
```
# TODO FIX 3, 4
### 3. Compiler Selection
**Official Guide**: Uses `afl-clang-fast` (LLVM mode)

**This Workshop**: Use `afl-cc` (auto-selects best available backend)
```bash
export CC=afl-cc
export CXX=afl-c++
```

**Why**: `afl-cc` automatically picks GCC plugin mode when LLVM isn't available. Works identically for the exercises.

### 4. Additional Tools Pre-installed
The VM comes with tools needed for later exercises:
- 32-bit compilation support (`gcc-multilib`)
- Code coverage tools (`lcov`)
- QEMU for binary-only fuzzing
- Enhanced debugging tools

---

## Optional: Building AFL++ from Source (Advanced)

If you want to learn how AFL++ is built:

```bash
# Inside the VM
multipass shell fuzzing-vm

# Remove system package
sudo apt remove afl++

# Clone and build from source
git clone https://github.com/AFLplusplus/AFLplusplus
cd AFLplusplus
make all
sudo make install
```

**Note**: LLVM mode may fail to build on Ubuntu 20.04, but GCC mode is sufficient for all Fuzzing101 exercises.

---

## Important: Resource Usage

**CPU & Heat**: AFL++ uses 100% CPU continuously - your computer will get hot. The workshop VM is limited to 2 CPUs and 4GB RAM to prevent issues.

**Disk**: Output directories can grow to several GB. Monitor with `df -h` and clean old outputs with `rm -rf ~/fuzzing_xpdf/out/`

---

## VM Management

### Basic Operations
```bash
# Shell into VM
multipass shell fuzzing-vm

# List all VMs
multipass list

# Get VM info
multipass info fuzzing-vm

# Stop the VM
multipass stop fuzzing-vm

# Start the VM
multipass start fuzzing-vm

# Execute command in VM without entering shell
multipass exec fuzzing-vm -- <command>
```

### Removing the VM

**Delete VM completely**:
```bash
# Stop and delete
multipass stop fuzzing-vm
multipass delete fuzzing-vm

# Free up disk space
multipass purge
```

**One-liner**:
```bash
multipass delete fuzzing-vm && multipass purge
```

### Uninstalling Multipass

```bash
# macOS
brew uninstall --cask multipass

# Windows
winget uninstall Canonical.Multipass
# Or: Settings → Apps → Multipass → Uninstall

# Linux
sudo snap remove multipass
```

---

## Basic Linux Commands Reference

Essential commands for navigating the VM and following the exercises:

### Navigation
```bash
# Print current directory
pwd

# List files in current directory
ls

# List with details (size, permissions, dates)
ls -la

# Change directory
cd path/to/directory

# Go to home directory
cd ~
cd $HOME

# Go up one directory
cd ..

# Go to previous directory
cd -
```

### File Operations
```bash
# Create directory
mkdir directory_name

# Remove file
rm filename

# Remove directory and contents
rm -rf directory_name

# Copy file
cp source.txt destination.txt

# Move/rename file
mv oldname.txt newname.txt

# View file contents
cat file.txt

# View file with paging
less file.txt
# (press 'q' to quit)

# Edit file
vim file.txt
nano file.txt
```

### Process Management
```bash
# List running processes
ps aux

# Find specific process
ps aux | grep process_name

# Kill process by PID
kill <PID>

# Kill process by name
pkill process_name

# Stop running command
Ctrl+C
```

### System Information
```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check CPU/memory usage (live)
top
# (press 'q' to quit)

# Download file from URL
wget https://example.com/file.tar.gz

# Extract tar.gz archive
tar -xvzf file.tar.gz
```

### Environment Variables
```bash
# Set variable for current session
export CC=afl-cc
export CXX=afl-c++

# View variable
echo $CC
echo $HOME

# View all environment variables
env
```

### Permissions
```bash
# Make script executable
chmod +x script.sh

# Run executable
./script.sh

# Run with sudo (root privileges)
sudo command
```

### Disclaimer
**Educational Purpose**: This workshop teaches security research techniques for authorized testing only. Use these skills exclusively on systems you own or have explicit permission to test.

**Your Responsibility**: You are solely responsible for how you use this knowledge. The instructor and workshop organizers take no responsibility for:
- Hardware issues (overheating, wear), data loss, or system instability
- Misuse of techniques learned (unauthorized testing, exploitation, or illegal activities)
- Any consequences of your actions

By participating, you agree to use this knowledge ethically and legally, and accept full responsibility for your actions.

---

## Resources

- [Fuzzing101 Repository](https://github.com/antonio-morales/Fuzzing101)
- [AFL++ Documentation](https://github.com/AFLplusplus/AFLplusplus/blob/stable/docs/README.md)
- [Multipass Documentation](https://multipass.run/docs)

---

Good luck! 🐛