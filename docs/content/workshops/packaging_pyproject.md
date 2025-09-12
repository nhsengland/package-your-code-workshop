# Packaging with pyproject.toml: Modern Python Project Configuration

Learn how to properly configure your Python projects using pyproject.toml, the modern standard for Python packaging and project metadata.

!!! success "Learning Objectives"

    - Understand the current minimal pyproject.toml configuration
    - Add comprehensive project metadata and information
    - Configure dynamic version management from `__init__.py`
    - Set up tool configurations for code quality tools
    - Follow modern Python packaging standards

!!! info "Why This Matters for RAP"
    Proper project configuration is essential for [Gold RAP](https://nhsdigital.github.io/rap-community-of-practice/introduction_to_RAP/levels_of_RAP/#gold-rap-analysis-as-a-product) and useful for [Silver RAP](https://nhsdigital.github.io/rap-community-of-practice/introduction_to_RAP/levels_of_RAP/#silver-rap-implementing-good-analytical-practices). The pyproject.toml file standardizes how Python projects are configured, making them more maintainable, discoverable, and professional. For Silver RAP and above, many development tools and settings can be centrally configured in pyproject.toml.

## Task 1: Understanding the Current pyproject.toml

Let's examine what we currently have in our pyproject.toml file.

**You should see:**

```toml
[project] # (1)!
name = "package-your-code-workshop" # (2)!
version = "0.1.0" # (3)!

[tool.setuptools.packages.find] # (4)!
include = ["practice_level_gp_appointments*"] # (5)!
```

1. The `[project]` section contains core project metadata defined by [PEP 621](https://peps.python.org/pep-0621/)
2. Project name - must be unique if publishing to PyPI, should follow Python naming conventions
3. Static version number - we'll configure this to be dynamic later in the workshop
4. Tool-specific configuration section for setuptools (our build backend)
5. Tells setuptools which packages to include when building - the `*` includes subpackages

## Task 2: Adding Comprehensive Project Metadata

Let's expand our project configuration with proper metadata that makes our package professional and discoverable.

### 2.1 Add Core Project Information

Open your `pyproject.toml` file and replace the `[project]` section with **your own details**:

!!! tip inline end "Personalizing Your Package"
    **Make it yours!** Replace "Your Name" and "your.email@nhs.net" with your actual details. This is important for:
    
    - **Attribution** - You get credit for your work alongside the original author
    - **Contact** - People know who to reach for questions about your contributions
    - **Professional development** - Your name appears in package metadata
    - **Portfolio building** - Contributes to your coding portfolio

```toml
[project]
name = "package-your-code-workshop"
version = "0.1.0"
description = "NHS Data Science Workshop - Learn to package your Python code professionally" # (1)!
readme = "README.md" # (2)!
license = {text = "MIT"} # (3)!
requires-python = ">=3.9" # (4)!
authors = [ # (5)!
    {name = "Joseph Wilson", email = "joseph.wilson@nhs.net"}, # (6)!
    {name = "Your Name", email = "your.email@nhs.net"}, # (7)!
    {name = "NHS England Data Science Team"},
]
maintainers = [ # (8)!
    {name = "NHS England Data Science Team", email = "datascience@nhs.net"},
]
keywords = ["nhs", "data-science", "packaging", "workshop", "gp-appointments"] # (9)!
```

1. Clear, concise description of what the project does
2. Points to the README file for detailed project information
3. License specification - references the MIT license in our LICENSE file
4. Minimum Python version required - important for compatibility
5. Authors who created the project - can include name and/or email
6. The very good looking, talented, and, most of all, humble creator of this workshop
7. **Add your own name and email here** - you're contributing to this project!
8. Current maintainers responsible for ongoing development
9. Keywords help with discoverability in package indexes

### 2.2 Add Project URLs and Classifiers

Continue adding to your `[project]` section:

!!! tip inline end "Customize Your Project URLs"
    **If you've completed the [MkDocs Documentation workshop](mkdocs_documentation.md)** and set up GitHub Pages, update these URLs to point to **your own** repository and documentation:
    
    - **Homepage & Documentation**: `https://yourusername.github.io/package-your-code-workshop`
    - **Repository**: `https://github.com/yourusername/package-your-code-workshop`
    - **Bug Tracker**: `https://github.com/yourusername/package-your-code-workshop/issues`
    
    This makes your package truly yours and showcases your own documentation site!

```toml
[project.urls] # (1)!
Homepage = "https://nhsengland.github.io/package-your-code-workshop"
Documentation = "https://nhsengland.github.io/package-your-code-workshop"
Repository = "https://github.com/nhsengland/package-your-code-workshop"
"Bug Tracker" = "https://github.com/nhsengland/package-your-code-workshop/issues"

classifiers = [ # (2)!
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
```

1. URLs section provides important project links for users and tools - **customize these!**
2. Classifiers categorize your project in package indexes like PyPI

!!! tip "PyPI Classifiers"
    [PyPI Classifiers](https://pypi.org/classifiers/) are standardized tags that help categorize packages. They improve discoverability and help users understand your project's purpose and compatibility.

### 2.3 Test Your Configuration

Let's verify our configuration is valid:

=== "With UV (If you've done Dependency Management)"

    ```bash
    # Use traditional build tool for dry-run testing
    uv run python -m pip install build
    uv run python -m build --wheel --no-isolation --dry-run
    ```

    !!! info "Why not `uv build`?"
        UV's `uv build` command doesn't have a `--dry-run` option, so we use the traditional build tool to test our configuration without creating files.

=== "With pip + venv (Basic Setup)"

    ```bash
    # Check if pyproject.toml is valid and test build
    python -m pip install build
    python -m build --wheel --no-isolation --dry-run
    ```

!!! success "What You Should See"
    - No syntax errors in the TOML format
    - Build process completes successfully
    - All metadata is properly recognized

## Task 3: Dynamic Version Management

Instead of manually updating version numbers in multiple places, let's configure dynamic versioning from our `__init__.py` file.

### 3.1 Examine Current Version Setup

First, let's see how version is currently defined:

```bash
# Check the version in __init__.py
grep -n "__version__" practice_level_gp_appointments/__init__.py
```

### 3.2 Configure Dynamic Versioning

Update your `[project]` section to use dynamic versioning:

```toml
[project]
name = "package-your-code-workshop"
dynamic = ["version"] # (1)!
description = "NHS Data Science Workshop - Learn to package your Python code professionally"
# ... rest of your project configuration
```

1. Tells build tools that version should be determined dynamically

Then add the setuptools configuration to read from `__init__.py`:

```toml
[tool.setuptools.dynamic] # (1)!
version = {attr = "practice_level_gp_appointments.__version__"} # (2)!
```

1. Setuptools-specific configuration for dynamic fields
2. Points to the `__version__` variable in our package's `__init__.py`

### 3.3 Test Dynamic Versioning

Let's verify the dynamic versioning works:

=== "With UV (If you've done Dependency Management)"

    ```bash
    # Test the build again to ensure version is read correctly
    uv run python -m build --wheel --no-isolation --dry-run
    ```

=== "With pip + venv (Basic Setup)"

    ```bash
    # Test the build again to ensure version is read correctly
    python -m build --wheel --no-isolation --dry-run
    ```

!!! tip "Version Management Benefits"
    - **Single source of truth** - version only defined in `__init__.py`
    - **Automatic consistency** - build tools read the same version
    - **Easier releases** - update version in one place

??? info "Alternative Versioning Approaches"
    Other dynamic versioning options include:
    
    **From Git tags** using `setuptools-scm`:
    ```toml
    # In pyproject.toml
    [project]
    dynamic = ["version"]
    
    [tool.setuptools_scm]
    # Version from git tags (e.g., v1.0.0)
    ```
    ```bash
    # Quick setup
    pip install setuptools-scm
    git tag v0.1.0  # Create your first tag
    ```
    
    **From a VERSION file**:
    ```toml
    # In pyproject.toml
    [tool.setuptools.dynamic]
    version = {file = "VERSION"}
    ```
    ```bash
    # Quick setup
    echo "0.1.0" > VERSION
    ```
    
    **From environment variables**:
    ```toml
    # In pyproject.toml
    [tool.setuptools.dynamic]
    version = {attr = "your_package._version.__version__"}
    ```
    ```python
    # In your_package/_version.py
    import os
    __version__ = os.getenv("PACKAGE_VERSION", "0.1.0-dev")
    ```

## Task 4: Configuring Development Tools

Let's configure code quality tools in our pyproject.toml to maintain consistent coding standards.

### 4.1 Configure Ruff (Linter and Formatter)

Add Ruff configuration to your pyproject.toml:

```toml
[tool.ruff] # (1)!
line-length = 88 # (2)!
target-version = "py39" # (3)!

[tool.ruff.lint] # (4)!
select = [ # (5)!
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # Pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [ # (6)!
    "E501", # line too long (handled by formatter)
]

[tool.ruff.lint.isort] # (7)!
known-first-party = ["practice_level_gp_appointments"]
```

1. Main Ruff configuration section
2. Maximum line length (matches Black default)
3. Target Python version for rule selection
4. Linting-specific configuration
5. Enable specific rule categories for comprehensive checking
6. Disable rules that conflict with the formatter
7. Configure import sorting with our package as first-party

Now remove the old configuration file to avoid conflicts:

```bash
# Remove the old ruff.toml file
rm ruff.toml
```

!!! warning "Configuration Migration"
    After adding Ruff configuration to pyproject.toml, **delete the old ruff.toml file** to prevent configuration conflicts. Ruff reads configuration in a specific order, and having both files can lead to unexpected behavior.

### 4.2 Test Ruff Configuration

Our repository already has Ruff installed and configured. Let's test our new pyproject.toml configuration:

=== "With UV (If you've done Dependency Management)"

    ```bash
    # Run linting with our new pyproject.toml config
    uv run ruff check practice_level_gp_appointments/

    # Run formatting (shows what would change)
    uv run ruff format --diff practice_level_gp_appointments/
    ```

=== "With pip + venv (Basic Setup)"

    ```bash
    # Run linting with our new pyproject.toml config
    ruff check practice_level_gp_appointments/

    # Run formatting (shows what would change)
    ruff format --diff practice_level_gp_appointments/
    ```

!!! tip "Centralizing Configuration"
    By moving Ruff configuration to pyproject.toml, we're centralizing all our project settings in one place. Ruff will automatically read the configuration from pyproject.toml.

!!! tip "Ruff Benefits"
    [Ruff](https://docs.astral.sh/ruff/) is extremely fast and combines multiple tools:
    - **Linter** (replaces flake8, isort, pyupgrade, and more)
    - **Formatter** (replaces Black)
    - **Single tool** instead of managing multiple dependencies

### 4.3 Additional Tool Configurations

??? info "Other Common Tool Configurations"
    You can configure other development tools in pyproject.toml:

    **Pytest Configuration:**
    ```toml
    [tool.pytest.ini_options]
    testpaths = ["tests"]
    python_files = ["test_*.py", "*_test.py"]
    python_classes = ["Test*"]
    python_functions = ["test_*"]
    addopts = "-v --tb=short --strict-markers"
    markers = [
        "slow: marks tests as slow",
        "integration: marks tests as integration tests",
    ]
    ```

    **Black Formatter Configuration:**
    ```toml
    [tool.black]
    line-length = 88
    target-version = ['py39']
    include = '\.pyi?$'
    exclude = '''
    /(
        \.git
      | \.mypy_cache
      | \.tox
      | \.venv
      | _build
      | buck-out
      | build
      | dist
    )/
    '''
    ```

    **Coverage Configuration:**
    ```toml
    [tool.coverage.run]
    source = ["practice_level_gp_appointments"]
    omit = ["*/tests/*", "*/test_*"]

    [tool.coverage.report]
    exclude_lines = [
        "pragma: no cover",
        "def __repr__",
        "raise AssertionError",
        "raise NotImplementedError",
    ]
    ```

    **MyPy Type Checking:**
    ```toml
    [tool.mypy]
    python_version = "3.9"
    warn_return_any = true
    warn_unused_configs = true
    disallow_untyped_defs = true
    ```

### 4.4 Run All Quality Checks

Let's test our complete setup:

=== "With UV (If you've done Dependency Management)"

    ```bash
    # Run ruff linting
    uv run ruff check practice_level_gp_appointments/

    # Run ruff formatting
    uv run ruff format practice_level_gp_appointments/

    # Test the build process
    uv run python -m build --wheel --no-isolation --dry-run
    ```

=== "With pip + venv (Basic Setup)"

    ```bash
    # Run ruff linting
    ruff check practice_level_gp_appointments/

    # Run ruff formatting
    ruff format practice_level_gp_appointments/

    # Test the build process
    python -m build --wheel --no-isolation --dry-run
    ```

!!! success "Quality Assurance Complete"
    Your pyproject.toml now provides:
    - **Professional metadata** for package discovery
    - **Dynamic versioning** for easier maintenance
    - **Tool configuration** for consistent code quality

## Task 5: Using Your Packaged Code in Other Projects

Now that we've properly configured our package, let's see how to use it in other projects - just like we use `nhs_herbot` and `oops_its_a_pipeline` in our dependencies.

### 5.1 Understanding Git-Based Dependencies

In our dependency management workshop, we saw examples like:

```toml
dependencies = [
    "pandas>=2.1.0",
    "oops_its_a_pipeline@git+https://github.com/nhsengland/oops-its-a-pipeline.git",
    "nhs_herbot@git+https://github.com/nhsengland/nhs_herbot.git",
]
```

These are **git-based dependencies** - packages installed directly from GitHub repositories. Now that our project is properly packaged, we can use it the same way!

### 5.2 Make Your Code Available

First, ensure your code is available on GitHub (you should already have this from previous workshops):

```bash
# Check your git status
git status

# If you have uncommitted changes, commit them
git add .
git commit -m "feat: complete pyproject.toml configuration with metadata and tools"

# Push to your repository (if you haven't already)
git push origin main
```

### 5.3 Create a New Test Project

Let's create a simple test project to demonstrate importing your packaged code:

```bash
# Move to a different directory (outside your current project)
cd ..

# Create a new test project directory
mkdir test-import-project
cd test-import-project
```

Now create a `pyproject.toml` file for your test project. **Copy and paste** this content into a new `pyproject.toml` file:

```toml
[project]
name = "test-import-project"
version = "0.1.0"
description = "Testing import of our packaged GP appointments code"
dependencies = [
    "pandas>=2.0.0",
    # We'll add our package dependency here
]
```

### 5.4 Add Your Package as a Dependency

Now let's add your properly packaged code as a git dependency. **Update your `pyproject.toml` file** with your repository details:

!!! tip "Update with Your Repository"
    Replace `YOUR-USERNAME` with your actual GitHub username in the configuration below!

```toml
[project]
name = "test-import-project"
version = "0.1.0"
description = "Testing import of our packaged GP appointments code"
dependencies = [
    "pandas>=2.0.0",
    "package-your-code-workshop@git+https://github.com/YOUR-USERNAME/package-your-code-workshop.git",
]
```

### 5.5 Install and Test Your Package

Now let's install your package and test that we can import it:

=== "With UV"

    ```bash
    # Create virtual environment and install dependencies
    uv venv
    source .venv/bin/activate
    uv sync
    
    # Test importing your package
    uv run python -c "import practice_level_gp_appointments; print('Success. Imported your package')"
    
    # Test accessing your package's functions
    uv run python -c "
    from practice_level_gp_appointments.analytics import SummarisationStage
    print('Successfully imported SummarisationStage class!')
    print(SummarisationStage.__doc__)
    "
    ```

=== "With pip + venv"

    ```bash
    # Create virtual environment and install dependencies
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .
    
    # Test importing your package
    python -c "import practice_level_gp_appointments; print('Success. Imported your package')"
    
    # Test accessing your package's functions
    python -c "
    from practice_level_gp_appointments.analytics import SummarisationStage
    print('Successfully imported SummarisationStage class!')
    print(SummarisationStage.__doc__)
    "
    ```

!!! success "Import Test Complete"
    If the commands above run without errors, your package is successfully configured and can be imported into other projects!

### 5.6 Advanced: Using Specific Versions

You can also specify particular versions, branches, or commits:

```toml
# Specific branch
dependencies = [
    "package-your-code-workshop@git+https://github.com/YOUR-USERNAME/package-your-code-workshop.git@main",
]

# Specific tag/version
dependencies = [
    "package-your-code-workshop@git+https://github.com/YOUR-USERNAME/package-your-code-workshop.git@v1.0.0",
]

# Specific commit
dependencies = [
    "package-your-code-workshop@git+https://github.com/YOUR-USERNAME/package-your-code-workshop.git@abc1234",
]
```

### 5.7 Real-World Example: Team Collaboration

This is exactly how teams share code within organizations:

!!! example "NHS Data Science Team Workflow"
    
    **Team Member A** creates a useful data processing package:
    ```toml
    # In their pyproject.toml
    [project]
    name = "nhs-data-utilities"
    dependencies = ["pandas", "numpy"]
    ```
    
    **Team Member B** uses it in their analysis project:
    ```toml
    # In their analysis project
    [project]
    name = "mortality-trends-analysis"
    dependencies = [
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "nhs-data-utilities@git+https://github.com/nhsengland/nhs-data-utilities.git",
    ]
    ```
    
    **Benefits:**
    - ✅ **Reusable code** - No copy-pasting between projects
    - ✅ **Version control** - Track which version of utilities you're using
    - ✅ **Easy updates** - Update the git reference to get new features
    - ✅ **Team standards** - Everyone uses the same tested, documented code

### 5.8 Best Practices for Git Dependencies

!!! tip "Production Best Practices"

    **DO:**

    - ✅ Use specific tags/versions in production: `@v1.2.0`
    - ✅ Document which projects depend on your package
    - ✅ Use semantic versioning for your releases
    - ✅ Test your package in isolation before tagging releases
    
    **DON'T:**

    - ❌ Point to `@main` in production (versions can change unexpectedly)
    - ❌ Make breaking changes without version bumps
    - ❌ Forget to update documentation when changing interfaces

### 5.9 Integration with PyPI (Optional)

For public packages, you can also publish to PyPI:

```bash
# Build your package
python -m build

# Upload to PyPI (requires account and API token)
python -m twine upload dist/*
```

Then others can install simply with:
```bash
pip install package-your-code-workshop
```

!!! warning "PyPI Publication"
    Only publish to PyPI if your package is intended for public use. For internal NHS/organizational use, git dependencies are often more appropriate.

## Checkpoint

Before moving to the next workshop, verify you can:

- [ ] Understand the structure and purpose of pyproject.toml
- [ ] Add comprehensive project metadata including authors, description, and classifiers
- [ ] Configure dynamic version management from `__init__.py`
- [ ] Set up and run code quality tools like Ruff
- [ ] Build your package successfully with proper metadata
- [ ] Use your packaged code as a dependency in other projects

## Next Steps

Excellent work! You've configured a professional Python project that follows modern standards.

**Continue your learning journey** - these workshops can be done in any order:

- [**Dependency Management**](dependency_management.md) - Modern Python dependency management with UV
- [**Documentation with MkDocs**](mkdocs_documentation.md) - Professional documentation and API reference
- [**Pre-Commit Hooks**](precommit_hooks.md) - Automate code quality checks
- [**CI/CD with GitHub Actions**](github_actions.md) - Automate testing and deployment

??? info "Additional Resources"

    ### pyproject.toml and Packaging

    - [PEP 518 - pyproject.toml](https://peps.python.org/pep-0518/) - Original specification
    - [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/) - Project metadata in pyproject.toml
    - [Python Packaging User Guide](https://packaging.python.org/) - Comprehensive packaging documentation
    - [PyPI Classifiers](https://pypi.org/classifiers/) - Complete list of package classifiers

    ### Code Quality Tools

    - [Ruff Documentation](https://docs.astral.sh/ruff/) - Fast Python linter and formatter
    - [Black Documentation](https://black.readthedocs.io/) - Python code formatter
    - [pytest Documentation](https://docs.pytest.org/) - Testing framework
    - [MyPy Documentation](https://mypy.readthedocs.io/) - Static type checker

    ### Build Tools and Standards

    - [build Documentation](https://build.pypa.io/) - Python package build frontend
    - [setuptools Documentation](https://setuptools.pypa.io/) - Python package build backend
    - [Wheel Format](https://peps.python.org/pep-0427/) - Built distribution format
    - [TOML Specification](https://toml.io/) - Configuration file format

    ### NHS and RAP Standards

    - [RAP Community of Practice](https://nhsdigital.github.io/rap-community-of-practice/) - NHS RAP standards and guidance
