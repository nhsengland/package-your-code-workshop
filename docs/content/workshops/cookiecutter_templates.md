# Cookiecutter Data Science: Professional Project Templates

*Bonus Workshop - Self-Paced*

Learn how to create standardised, professional data science projects using Cookiecutter Data Science (CCDS), a proven template used by data scientists worldwide.

!!! success "Learning Objectives"

    - Understand the importance of standardized project structure in data science
    - Install and use Cookiecutter to generate professional project templates
    - Create a new data science project using the CCDS template
    - Explore and customize the generated project structure
    - Apply best practices for reproducible data science workflows

!!! info "Why This Matters for RAP"
    Standardized project structure is fundamental to [Silver RAP](https://nhsdigital.github.io/rap-community-of-practice/introduction_to_RAP/levels_of_RAP/#silver-rap-implementing-best-practice) and essential for [Gold RAP](https://nhsdigital.github.io/rap-community-of-practice/introduction_to_RAP/levels_of_RAP/#gold-rap-analysis-as-a-product). Using proven templates like CCDS ensures your projects follow industry best practices from day one, making them more maintainable, collaborative, and reproducible.

## What is Cookiecutter Data Science?

[**Cookiecutter Data Science (CCDS)**](https://cookiecutter-data-science.drivendata.org/) is a standardized project template for data science projects, developed by [DrivenData](https://drivendata.org/) and used by thousands of data scientists worldwide.

!!! quote "From the CCDS Team"
    "A logical, reasonably standardized, but flexible project structure for doing and sharing data science work." - [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/)

### Why Use CCDS?

**🏗️ Consistent Structure**: Every project follows the same layout, making it easy for team members to navigate and contribute.

**📊 Data Science Focused**: Specifically designed for data science workflows with dedicated folders for data, notebooks, models, and reports.

**🔄 Reproducible**: Includes configuration for environment management, dependency tracking, and documentation.

**🚀 Battle Tested**: Used by academic institutions, startups, and Fortune 500 companies for production data science work.

**🤝 Team Collaboration**: New team members can quickly understand and contribute to any CCDS project.

## Task 1: Understanding Project Structure Problems

Before we dive into CCDS, let's understand why standardized project structure matters.

### 1.1 Common Data Science Project Pitfalls

Without a standard structure, data science projects often suffer from:

    my_analysis/
    ├── analysis.ipynb
    ├── data.csv
    ├── data_cleaned.csv
    ├── final_analysis.ipynb
    ├── final_analysis_v2.ipynb
    ├── final_analysis_FINAL.ipynb
    ├── model.pkl
    ├── plot1.png
    ├── plot2.png
    └── README.txt

**Problems with this approach:**

- **Hard to navigate** - No clear organization
- **Not reproducible** - Unclear which files are inputs vs outputs
- **Poor collaboration** - Team members can't find what they need
- **Doesn't scale** - Becomes unwieldy as projects grow
- **RAP non-compliant** - Doesn't meet professional standards

!!! note
    Typically, the projects aren't this bad and the point is exaggerated for effect. However, having logical standardised structures from the start of a project can help ensure consistency and professionalism as the project evolves.

### 1.2 The CCDS Solution

CCDS provides a logical, standardized structure that addresses these problems:

```bash
example/
├── LICENSE            # (1)!
├── Makefile           # (2)!
├── README.md          # (3)!
├── data               # (4)!
│   ├── external
│   ├── interim
│   ├── processed
│   └── raw
├── docs               # (5)!
├── example # (6)!
│   ├── __init__.py
│   ├── config.py
│   ├── dataset.py
│   ├── features.py
│   ├── modeling
│   └── plots.py
├── models             # (7)!
├── notebooks          # (8)!
├── pyproject.toml     # (9)!
├── references         # (10)!
├── reports            # (11)!
│   └── figures
└── tests              # (12)!
```

1. Open-source license
2. Automated commands like `make data` or `make train`
3. Top-level project documentation
4. Data directory with clear pipeline: raw → interim → processed → external
5. MkDocs documentation project
6. Source code package (named after your project)
7. Trained models and predictions
8. Jupyter notebooks for analysis
9. Modern Python project configuration
10. Data dictionaries and manuals
11. Generated reports and figures
12. Unit tests for your code

!!! tip "Benefits of This Structure"
    - **Clear data flow** - From raw → interim → processed
    - **Organized code** - Separate modules for different tasks
    - **Report ready** - Dedicated space for outputs
    - **Team friendly** - Anyone can navigate and contribute
    - **RAP compliant** - Meets professional reproducibility standards

## Task 2: Installing CCDS

Let's get CCDS (Cookiecutter Data Science) set up so we can generate professional project templates.

### 2.1 Install CCDS

CCDS is distributed as a Python package called `cookiecutter-data-science`. Let's install it:

=== "With UV (If you've done Dependency Management)"

    ```bash
    # Install cookiecutter-data-science globally using UV
    uv tool install cookiecutter-data-science
    
    # Verify installation
    uv tool run ccds --version
    ```

    !!! tip "UV Tool Installation"
        Using `uv tool install cookiecutter-data-science` installs the CCDS package globally and isolated from your projects. This is perfect for tools you want to use across multiple projects.

=== "With pip (Traditional approach)"

    ```bash
    # Install cookiecutter-data-science globally
    pip install --user cookiecutter-data-science
    
    # Verify installation
    ccds --version
    ```

=== "With pipx (Recommended by CCDS)"

    ```bash
    # Install cookiecutter-data-science with pipx
    pipx install cookiecutter-data-science
    
    # Verify installation
    ccds --version
    ```

    !!! info "pipx Installation"
        The [official CCDS documentation](https://cookiecutter-data-science.drivendata.org/) recommends using pipx for cross-project utility applications like CCDS.

### 2.2 Verify Installation

Test that CCDS is working correctly:

=== "With UV"

    ```bash
    # Test CCDS
    uv tool run ccds --help
    ```

=== "With pip"

    ```bash
    # Test CCDS
    ccds --help
    ```

!!! success "Expected Output"
    You should see the CCDS help text with available commands and options for creating data science projects.

## Task 3: Creating Your First CCDS Project

Now let's use CCDS to create a professional data science project following the standardized template.

### 3.1 Generate a New Project

We'll create a project for analyzing NHS GP appointment data (similar to our workshop example):

=== "With UV"

    ```bash
    # Create a new CCDS project
    uv tool run ccds https://github.com/drivendataorg/cookiecutter-data-science
    ```

=== "With pip"

    ```bash
    # Create a new CCDS project
    ccds https://github.com/drivendataorg/cookiecutter-data-science
    ```

=== "With pipx"

    ```bash
    # Create a new CCDS project
    ccds https://github.com/drivendataorg/cookiecutter-data-science
    ```

!!! info "CCDS Command"
    The `ccds` command now requires the full GitHub URL to the latest Cookiecutter Data Science template. This ensures you get the most up-to-date version with all the latest features and options.

### 3.2 Configure Your Project

CCDS will prompt you for project details. Here's an example configuration for an NHS data science project:

```bash
$ ccds
You've downloaded /home/jowi60/.cookiecutters/cookiecutter-data-science before. Is it okay to delete and re-download it? [y/n] (y):
project_name (project_name): example_nhs_project # (1)!
repo_name (example_nhs_project): # (2)!
module_name (example_nhs_project): # (3)!
author_name (Your name (or your organization/company/team)): NHS Data Science Team # (4)!
description (A short description of the project.): This is simply an example of using CCDS to create a project # (5)!
python_version_number (3.10): 3.12 # (6)!
Select dataset_storage
    1 - none
    2 - azure
    3 - s3
    4 - gcs
    Choose from [1/2/3/4] (1): # (7)!
Select environment_manager
    1 - virtualenv
    2 - conda
    3 - pipenv
    4 - uv
    5 - pixi
    6 - poetry
    7 - none
    Choose from [1/2/3/4/5/6/7] (1): 4 # (8)!
Select dependency_file
    1 - requirements.txt
    2 - pyproject.toml
    3 - environment.yml
    4 - Pipfile
    5 - pixi.toml
    Choose from [1/2/3/4/5] (1): 2 # (9)!
Select pydata_packages
    1 - none
    2 - basic
    Choose from [1/2] (1): 2 # (10)!
Select testing_framework
    1 - none
    2 - pytest
    3 - unittest
    Choose from [1/2/3] (1): 2 # (11)!
Select linting_and_formatting
    1 - ruff
    2 - flake8+black+isort
    Choose from [1/2] (1): 1 # (12)!
Select open_source_license
    1 - No license file
    2 - MIT
    3 - BSD-3-Clause
    Choose from [1/2/3] (1): 2 # (13)!
Select docs
    1 - mkdocs
    2 - none
    Choose from [1/2] (1): 1 # (14)!
Select include_code_scaffold
    1 - Yes
    2 - No
    Choose from [1/2] (1): 1 # (15)!
```

1. **Project Name**: We want a short and descriptive name for our project.
2. **Repository Name**: This will be the name of the git repository, this defaults to the project name but can be changed.
3. **Module Name**: This is the name of the main Python module for your code, again defaulting to the project name but can be changed.
4. **Author Name**: Use your team or organization name for clarity.
5. **Description**: A brief summary of the project's purpose.
6. **Python Version**: Choose a modern, supported version (e.g., 3.12).
7. **Dataset Storage**: Select `none` unless you plan to use cloud storage.
8. **Environment Manager**: Choose `uv` if you've done the dependency management workshop. It won't create the virtual environment for you, but it will set up the configuration files.
9. **Dependency File**: Choose `pyproject.toml` for modern Python projects.
10. **PyData Packages**: Choose `basic` to include common data science libraries like pandas, numpy, and matplotlib.
11. **Testing Framework**: Choose `pytest` for professional testing.
12. **Linting and Formatting**: Choose `ruff` for fast, modern code quality checks.
13. **Open Source License**: Choose `MIT` for open-source NHS work.
14. **Docs**: Choose `mkdocs` if you plan to use what you have learned in the documentation workshop.
15. **Include Code Scaffold**: Choose `Yes` to get example data processing scripts to help you get started.

After answering all the prompts, CCDS will generate your new project in a directory named after your project. Try creating a project called `nhs-gp-appointment-analysis` to follow along with the example.

### 3.3 Explore Your New Project

Let's examine what CCDS created for us:

```bash
# Navigate to your new project
cd nhs-gp-appointment-analysis

# See the project structure
tree -L 2
# Or if tree isn't available:
find . -type d -maxdepth 2 | sort
```

You can also just open it in an IDE of choice (e.g., VSCode, PyCharm) to explore the files and directories.

!!! info "Project Structure Generated"
    CCDS created a complete project with:
    
    - **Organized directories** for data, code, docs, and outputs
    - **Configuration files** for dependencies and git
    - **Documentation templates** to get you started
    - **Makefile** for common tasks
    - **Git initialization** ready for version control

## Task 4: Understanding the CCDS Structure

Let's explore each part of your new project and understand its purpose.

### 4.1 Data Organization

The `data/` directory follows a clear data processing pipeline:

```bash
# Explore the data structure
ls -la data/
```

**Directory purposes:**
- **`raw/`** - Original, immutable data (never edit these files!)
- **`external/`** - Third-party data sources
- **`interim/`** - Partially processed data
- **`processed/`** - Final, analysis-ready datasets

!!! warning "Data Handling Best Practices"
    
    **DO:**
    - ✅ Keep raw data immutable - never edit original files
    - ✅ Document data sources and processing steps
    - ✅ Use version control for data processing scripts (not the data itself)
    
    **DON'T:**
    - ❌ Put large data files in git (use .gitignore)
    - ❌ Edit raw data files directly
    - ❌ Store personal or sensitive data without proper security

### 4.2 Source Code Organization

The `src/` directory organizes your code by function:

```bash
# Explore the source code structure  
ls -la src/
```

**Code organization:**
- **`data/`** - Scripts for downloading, cleaning, and processing data
- **`features/`** - Code for feature engineering and data transformation
- **`models/`** - Training scripts and model utilities
- **`visualization/`** - Plotting and visualization functions

### 4.3 Project Configuration

Let's examine the key configuration files:

```bash
# Look at the project dependencies
cat pyproject.toml

# Check the README template
head -20 README.md

# See what's ignored by git
cat .gitignore
```

!!! tip "Configuration Benefits"
    CCDS provides:
    
    - **`pyproject.toml`** - Modern Python dependency management
    - **`requirements.txt`** - Fallback for traditional pip workflows  
    - **`.gitignore`** - Sensible defaults for data science (excludes data files, models, etc.)
    - **`Makefile`** - Automated commands for common tasks

### 4.4 Documentation and Reports

```bash
# Explore documentation structure
ls -la docs/
ls -la reports/
```

**Documentation structure:**
- **`docs/`** - Project documentation and guides
- **`reports/`** - Generated analysis reports
- **`reports/figures/`** - Charts and visualizations for reports

## Task 5: Customizing Your CCDS Project

Let's make this project truly yours by adding some initial content and configuration.

### 5.1 Update Project Documentation

Edit the README.md to describe your specific project:

```bash
# Open the README in your editor
# Replace the template content with your project details
```

**Include in your README:**
- **Project overview** - What problem are you solving?
- **Data sources** - Where does your data come from?
- **Key findings** - What have you discovered? (update as you progress)
- **How to reproduce** - Instructions for running your analysis

### 5.2 Set Up Dependencies

Let's add some common data science dependencies to your project:

=== "Modern approach (pyproject.toml)"

    Add these to your `pyproject.toml`:
    
    ```toml
    [project]
    dependencies = [
        "pandas>=2.0.0",
        "numpy>=1.24.0", 
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "scikit-learn>=1.3.0",
        "jupyter>=1.0.0",
    ]
    
    [dependency-groups]
    dev = [
        "pytest>=7.0.0",
        "ruff>=0.1.0",
    ]
    ```

=== "Traditional approach (requirements.txt)"

    Add these to your `requirements.txt`:
    
    ```txt
    pandas>=2.0.0
    numpy>=1.24.0
    matplotlib>=3.7.0
    seaborn>=0.12.0
    scikit-learn>=1.3.0
    jupyter>=1.0.0
    pytest>=7.0.0
    ruff>=0.1.0
    ```

### 5.3 Initialize Version Control

Your project is ready for git:

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Make your first commit
git commit -m "Initial commit: CCDS project structure

Generated using Cookiecutter Data Science template for
NHS GP appointment analysis project."
```

### 5.4 Create Your First Notebook

Let's create an initial analysis notebook:

```bash
# Create a new notebook in the notebooks directory
touch notebooks/01-initial-data-exploration.ipynb
```

!!! tip "Notebook Naming Convention"
    CCDS recommends numbering notebooks for clear progression:
    
    - **`01-initial-data-exploration.ipynb`**
    - **`02-data-cleaning-and-preprocessing.ipynb`** 
    - **`03-exploratory-data-analysis.ipynb`**
    - **`04-model-development.ipynb`**
    - **`05-final-analysis-and-reporting.ipynb`**

## Task 6: Working with Your CCDS Project

Now let's see how to use the project structure for actual data science work.

### 6.1 Using the Makefile

CCDS includes a Makefile with common commands:

```bash
# See available make commands
make help
```

**Common make commands:**
- **`make data`** - Download/generate data
- **`make clean`** - Delete compiled files
- **`make lint`** - Check code style
- **`make requirements`** - Install dependencies

### 6.2 Example Workflow

Here's how a typical CCDS workflow looks:

1. **Add raw data** to `data/raw/`
2. **Create processing scripts** in `src/data/`
3. **Generate clean data** to `data/processed/`
4. **Develop features** using `src/features/`
5. **Train models** with `src/models/`
6. **Create visualizations** using `src/visualization/`
7. **Generate reports** in `reports/`

### 6.3 Integration with Other Workshops

Your CCDS project works perfectly with other workshop tools:

**Dependency Management:**
```bash
# If you've done the dependency management workshop
uv sync  # Install dependencies from pyproject.toml
```

**Documentation:**
```bash
# If you've done the MkDocs workshop
mkdocs new .  # Add documentation site to your project
```

**Code Quality:**
```bash
# If you've done the packaging workshop
ruff check src/  # Lint your source code
```

## Best Practices for CCDS Projects

### Data Science Workflow

!!! tip "Follow the Data Science Process"
    
    **1. Understand the Problem**
    - Document business requirements in `docs/`
    - Define success metrics clearly
    
    **2. Explore the Data**
    - Keep raw data untouched in `data/raw/`
    - Document data quality issues
    - Create initial notebooks for exploration
    
    **3. Prepare the Data**
    - Write reusable scripts in `src/data/`
    - Save processed data to `data/processed/`
    - Version your data processing pipeline
    
    **4. Model and Analyze**
    - Develop models in `src/models/`
    - Save trained models to `models/`
    - Create reproducible training scripts
    
    **5. Communicate Results**
    - Generate reports in `reports/`
    - Create visualizations for stakeholders
    - Document findings and recommendations

### Project Organization

!!! warning "Keep It Organized"
    
    **DO:**
    - ✅ Use descriptive file names with dates/versions
    - ✅ Document your analysis process in notebooks
    - ✅ Write reusable functions in `src/` modules
    - ✅ Keep notebooks clean and well-commented
    - ✅ Regular git commits with clear messages
    
    **DON'T:**
    - ❌ Put everything in one massive notebook
    - ❌ Copy-paste code between notebooks
    - ❌ Mix exploration and production code
    - ❌ Forget to document your assumptions

### Team Collaboration

!!! info "Working with Teams"
    
    **Benefits for teams:**
    - **Onboarding** - New team members know where everything is
    - **Code review** - Consistent structure makes reviews easier
    - **Knowledge sharing** - Clear documentation and organization
    - **Reproducibility** - Anyone can run your analysis
    
    **Tips for collaboration:**
    - Use clear commit messages
    - Document your analysis decisions
    - Share environment setup instructions
    - Regular code reviews and knowledge sharing

## Troubleshooting

### Common Issues

!!! warning "Template Generation Fails"
    ```bash
    # Clear CCDS cache and try again
    rm -rf ~/.cookiecutters/
    uv tool run ccds
    ```

!!! warning "Dependencies Won't Install"
    ```bash
    # Update pip and try again
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

!!! warning "Git Issues"
    ```bash
    # If git isn't initialized
    git init
    git add .
    git commit -m "Initial commit"
    ```

## Checkpoint

Before finishing this workshop, verify you can:

- [ ] Install and use Cookiecutter to generate project templates
- [ ] Create a new data science project using the CCDS template
- [ ] Understand the purpose of each directory in the CCDS structure
- [ ] Customize the project with your own dependencies and documentation
- [ ] Follow best practices for data science project organization
- [ ] Integrate CCDS with other workshop tools (UV, git, etc.)

## Next Steps

Excellent work! You now have a professional, standardized project structure that follows industry best practices.

**Continue building your skills:**

- [**Dependency Management**](dependency_management.md) - Manage project dependencies professionally
- [**Packaging with pyproject.toml**](packaging_pyproject.md) - Make your code installable and reusable
- [**Documentation with MkDocs**](mkdocs_documentation.md) - Create professional project documentation
- [**Pre-Commit Hooks**](precommit_hooks.md) - Automate code quality checks
- [**CI/CD with GitHub Actions**](github_actions.md) - Automate testing and deployment

**Apply CCDS to real projects:**
- Use CCDS for your next data analysis project
- Convert existing projects to follow CCDS structure
- Create team guidelines based on CCDS principles

??? info "Additional Resources"

    ### Cookiecutter Data Science

    - [CCDS Official Website](https://cookiecutter-data-science.drivendata.org/) - Complete documentation and philosophy
    - [CCDS GitHub Repository](https://github.com/drivendata/cookiecutter-data-science) - Source code and issues
    - [DrivenData Blog](https://drivendata.co/blog/) - Articles on data science best practices
    - [CCDS Philosophy](https://cookiecutter-data-science.drivendata.org/#why-use-this-project-structure) - Why this structure works

    ### Cookiecutter Templates

    - [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/) - Complete Cookiecutter guide
    - [Cookiecutter Templates](https://github.com/cookiecutter/cookiecutter#available-cookiecutters) - Other useful templates
    - [Creating Custom Templates](https://cookiecutter.readthedocs.io/en/latest/tutorials.html) - Build your own templates

    ### Data Science Project Management

    - [Good Enough Practices](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510) - Academic paper on scientific computing best practices
    - [The Turing Way](https://the-turing-way.netlify.app/) - Comprehensive guide to reproducible research
    - [Software Carpentry](https://software-carpentry.org/) - Best practices for scientific software

    ### NHS and Healthcare Data Science

    - [RAP Community of Practice](https://nhsdigital.github.io/rap-community-of-practice/) - NHS standards for reproducible analysis
    - [NHS Digital Data Science](https://digital.nhs.uk/about-nhs-digital/our-work/nhs-digital-data-and-technology-standards) - NHS data standards and guidelines
    - [FAIR Data Principles](https://www.go-fair.org/fair-principles/) - Making data Findable, Accessible, Interoperable, Reusable
