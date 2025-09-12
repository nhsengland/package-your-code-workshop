# Dependency Management: From pip to the pyroject.toml to uv

Learn how to modernize your Python dependency management by building on traditional `pip + venv` workflows and transitioning to modern tools like `uv` for better organization and performance.

!!! success "Learning Objectives"

    - Master pip + venv fundamentals that form the foundation of Python dependency management
    - Organize dependencies using `pyproject.toml` for better structure and maintainability
    - Understand how simple requirements become complex dependency trees
    - Introduce UV as a modern Python package manager built on solid foundations
    - Create reproducible environments using lockfiles and dependency groups

??? info "Why This Matters for RAP"
    This workshop directly supports [Silver RAP](https://nhsdigital.github.io/rap-community-of-practice/introduction_to_RAP/levels_of_RAP/#silver-rap-implementing-best-practice) by teaching you to include comprehensive dependency information in your repository. You'll learn to structure dependencies using `pyproject.toml`, which not only ensures reproducibility but also shapes your analytical pipeline into a proper package - a key step toward Gold RAP's "code is fully packaged" requirement.

## Task 1: Understanding Traditional Python Dependency Management

Let's start by setting up a traditional Python environment to understand the current approach and its limitations.

### 1.1 Create a Virtual Environment

First, let's create a clean virtual environment using the standard `venv` module:

!!! info inline end "Virtual Environment Basics"
    [Virtual environments](https://docs.python.org/3/tutorial/venv.html) isolate your project dependencies from your system Python installation. The `.venv` directory contains a complete Python installation specific to your project.

```bash
# Create a new virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Verify we're in the virtual environment
which python
```

### 1.2 Examine Current Dependencies

Let's look at what dependencies our project needs:

```bash
# View the current requirements file
cat requirements.txt
```

You should see a mix of dependencies including documentation tools, development tools, and core project dependencies.

### 1.3 Install Dependencies and Observe Complexity

Now let's install these dependencies and see what actually gets installed:

```bash
# Install all requirements
pip install -r requirements.txt

# See what was actually installed (this will be much longer!)
pip freeze
```

!!! warning "Dependency Explosion"
    Notice how our simple requirements file with ~10 packages resulted in many more installed packages. These are sub-dependencies (dependencies of dependencies) that [pip resolved automatically](https://pip.pypa.io/en/stable/topics/dependency-resolution/).

### Understanding Traditional Approach Limitations

The traditional `pip + venv` approach works well for basic projects but has some challenges as projects grow:

- **Mixed dependency purposes**: Production, development, and documentation dependencies are all in one file
- **Sub-dependency visibility**: `pip freeze` shows all packages, making it hard to distinguish your direct dependencies
- **Slower resolution**: [pip can be slow](https://peps.python.org/pep-0508/) with complex dependency trees
- **No built-in lockfiles**: Reproducible environments require manual [`pip freeze`](https://pip.pypa.io/en/stable/cli/pip_freeze/) management

!!! tip "`pip` and `venv` is still valid"
    Don't worry - `pip` and `venv` is still a perfectly valid approach for many projects! We're building on this solid foundation, not replacing it entirely.

## Task 2: Organizing Dependencies with pyproject.toml

Before we introduce `uv`, let's improve our dependency organization using the modern `pyproject.toml` standard.

### 2.1 Understanding pyproject.toml Structure

!!! info inline end "Complete pyproject.toml Guide"
    This section focuses on **dependency management** within pyproject.toml. For comprehensive coverage of project metadata, dynamic versioning, and tool configuration, see our [**Packaging with pyproject.toml**](packaging_pyproject.md) workshop.

The [`pyproject.toml`](https://peps.python.org/pep-0621/) file is the modern standard for Python project configuration. For detailed guidance on writing pyproject.toml files, see the [official writing guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/). Let's examine our current minimal setup:

```bash
# View current pyproject.toml
cat pyproject.toml
```

### 2.2 Add Project Dependencies

Let's organize our dependencies by purpose. Open `pyproject.toml` and add the following sections:

```toml
[project] # (1)!
name = "package-your-code-workshop"
version = "0.1.0"
description = "A workshop demonstrating Python packaging best practices"
dependencies = [ # (2)!
    "pandas>=2.1.0",
    "numpy>=1.25.0",
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
    "plotly>=5.15.0",
    "oops_its_a_pipeline@git+https://github.com/nhsengland/oops-its-a-pipeline.git", # (3)!
    "nhs_herbot@git+https://github.com/nhsengland/nhs_herbot.git",
]

[dependency-groups] # (4)!
docs = [ # (5)!
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
    "mkdocstrings>=0.22.0",
    "mkdocstrings-python>=1.0.0",
]
dev = [ # (6)!
    "ruff>=0.4.0",
    "pytest>=7.4.0",
]

[tool.setuptools.packages.find] # (7)!
include = ["practice_level_gp_appointments*"]
```

1. Core project metadata section following [PEP 621](https://peps.python.org/pep-0621/)
2. Core dependencies required for your application to run in production
3. Git-based dependencies - packages installed directly from repositories
4. Dependency groups for development tools following [PEP 735](https://peps.python.org/pep-0735/)
5. Documentation generation dependencies - only needed when building docs
6. Development tools - only needed when coding and testing
7. Build tool configuration - tells setuptools which packages to include

!!! tip "Why Separate Groups?"
    
    Now you can install exactly what you need:
    
    ```bash
    # Traditional approach - everything mixed together
    pip install -r requirements.txt  # ~50 packages
    
    # Modern approach - install selectively
    pip install -e .         # Core dependencies only
    pip install -e .[dev]    # Core + development tools
    pip install -e .[docs]   # Core + documentation tools
    ```

??? warning "Dependency Groups: Modern Best Practice"
    
    We're using `dependency-groups` as the modern best practice for development tools:
    
    ```toml
    # Modern approach - dependency groups for dev tools
    [dependency-groups]
    dev = ["pytest", "ruff"]
    docs = ["mkdocs", "mkdocs-material"]
    ```
    
    **Dependency groups** are specifically designed for development tools, testing, and build processes. They're supported by modern tools like UV and newer versions of pip.
    
    **For backwards compatibility with older pip versions**, you can still use:
    ```toml
    # Fallback approach - optional dependencies
    [project.optional-dependencies]
    dev = ["pytest", "ruff"]
    docs = ["mkdocs", "mkdocs-material"]  
    ```

### 2.3 Test the New Structure

Let's clean our environment and test our new dependency structure:

```bash
# Deactivate and remove the old environment
deactivate
rm -rf .venv

# Create a fresh environment
python -m venv .venv
source .venv/bin/activate

# Install just core dependencies
pip install -e .

# Test that our package is accessible
python -c "import practice_level_gp_appointments; print('Success')"

# Now install development tools too
pip install -e .[dev]

# Install everything
pip install -e .[dev,docs]
```

??? error "Previously encountered issues with `libodbc.so.2` and `pyodbc`"

    If you encounter an error during this stage related to `libodbc.so.2`, `pyodbc`, or similar it might be some missing system dependencies. These should be installed automatically when you create your container but if you are still getting the error try the following commands:

    ```bash
    sudo apt-get update
    sudo apt-get install -y unixodbc unixodbc-dev

    pip install --force-reinstall pyodbc

    python -c "import practice_level_gp_appointments; print('Success')"
    ```

    This should resolve the issue.

## Task 3: Introducing UV

Now let's introduce [UV](https://docs.astral.sh/uv/), a modern Python package manager built in [Rust](https://www.rust-lang.org/) that builds on the foundations we've established.

### 3.1 Install UV

Let's install [UV](https://docs.astral.sh/uv/) on your system:

```bash
# Install UV (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart your shell or source the new PATH
source ~/.bashrc  # or ~/.zshrc depending on your shell # (1)!

# Verify installation
uv --version
```

1. To check the type of shell you're using, run `echo $SHELL`. If it ends with `zsh`, use `source ~/.zshrc` instead.

!!! info "Windows Installation"
    On Windows, use: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`. For more installation options, see the [UV installation guide](https://docs.astral.sh/uv/getting-started/installation/).

### 3.2 Migrate Existing Project to UV

Let's migrate our existing project to use UV while keeping our pyproject.toml structure. For a comprehensive migration guide, see [Migrating from pip to a UV project](https://docs.astral.sh/uv/guides/migration/pip-to-project/#migrating-from-pip-to-a-uv-project):

```bash
# First, clean the current environment
deactivate
rm -rf .venv

# Create a UV-managed virtual environment
uv venv

# Activate the environment
source .venv/bin/activate

# Install dependencies from pyproject.toml
uv sync --all-groups
```

!!! tip "UV Sync Command"
    `uv sync` reads your `pyproject.toml` and installs all dependencies. The `--all-groups` flag includes all dependency groups (dev, docs, etc.).

### 3.3 Practice: Selective Installation with UV

Now let's practice using UV's dependency groups with the same `optional-dependencies` syntax.

#### Practice Different Installation Patterns

Let's practice installing dependencies for different use cases using our existing pyproject.toml structure:

```bash
# Start with a clean slate
deactivate
rm -rf .venv

# 1. Core dependencies only (production-like)
uv venv
source .venv/bin/activate
uv sync
pip list  # See what got installed

# 2. Add development tools
uv sync --group dev
pip list  # Notice the additional packages

# 3. Clean and try docs only
deactivate
rm -rf .venv
uv venv
source .venv/bin/activate
uv sync --group docs
pip list  # Just core + docs packages

# 4. Everything for full development
uv sync --all-groups
pip list  # All packages
```

??? example "Real-World Scenarios"
    
    **New Developer Setup**: A developer working on code (not docs)
    ```bash
    uv sync --group dev
    ```
    
    **Documentation Writer**: Someone updating docs (not coding)
    ```bash
    uv sync --group docs
    ```
    
    **Production Deployment**: Server needs only core functionality
    ```bash
    uv sync  # No groups = core only
    ```
    
    **CI/CD Pipeline**: Different jobs, different needs
    ```yaml
    # Testing job
    - run: uv sync --group dev
    
    # Documentation job  
    - run: uv sync --group docs
    
    # Production deployment
    - run: uv sync
    ```

### 3.4 Alternative: Building a Project from Scratch with UV

Let's also practice the "greenfield" approach - starting a completely new project with UV:

```bash
# Clean everything
deactivate
rm -rf .venv uv.lock

# Initialize a new UV project
uv init --name package-your-code-workshop --python 3.12

# Create and activate environment
uv venv --python 3.12
source .venv/bin/activate

# Add dependencies one by one (UV builds pyproject.toml automatically)
uv add pandas numpy matplotlib seaborn plotly

# Add development dependencies
uv add --group dev ruff pytest

# Add documentation dependencies  
uv add --group docs mkdocs mkdocs-material mkdocstrings mkdocstrings-python

# Check what UV created
cat pyproject.toml
```

??? tip "UV Auto-Generation"
    
    UV automatically creates and updates your `pyproject.toml` as you add dependencies. This is great for new projects where you want to build up dependencies incrementally.

### 3.5 Understanding UV Lockfiles

UV automatically creates a `uv.lock` file for reproducible builds. Let's explore it:

```bash
# Check if lockfile exists
ls -la uv.lock

# Look at the lockfile structure
head -20 uv.lock

# Install from exact lockfile versions
uv sync --frozen
```

!!! warning "Always Commit Lockfiles"
    Add `uv.lock` to version control to ensure everyone gets exactly the same dependency versions. This is essential for [RAP Gold standard](https://nhsdigital.github.io/rap-community-of-practice/introduction_to_RAP/levels_of_RAP/) reproducibility - your analytical pipelines will run identically across different environments and team members.

## Task 4: Working with UV in Practice

Let's explore common UV workflows you'll use in daily development. For comprehensive guidance on UV project workflows, see the [Working on Projects guide](https://docs.astral.sh/uv/guides/projects/#working-on-projects).

### 4.1 Adding and Removing Dependencies

```bash
# Add a new dependency
uv add requests

# Add a development dependency
uv add --group dev mypy

# Remove a dependency
uv remove requests

# Upgrade all dependencies
uv lock --upgrade
```

### 4.2 Managing Environments

```bash
# Create environment with specific Python version
uv venv --python 3.11

# List available Python versions
uv python list

# Install a specific Python version (if needed)
uv python install 3.11
```

### 4.3 Running Commands

```bash
# Run commands in the UV environment
uv run python --version

# Run the package as a module (uses __main__.py)
uv run python -m practice_level_gp_appointments

# Run a specific script file
uv run python practice_level_gp_appointments/pipeline.py

# Run tools from your environment
uv run ruff check .
```

!!! tip "UV Run"
    `uv run` automatically activates the virtual environment and runs the command, even if you haven't manually activated the environment.

## Migration Command Reference

Here's a quick reference for migrating from pip workflows to UV:

| Traditional pip | Modern UV | Purpose |
|-----------------|-----------|---------|
| `pip install package` | `uv add package` | Add new dependency |
| `pip install -r requirements.txt` | `uv sync` | Install all dependencies |
| `pip install -e .` | `uv sync` | Install project in development mode |
| `pip freeze > requirements.txt` | `uv export > requirements.txt` | Export current environment |
| `pip install --upgrade package` | `uv add package --upgrade` | Upgrade package |
| `python script.py` | `uv run python script.py` | Run Python script |

??? info "Command Details"
    
    **Key differences to note**:
    
    - `uv sync` installs your project and dependencies from `pyproject.toml`
    - `uv export` creates requirements.txt from the current environment
    - `uv lock` updates the lockfile (separate from installation)
    - All UV commands automatically handle virtual environments

## Best Practices

### Dependency Group Organization

!!! tip "Keep It Simple: Two Groups"
    
    **For most projects, you only need two dependency groups**:
    
    - **Core dependencies** (`dependencies`): What your app needs to run
    - **Development dependencies** (`dev`): Tools for coding, testing, linting
    
    **Simple, effective setup**:
    ```toml
    [project]
    dependencies = ["pandas", "requests"]
    
    [dependency-groups]
    dev = ["pytest", "ruff"]
    ```
    
    **Installation**:
    ```bash
    # With UV (modern)
    uv sync --group dev
    
    # With pip (fallback - use optional-dependencies)
    pip install -e .[dev]
    ```

??? example "Advanced: More Granular Groups"
    
    **If your project grows complex, you can break down further**:
    
    - `docs`: Documentation generation tools
    - `test`: Testing-specific dependencies (separate from general dev)
    - `typing`: Type checking tools (mypy, type stubs)
    - `jupyter`: Jupyter notebook dependencies
    
    **Example comprehensive setup**:
    ```toml
    [dependency-groups]
    dev = ["ruff", "pytest"]
    test = ["pytest", "pytest-cov"]
    docs = ["mkdocs", "mkdocs-material"]
    typing = ["mypy", "types-requests"]
    ```
    
    **But honestly, most projects don't need this complexity!**

### Installation Patterns

!!! example "Two Commands You'll Use Most"
    
    ```bash
    # Production deployment
    uv sync
    
    # Development work  
    uv sync --group dev
    ```
    
    That's it! Simple and effective.

??? info "Other Installation Options"
    
    ```bash
    # Install everything (if you have multiple groups)
    uv sync --all-groups
    
    # Install specific groups only
    uv sync --group docs
    uv sync --group test
    
    # Multiple specific groups
    uv sync --group dev --group test
    ```

### Working on Locked-Down Platforms

!!! warning "When You Can't Install UV"
    
    **Many enterprise/NHS environments don't allow installing new tools like UV.** The good news? The organized dependency structure still helps with traditional [pip](https://pip.pypa.io/en/stable/)!
    
    **With organized pyproject.toml, you can still benefit**:
    ```bash
    # Use pip with optional dependencies
    pip install -e .              # Core dependencies only
    pip install -e .[dev]         # Core + development tools
    
    # Or export to requirements files for teams
    uv export --group dev > requirements-dev.txt  # (when UV is available)
    # Then share requirements-dev.txt for pip users
    pip install -r requirements-dev.txt
    ```
    
    **Key benefits even with just pip**:
    - Clear separation of production vs development dependencies
    - Easy to share specific requirement sets with team members
    - Future-ready when you can eventually use modern tools like [Poetry](https://python-poetry.org/) or [Hatch](https://hatch.pypa.io/)
    - Better project organization and documentation

### Do This

- **Organize dependencies**: Use `pyproject.toml` to separate production and development dependencies
- **Use the tools available**: UV when possible, pip when necessary - both work with organized dependencies
- **Pin appropriately**: Use `>=` for minimum versions, avoid overly specific pins
- **Document your setup**: Make it clear how team members should install dependencies
- **Plan for constraints**: Consider locked-down environments when choosing your approach

### Avoid This

- **All dependencies in one place**: Don't mix production and development dependencies
- **Unpinned dependencies**: Specify minimum versions for stability
- **Over-pinning**: Avoid exact version pins unless absolutely necessary
- **Assuming everyone can use modern tools**: Not everyone can install UV on their systems

## Troubleshooting

### Common Issues

!!! warning "Package Not Found"
    ```bash
    # Clear cache and retry
    uv cache clean
    uv sync --all-groups
    ```

!!! warning "Version Conflicts"
    ```bash
    # Use UV's conflict resolution options
    uv add package-name --resolution lowest-direct
    ```

!!! warning "Environment Issues"
    ```bash
    # Start completely fresh
    rm -rf .venv uv.lock
    uv venv
    uv sync --all-groups
    ```

## Checkpoint

Before moving to the next workshop, verify you can:

- [ ] Create and activate virtual environments with both `venv` and `uv`
- [ ] Understand the difference between direct and sub-dependencies
- [ ] Organize dependencies in `pyproject.toml` using dependency groups
- [ ] Install dependencies with both `pip` and `uv sync`
- [ ] Add and remove packages using UV commands
- [ ] Understand the purpose of `uv.lock` files

## Next Steps

Excellent work! You've successfully modernized your dependency management workflow while building on solid `pip + venv` foundations.

**Continue your learning journey** - these workshops can be done in any order:

- [**Packaging with pyproject.toml**](packaging_pyproject.md) - Make your code installable and reusable
- [**Documentation with MkDocs**](mkdocs_documentation.md) - Create professional documentation
- [**Pre-Commit Hooks**](precommit_hooks.md) - Automate code quality checks
- [**CI/CD with GitHub Actions**](github_actions.md) - Automate testing and deployment

??? info "Additional Resources"

    ### RAP Community of Practice

    - [Why Use Virtual Environments](https://nhsdigital.github.io/rap-community-of-practice/training_resources/python/virtual-environments/why-use-virtual-environments/) - RAP guidance on virtual environments for reproducible analysis

    ### UV (Modern Python Package Manager)

    - [UV Documentation](https://docs.astral.sh/uv/) - Complete UV guide and reference
    - [UV Working on Projects](https://docs.astral.sh/uv/guides/projects/#working-on-projects) - Practical UV project workflows
    - [UV Migration Guide](https://docs.astral.sh/uv/guides/migration/pip-to-project/#migrating-from-pip-to-a-uv-project) - Step-by-step pip to UV migration
    - [UV vs pip Comparison](https://docs.astral.sh/uv/pip/) - Detailed comparison of tools

    ### Python Project Configuration

    - [Writing pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) - Official guide to pyproject.toml
    - [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/) - Standard for pyproject.toml
    - [PEP 735 - Dependency Groups](https://peps.python.org/pep-0735/) - Modern dependency organization

    ### Traditional Python Packaging

    - [Python Packaging Guide](https://packaging.python.org/) - Official Python packaging documentation
    - [Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html) - Python.org official guide
    - [pip User Guide](https://pip.pypa.io/en/stable/user_guide/) - Official pip documentation

    ### Best Practices & Standards

    - [Python Packaging Best Practices](https://packaging.python.org/en/latest/guides/) - Official packaging guidelines
    - [Understanding Semantic Versioning](https://semver.org/) - Version specification standards
    - [Python Enhancement Proposals (PEPs)](https://peps.python.org/) - Python standards and proposals
