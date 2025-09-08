# Dependency Management: From pip to UV

Learn how to transition from traditional Python dependency management to modern tools like `uv` for better performance and reliability.

## What You'll Learn

- � **Understanding traditional pip + venv** workflow and its limitations
- 🚀 **Introducing UV** - the future of Python package management
- 📦 **Organizing dependencies** by purpose (production, development, docs)
- 🔒 **Creating reproducible environments** with lockfiles
- ⚡ **Lightning-fast dependency resolution** with UV

## Part 1: Traditional Python Dependency Management

Let's start by understanding how you've likely been managing dependencies so far.

### Current Setup (pip + venv)

Your project is currently set up using the traditional Python approach:

```bash
# Virtual environment
python -m venv .venv
source .venv/bin/activate

# Dependencies in separate files
pip install -r requirements.txt           # Core dependencies
pip install -r requirements-dev.txt       # Development tools
pip install -r requirements-docs.txt      # Documentation tools
```

### Problems with Traditional Approach

While this works, it has several limitations:

❌ **Slow dependency resolution** - pip can be very slow with complex dependencies
❌ **Unreliable resolution** - pip doesn't always find the best solution
❌ **No lockfiles by default** - hard to ensure reproducible installs
❌ **Manual dependency organisation** - easy to mix up production vs development deps
❌ **Version conflicts** - difficult to detect and resolve

## Part 2: Introducing UV

`uv` is an extremely fast Python package installer and resolver, written in Rust. It's designed to be a drop-in replacement for `pip` and `pip-tools`.

### Why UV?

- **⚡ 10-100x faster** than pip
- **🔒 Reliable dependency resolution** with proper conflict detection  
- **📝 Lockfile support** for reproducible builds
- **🎯 Modern tooling** designed for today's Python ecosystem
- **🔄 Drop-in replacement** for existing pip workflows

## Hands-On Exercise 1: Installing UV

Let's install UV and explore its basic functionality:

### 1.1 Install UV

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### 1.2 Compare Speed: pip vs uv

Let's see the difference in action:

```bash
# Time pip installation (traditional way)
time pip install pandas matplotlib seaborn

# Time uv installation  
time uv add pandas matplotlib seaborn
```

You should see UV is significantly faster! ⚡

## Part 3: Migrating from pip to UV

Now let's migrate our project from the traditional setup to UV.

### 3.1 Convert requirements.txt to pyproject.toml

Instead of separate requirements files, UV uses `pyproject.toml` with organized dependency groups:

**Before (Multiple files):**
```bash
requirements.txt          # Core dependencies
requirements-dev.txt       # Development dependencies  
requirements-docs.txt      # Documentation dependencies
```

**After (Single file):**
```toml
[project]
dependencies = [
    "pandas>=2.1.0",
    "numpy>=1.25.0", 
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
    "plotly>=5.15.0",
]

[dependency-groups]
dev = [
    "pytest>=7.4.0",
    "black>=23.7.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.5.0",
]
docs = [
    "mkdocs-material>=9.1.0",
    "mkdocstrings[python]>=0.23.0",
]
```

### 3.2 Hands-On: Convert Your Project

Let's convert your current setup:

1. **Update pyproject.toml** to use dependency groups (this is already done for you!)

2. **Create UV environment**:
   ```bash
   # Remove old venv
   rm -rf .venv
   
   # Create new UV environment
   uv venv
   source .venv/bin/activate
   ```

3. **Install with UV**:
   ```bash
   # Install all dependencies (production + dev + docs)
   uv sync --all-groups
   
   # Or install specific groups
   uv sync --group dev
   uv sync --group docs
   ```

4. **Test the setup**:
   ```bash
   python main.py
   ```

## Understanding Dependency Groups vs Optional Dependencies

UV supports both patterns. Here's when to use each:

### Dependency Groups (Recommended for UV)
```toml
[dependency-groups]
dev = ["pytest", "black"]
docs = ["mkdocs", "mkdocstrings"]
```

**Advantages:**
- ✅ Better for development workflows
- ✅ Clear separation of concerns
- ✅ Works perfectly with UV commands

### Optional Dependencies (Traditional)
```toml
[project.optional-dependencies]
dev = ["pytest", "black"]
docs = ["mkdocs", "mkdocstrings"]
```

**Advantages:**
- ✅ Standard Python packaging (PEP 621)
- ✅ Works with pip install -e .[dev]
- ✅ Better for distribution

## Working with UV Lockfiles

UV automatically generates `uv.lock` files for reproducible builds:

```bash
# Install dependencies (creates/updates uv.lock)
uv sync --all-groups

# Install from lockfile (exact versions)
uv sync --frozen

# Update dependencies
uv lock --upgrade

# Install specific package
uv add requests>=2.28.0

# Remove package
uv remove requests
```

**🔑 Key Point:** Always commit `uv.lock` to version control for reproducible builds!

## Migration Commands Cheat Sheet

| Traditional pip | Modern UV | Purpose |
|-----------------|-----------|---------|
| `pip install package` | `uv add package` | Add new dependency |
| `pip install -r requirements.txt` | `uv sync` | Install all dependencies |
| `pip install -e .` | `uv sync` | Install in development mode |
| `pip freeze > requirements.txt` | `uv lock` | Create lockfile |
| `pip install --upgrade package` | `uv add package --upgrade` | Upgrade package |

## Best Practices

### ✅ Do This

- **Use dependency groups**: Separate dev, docs, test dependencies
- **Commit lockfiles**: Include `uv.lock` in version control
- **Pin major versions**: `pandas>=2.0.0,<3.0.0`
- **Regular updates**: Use `uv lock --upgrade` monthly
- **Use UV commands**: Replace pip commands with UV equivalents

### ❌ Avoid This

- **Mixing tools**: Don't use pip and UV in the same project
- **Unpinned dependencies**: `pandas` (too loose)
- **Over-pinning**: `pandas==2.1.3` (too strict for libraries)
- **Ignoring lockfiles**: Always commit `uv.lock`

## Troubleshooting

### Common Migration Issues

**Issue**: "Package not found"
```bash
# Solution: Clear cache and retry
uv cache clean
uv sync --all-groups
```

**Issue**: Version conflicts
```bash
# Solution: Use UV's conflict resolution
uv add package-name --resolution lowest-direct
```

**Issue**: Old virtual environment conflicts
```bash
# Solution: Start fresh
rm -rf .venv
uv venv
uv sync --all-groups
```

## Checkpoint ✅

Before moving to the next workshop, verify:

- [ ] UV is installed and working (`uv --version`)
- [ ] You've successfully migrated from pip to UV
- [ ] Your `pyproject.toml` has organized dependency groups
- [ ] You can install dependencies with `uv sync --all-groups`
- [ ] You understand the benefits of UV over traditional pip
- [ ] The `uv.lock` file exists and you understand its purpose

## Next Steps

Excellent work! You've modernized your dependency management workflow. 

Next up: **[Packaging with pyproject.toml](packaging_pyproject.md)** - Learn how to make your code installable and reusable with proper packaging configuration.

## Additional Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [Python Packaging Guide](https://packaging.python.org/)
- [UV vs pip Comparison](https://docs.astral.sh/uv/pip/)
