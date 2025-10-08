# CSEC Fuzzing Workshop

A hands-on introduction to AFL++ fuzzing using [Fuzzing101 Exercise 1](https://github.com/antonio-morales/Fuzzing101/tree/main/Exercise%201).

## Prerequisites

- **Python 3.11+** - If not installed, see: https://www.python.org/downloads/
- macOS, Windows (with Hyper-V), or Linux

**Note for Linux users**: The setup script is designed for macOS/Windows. If you're on Linux, follow the manual installation steps in the script's comments to set up your environment.

## Quick Start

The setup script automates VM creation and installs all dependencies:

```bash
python3 vm_setup.py
```

**What it does:**
- Installs Multipass (if needed)
- Creates Ubuntu 20.04 VM (2 CPUs, 4GB RAM, 20GB disk)
- Installs build tools, LLVM/Clang, debugging tools
- Configures core dump pattern for AFL++ fuzzing
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
**Official Guide**: Build AFL++ from source using `make distrib` (which doesnt really exist)

**This Workshop**: Use system package
```bash
sudo apt install -y afl++
```

**Why**: More reliable, no build failures, consistent environment. GCC plugin mode works perfectly for all exercises.

### 2. System Configuration (Core Dumps)
**Official Guide**: Requires manual core pattern configuration
```bash
sudo su
echo core >/proc/sys/kernel/core_pattern
exit
```

**This Workshop**: Automatically configured during VM setup by `vm_setup.py`. You should not need to configure this manually.

**What is core_pattern?**
When a program crashes, Linux can save a "core dump" (a snapshot of the program's memory) to help with debugging. The `core_pattern` setting controls where these dumps go. By default, many systems send crash notifications to an external utility (like `apport` on Ubuntu), which causes delays. AFL++ needs immediate crash detection, so we configure the system to write core dumps directly to a file named "core" in the current directory instead of sending them to an external program.

---

## Optional: Building AFL++ from Source (Advanced)

If you want to learn how AFL++ is built:

```bash
# Inside the VM
multipass shell fuzzing-vm

# Remove system package (if installed)
sudo apt remove afl++

# Clone and build from source
git clone https://github.com/AFLplusplus/AFLplusplus
cd AFLplusplus
make all
sudo make install
```

**Note**: LLVM mode may fail to build on Ubuntu 20.04, but GCC mode is sufficient for all Fuzzing101 exercises.

---

## Important: PDF Corpus for Exercise 1

**Note**: The original Fuzzing101 PDF URLs are outdated and no longer work. Use these updated PDFs instead:

```bash
cd $HOME/fuzzing_xpdf/pdf_examples

# Download updated PDF samples
wget https://academiccatalog.umd.edu/undergraduate/colleges-schools/computer-mathematical-natural-sciences/computer-science/computer-science-major/computer-science-major.pdf
wget https://ontheline.trincoll.edu/images/bookdown/sample-local-pdf.pdf
wget https://academiccatalog.umd.edu/graduate/introduction-university-maryland/introduction-university-maryland.pdf
```

**Performance Tip**: Avoid PDFs larger than 100KB for the initial corpus - they significantly slow down fuzzing.

---

## Understanding Fuzzer Performance (Exec Speed)

When running AFL++, you'll see "exec speed" showing executions per second. Here's what to expect:

**Small programs** (parsers, utilities):
- Good: >5,000 exec/sec
- Acceptable: 1,000-5,000 exec/sec
- Slow: <1,000 exec/sec

**Medium programs** (PDF readers, image processors):
- Good: >1,000 exec/sec 
- Acceptable: 500-1,000 exec/sec
- Slow: <500 exec/sec

**Large programs** (browsers, compilers):
- Good: >100 exec/sec
- Acceptable: 50-100 exec/sec
- Slow: <50 exec/sec

**For this Xpdf exercise**, achieving >1,000 exec/sec with the recommended PDF corpus is good performance.

---

## A note on AFL++ compilers 

AFL++ provides different compilers for instrumenting your code. Here's what they do:

**`afl-clang-fast` / `afl-clang-fast++`** (LLVM mode) - What we use in this workshop
- Uses the LLVM compiler to add instrumentation
- Fast and efficient
- Works with the apt-installed AFL++ package

**`afl-gcc-fast` / `afl-g++-fast`** (GCC plugin mode)
- Uses GCC compiler with a plugin to add instrumentation
- Good alternative when LLVM isn't available
- Not included in older apt packages

**`afl-cc` / `afl-c++`** (Auto-selecting wrapper)
- Automatically picks the best compiler available
- Only in newer AFL++ versions (not in apt package version 2.59d)
- Convenient but not needed for this workshop

---

## Important: Resource Usage

**CPU & Heat**: AFL++ uses 100% CPU continuously - your computer will get hot. The workshop VM is limited to 2 CPUs and 4GB RAM to prevent issues.

**Disk**: Output directories can grow to several GB. You can monitor them with `df -h` and clean old outputs with `rm -rf ~/fuzzing_xpdf/out/`

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

If you want to delete the VM after the workshop to free up disk space, feel free to do so:

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

### Finding Files and Commands
```bash
# Find files by name (searches current directory and subdirectories)
find . -name "filename.txt"
find /path/to/search -name "*.pdf"

# Locate files quickly (uses system database, faster but may be outdated)
locate filename.txt

# Find location of executable/command
which python3
which afl-fuzz

# Show all locations of a command
whereis gcc
```

---

## General Fuzzing Workflow with AFL++

This section provides a general workflow for fuzzing any software target with AFL++. These steps apply to most classic fuzzing scenarios.

### Step 1: Download and Build Target (Normal Compilation)

Obtain the source code of the software you want to fuzz and compile it normally.

**Why**: You need to ensure the software builds and runs correctly before adding instrumentation.

### Step 2: Prepare Input Corpus

Create a directory with sample input files that the software can process.

**Why**: You need test files to verify the software works correctly. Later, (in many cases) same files will be used as the seed corpus for fuzzing.

### Step 3: Test the Normal Build

Run the compiled binary with your sample inputs to confirm it works as expected.

### Step 4: Clean Build Artifacts

Remove all compiled files after verifying the software works.

**Why**: You need a clean slate before recompiling with AFL++ instrumentation (more on instrumentation below).

**Alternative approach**: Some people keep two separate builds - one with the normal compiler for testing, and one with AFL++ for fuzzing. This avoids having to switch between builds.

### Step 5: Install AFL++

There are multiple ways to install AFL++:

**Method 1: System Package (Recommended for beginners and used in this workshop)**
- **Pros**: Fast, reliable, no compilation errors
- **Cons**: May not be the latest version

**Method 2: Build from Source (Advanced)**
- **Pros**: Latest features, full control over build options
- **Cons**: May fail to build (especially LLVM mode), requires build dependencies

For this workshop, we will stick to using the system package.

### Step 6: Recompile Target with AFL++ Instrumentation

Recompile the software using AFL++'s special compilers to add fuzzing instrumentation.

**Why**: AFL++ needs to instrument the binary to track code coverage during fuzzing.

**What is Instrumentation?**
Instrumentation is the process of adding extra code to a program during compilation. This code doesn't change what the program does, but it records information about which parts of the code are executed. When AFL++ instruments a binary, it inserts small "probes" at key points (like the start of functions or branches) that track:
- Which code paths have been executed
- How often each path is taken
- Which branches were taken in conditional statements

This coverage information is crucial for AFL++'s feedback loop - it tells the fuzzer which inputs are "interesting" because they explore new code paths.

**About Compiler Variables:**
- `CC`: C compiler (normally `gcc`, we set it to `afl-clang-fast`)
- `CXX`: C++ compiler (normally `g++`, we set it to `afl-clang-fast++`)

When you set these variables and rebuild, the build system uses AFL++'s compilers instead of the standard ones, automatically instrumenting the code.

### Step 7: Run the Fuzzer

Start AFL++ and let it run. The longer it runs, the more code paths it explores.

**How long to run**: Minutes for simple bugs, hours or days for complex software. Watch the "unique crashes" counter.

### Step 8: Reproduce Crashes

After AFL++ finds crashes, verify them by running the target with the crashing input.

### Step 9: Debug the Crash

Use a debugger (like `gdb`) to understand why the crash occurs.

Analyze the crash to determine:
- What caused it (buffer overflow, null pointer dereference, etc.)
- Where in the code it happened
- If it's exploitable

### Step 10: Analyze Exploitability

Review the source code and crash details to assess if this is a security vulnerability.

- Is it a memory corruption bug?
- Can an attacker control the crash?
- What's the potential impact?

### Step 11: Write an Exploit (Advanced)

If the bug is exploitable, you may develop a proof-of-concept exploit.

**Note**: Only perform this on software you have permission to test. This is for educational and authorized security research only.

### Step 12: Disclosure

If you've found a genuine security vulnerability:
1. Report it to the software vendor/maintainer privately
2. Follow coordinated disclosure practices
3. Request a CVE ID if appropriate (valued by employers and by the community)

---

### Disclaimer
**Educational Purpose**: This workshop teaches security research techniques for authorized testing only. Use these skills exclusively on systems you own or have explicit permission to test.

**Your Responsibility**: You are solely responsible for how you use this knowledge. The instructor and workshop organizers take no responsibility for:
- Hardware issues (overheating, wear), data loss, or system instability
- Misuse of techniques learned (unauthorized testing, exploitation, or illegal activities)
- Any consequences of your actions

By participating, you agree to use this knowledge ethically and legally, and accept full responsibility for your actions.

---

## Fuzzing Resources

### Foundational Resources

These resources cover the basics of fuzzing, core tools, and learning materials:

- [Fuzzing101 Repository](https://github.com/antonio-morales/Fuzzing101) - Step-by-step tutorial series for learning fuzzing from scratch
- [Multipass Documentation](https://multipass.run/docs) - Tool for quickly spinning up Ubuntu VMs (relates to Fuzzing101 setup)
- [AFL++ Documentation](https://github.com/AFLplusplus/AFLplusplus/blob/stable/docs/README.md) - Comprehensive documentation for AFL++, the most popular coverage-guided fuzzer
- [AFL++ Tutorials](https://aflplus.plus/docs/tutorials/) - Good list of tutorials for getting started with AFL++
- [Awesome-Fuzzing](https://github.com/secfigo/Awesome-Fuzzing) - Curated list of fuzzing resources, tools, and papers

### Building Something New (Project Ideas)

These resources showcase advanced techniques, real-world case studies, and novel approaches to fuzzing:

- [Leveling Up Fuzzing: Finding More Vulnerabilities](https://security.googleblog.com/2024/11/leveling-up-fuzzing-finding-more.html) - Google's advanced fuzzing techniques and improvements
- [SMT Solvers Guide](https://de-engineer.github.io/SMT-Solvers/) - Introduction to SMT solvers, useful for constraint-based fuzzing
- [Boosting Skeleton-Driven SMT Solver Fuzzing by Leveraging LLM to Produce Formula Generators](https://arxiv.org/abs/2508.20340) - Latest research on fuzzing techniques
- [Effective Fuzzing: dav1d Case Study](https://googleprojectzero.blogspot.com/2024/10/effective-fuzzing-dav1d-case-study.html) - Real-world example of fuzzing a video decoder
- [Breaking the Sound Barrier: Fuzzing Audio Codecs](https://googleprojectzero.blogspot.com/2025/05/breaking-sound-barrier-part-i-fuzzing.html) - Advanced case study on fuzzing audio processing
- [Jackalope](https://github.com/googleprojectzero/Jackalope) - Customizable, distributed fuzzer from Google Project Zero
- [Fuzzing Ladybird Browser](https://awesomekling.substack.com/p/fuzzing-ladybird-with-tools-from) - Case study on fuzzing a web browser with modern tools
- [JIT Bug Finding with SMT and Fuzzing](https://www.pypy.org/posts/2022/12/jit-bug-finding-smt-fuzzing.html) - Novel approach combining SMT solvers with fuzzing for JIT compilers
- [LLM4Decompile](https://github.com/albertan017/LLM4Decompile) - LLM-based binary decompilation for generating recompilable source code
- [LLAMAFUZZ](https://github.com/SecurityLab-UCD/LLAMAFUZZ) - LLM-enhanced greybox fuzzing for structured data mutation
- [RetroWrite](https://github.com/HexHive/retrowrite) - Binary rewriting framework for efficient binary-only fuzzing instrumentation
- [OSS-Fuzz-Gen](https://github.com/google/oss-fuzz-gen) - Google's LLM-powered fuzz target generation framework
---

Author: Sasha Zyuzin

Good luck! 🐛