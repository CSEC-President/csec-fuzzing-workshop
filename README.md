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
- Clones Fuzzing101 repository directly in the VM

**You're encouraged to review the script before running it** - it's well-commented and shows exactly what will be installed.

## After Setup

```bash
multipass shell fuzzing-vm
cd Fuzzing101/Exercise\ 1
# Follow the exercise instructions
```

Good luck! 🐛

