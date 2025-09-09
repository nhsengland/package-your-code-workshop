# Documentation with MkDocs: From Setup to GitHub Pages

Learn how to create professional documentation for your Python projects using MkDocs Material, generate automatic API documentation, and deploy to GitHub Pages.

!!! success "Learning Objectives"

    - Set up MkDocs with Material theme and NHS styling
    - Understand mkdocs.yml configuration structure
    - Generate automatic API documentation with mkdocstrings
    - Create and organize documentation pages
    - Deploy your documentation to GitHub Pages

!!! info "Why This Matters for RAP"
    Professional documentation is essential for [Silver RAP](https://nhsdigital.github.io/rap-community-of-practice/introduction_to_RAP/levels_of_RAP/#silver-rap-implementing-best-practice), which requires "well-documented code including user guidance, explanation of code structure & methodology." This workshop teaches you to create documentation that meets these standards automatically.

## Task 1: Understanding MkDocs and Material Theme Setup

Let's explore how MkDocs is already configured in this repository with NHS Data Science team styling.

### 1.1 Examine the Current Setup

First, let's look at the mkdocs.yml configuration file:

```bash
# View the MkDocs configuration
cat mkdocs.yml
```

!!! info "MkDocs Basics"
    [MkDocs](https://www.mkdocs.org/) is a fast, simple static site generator for building project documentation. [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) is a popular theme that provides a modern, responsive design.

### 1.2 Key Configuration Sections

Let's understand the main parts of our mkdocs.yml:

#### Site Information

```yaml
site_name: Package Your Code Workshop # (1)!
site_description: NHS Data Science Workshop - Package Your Code # (2)!
site_author: Joseph Wilson - NHS England - Data Science and Applied AI Team # (3)!
site_url: https://nhsengland.github.io/package-your-code-workshop # (4)!
```

1. Display name shown in browser tab and site header - keep it concise and descriptive
2. Brief description for search engines and social media sharing - appears in meta tags
3. Author information for attribution and contact - helps with project ownership clarity
4. Full URL where the site will be deployed - enables proper linking and canonical URLs

#### Material Theme Configuration

```yaml
theme:
  name: material # (1)!
  language: en # (2)!
  custom_dir: docs/overrides # (3)!
  palette:
    scheme: default # (4)!
    primary: indigo # (5)!
  logo: images/logo/nhs-blue-on-white.jpg # (6)!
  favicon: images/favicon/favicon.ico # (7)!
```

1. Use the Material theme for MkDocs - provides modern, responsive design
2. Set the site language to English for proper accessibility and SEO
3. Point to custom NHS templates and styling overrides
4. Use the default (light) colour scheme - can also be 'slate' for dark mode
5. Set primary colour to indigo to match NHS branding guidelines
6. NHS logo displayed in the site header navigation
7. Custom favicon for the browser tab - uses NHS branding

#### Navigation Structure

```yaml
nav:
  - Home: index.md # (1)!
  - Getting Started: getting_started.md # (2)!
  - Workshops: # (3)!
    - workshops/index.md # (4)!
    - Dependency Management: workshops/dependency_management.md # (5)!
    # ... more workshops
  - API Reference: # (6)!
    - api_reference/index.md # (7)!
```

1. Main landing page - provides project overview and quick start information
2. Detailed setup guide for getting the project running locally
3. Workshop section with dropdown navigation for all tutorials
4. Workshop index page explaining the learning path and prerequisites
5. Individual workshop pages - each covers a specific packaging topic
6. API Reference section for automatically generated documentation
7. API index page with overview of all modules and quick examples

!!! tip "NHS Styling"
    This repository uses NHS branding with custom colours, logos, and styling. The `custom_dir: docs/overrides` points to NHS-specific templates and the `extra_css` section includes NHS styling.

### 1.3 Test the Current Setup

Let's run the documentation server to see what we have:

=== "With UV (If you've done Dependency Management)"

    If you've completed the [Dependency Management workshop](dependency_management.md):

    ```bash
    # Activate your UV environment
    source .venv/bin/activate
    
    # Install documentation dependencies with UV
    uv sync --group docs
    
    # Start the development server
    mkdocs serve
    ```

=== "With pip + venv (Basic Setup)"

    Using the basic repository setup with requirements.txt:

    ```bash
    # Create and activate virtual environment (if not already done)
    python -m venv .venv
    source .venv/bin/activate
    
    # Install documentation dependencies from requirements.txt
    pip install -r requirements.txt
    
    # Start the development server
    mkdocs serve
    ```

Visit `http://127.0.0.1:8000` to see the documentation site running locally.

!!! info "Using GitHub Codespaces?"
    If you're running this in GitHub Codespaces, the port will be automatically forwarded. Look for a popup notification or check the **Ports** tab at the bottom of your VS Code interface. The forwarded URL will look like `https://your-codespace-name-8000.preview.app.github.dev/`

!!! warning "Port Already in Use?"
    If port 8000 is busy, MkDocs will automatically try 8001, 8002, etc. Check the terminal output for the actual URL.

## Task 2: Creating API Documentation with mkdocstrings

Now let's generate automatic API documentation for our Python package using mkdocstrings.

### 2.1 Understand mkdocstrings Configuration

Our mkdocs.yml already includes mkdocstrings setup:

```yaml
plugins:
  - mkdocstrings: # (1)!
      handlers:
        python: # (2)!
          options:
            docstring_style: numpy # (3)!
            members_order: source # (4)!
            show_source: true # (5)!
            show_bases: true # (6)!
```

1. The mkdocstrings plugin automatically generates API documentation from your Python docstrings
2. Use the Python handler to process Python modules and extract documentation
3. Parse docstrings using NumPy format - supports Parameters, Returns, Examples sections
4. Display class members and functions in the same order they appear in source code
5. Include links to the actual source code on GitHub for each function/class
6. Show base classes for inheritance relationships in class documentation

??? info "Docstring Styles"
    [mkdocstrings](https://mkdocstrings.github.io/) supports multiple docstring formats:

    **[NumPy](https://numpydoc.readthedocs.io/en/latest/format.html)** - Structured sections with clear parameter descriptions
    ```python
    def add(x, y):
        """Add two numbers.

        Parameters
        ----------
        x : int
            First number
        y : int
            Second number

        Returns
        -------
        int
            Sum of x and y
        """
    ```

    **[Google](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)** - Clean, readable format popular in modern Python
    ```python
    def add(x, y):
        """Add two numbers.

        Args:
            x (int): First number
            y (int): Second number

        Returns:
            int: Sum of x and y
        """
    ```

    **[Sphinx](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)** - Traditional reStructuredText format
    ```python
    def add(x, y):
        """Add two numbers.

        :param x: First number
        :type x: int
        :param y: Second number
        :type y: int
        :return: Sum of x and y
        :rtype: int
        """
    ```

    **[PEP 257](https://peps.python.org/pep-0257/)** - Basic Python docstring conventions
    ```python
    def add(x, y):
        """Add two numbers and return the result."""
    ```

    mkdocstrings can automatically detect and parse mixed styles within the same project, making it flexible for teams with varying documentation preferences.

### 2.2 Examine Existing Python Modules

Let's look at the structure of our Python package:

```bash
# List the Python modules in our package
ls -la practice_level_gp_appointments/

# Look at an example module with docstrings
head -20 practice_level_gp_appointments/data_processing.py
```

### 2.3 Create API Documentation Pages

Now let's create documentation pages for each module. First, examine the current API reference structure:

```bash
# Check what's in the API reference directory
ls -la docs/content/api_reference/
cat docs/content/api_reference/index.md
```

Let's create individual documentation pages for each module. We'll start with the data processing module:

1. **Create a new file** called `data_processing.md` in the `docs/content/api_reference/` directory
2. **Add the following content**:

```markdown
# Data Processing Module

::: practice_level_gp_appointments.data_processing
```

!!! tip "mkdocstrings Syntax"
    The `::: module.name` syntax tells mkdocstrings to automatically generate documentation for that module, including all functions, classes, and their docstrings.

??? info "Create the Other Module Pages"
    Now create the remaining API documentation pages following the same pattern:

    **Create `analytics.md`** in `docs/content/api_reference/`:
    ```markdown
    # Analytics Module

    ::: practice_level_gp_appointments.analytics
    ```

    **Create `visualization.md`** in `docs/content/api_reference/`:
    ```markdown
    # Visualization Module

    ::: practice_level_gp_appointments.visualization
    ```

    **Create `output.md`** in `docs/content/api_reference/`:
    ```markdown
    # Output Module

    ::: practice_level_gp_appointments.output
    ```

    **Create `pipeline.md`** in `docs/content/api_reference/`:
    ```markdown
    # Pipeline Module

    ::: practice_level_gp_appointments.pipeline
    ```

### 2.4 Update Navigation

Now let's add these new pages to our navigation in mkdocs.yml:

```yaml
nav:
  # ... existing navigation ...
  - API Reference: # (1)!
    - api_reference/index.md # (2)!
    - Data Processing: api_reference/data_processing.md # (3)!
    - Analytics: api_reference/analytics.md # (4)!
    - Visualization: api_reference/visualization.md # (5)!
```

1. Top-level navigation item with dropdown menu for API documentation
2. Overview page explaining the API structure and providing quick examples
3. Dedicated page for data processing functions (loading, cleaning, transforming)
4. Dedicated page for analytical functions (statistics, summaries, calculations)
5. Dedicated page for visualization functions (charts, plots, dashboards)

!!! warning "Edit mkdocs.yml Carefully"
    YAML is sensitive to indentation. Make sure to maintain the same indentation level as existing items in the nav section.

### 2.5 Test API Documentation

Let's see our API documentation in action:

```bash
# If mkdocs serve is still running, it should auto-reload
# Otherwise, restart it:
mkdocs serve
```

Navigate to the API Reference section and explore the automatically generated documentation.

!!! success "What You Should See"
    - Function signatures with parameter types
    - Docstring content formatted nicely
    - Source code links
    - Class inheritance information

## Task 3: Customizing and Organizing Documentation

Let's improve our documentation structure and add some custom content.

### 3.1 Create a Comprehensive API Reference Index

Let's update the API reference index page to include package-level auto-documentation and a clean navigation table:

1. **Open the file** `docs/content/api_reference/index.md`
2. **Replace its contents** with:

```markdown
# API Reference

::: practice_level_gp_appointments

## Module Documentation

| Module | Description | Key Components |
|--------|-------------|----------------|
| [Data Processing](data_processing.md) | Data loading, cleaning, and transformation | DataLoadingStage, DataJoiningStage |
| [Analytics](analytics.md) | Statistical analysis and summaries | SummarisationStage |
| [Visualization](visualization.md) | Chart generation and plotting | Visualization functions |
| [Output](output.md) | Data export and report generation | OutputStage |
| [Pipeline](pipeline.md) | Pipeline orchestration and workflow | NHSPracticeAnalysisPipeline |
```

!!! tip "Complete Documentation"
    The `::: practice_level_gp_appointments` directive automatically generates comprehensive documentation from the package's docstrings, imports, and version information.

### 3.2 Update Navigation

Now let's add all these new pages to our navigation in mkdocs.yml. You'll need to update the API Reference section:

```yaml
nav:
  # ... existing navigation ...
  - API Reference: # (1)!
    - api_reference/index.md # (2)!
    - Data Processing: api_reference/data_processing.md # (3)!
    - Analytics: api_reference/analytics.md # (4)!
    - Visualization: api_reference/visualization.md # (5)!
    - Output: api_reference/output.md # (6)!
    - Pipeline: api_reference/pipeline.md # (7)!
```

1. Top-level navigation item with dropdown menu for API documentation
2. Overview page with package documentation and navigation table
3. Dedicated page for data processing functions and classes
4. Dedicated page for analytical functions and classes
5. Dedicated page for visualization functions and classes
6. Dedicated page for output and export functions
7. Dedicated page for pipeline orchestration classes

!!! warning "Edit mkdocs.yml Carefully"
    YAML is sensitive to indentation. Make sure to maintain the same indentation level as existing items in the nav section.

### 3.3 Test Your API Documentation

Now let's see your API documentation in action:

```bash
# If mkdocs serve is still running, it should auto-reload
# Otherwise, restart it:
mkdocs serve
```

Visit `http://127.0.0.1:8000` and navigate to the API Reference section.

!!! info "Using GitHub Codespaces?"
    If you're running this in GitHub Codespaces, use the forwarded URL from the **Ports** tab instead of localhost. It will look like `https://your-codespace-name-8000.preview.app.github.dev/`

!!! success "What You Should See"
    
    **On the API Reference index page:**
    - Package description and version from the `__init__.py` file
    - All available classes and functions imported at package level
    - Clean navigation table with links to each module
    
    **On individual module pages:**
    - Function signatures with parameter types
    - Docstring content formatted nicely with sections
    - Source code links (if configured)
    - Class inheritance information
    
    **Overall navigation:**
    - API Reference dropdown in the main navigation
    - Each module accessible from the dropdown menu

## Task 4: Deploying to GitHub Pages

Now let's set up your documentation to be deployed to GitHub Pages using the manual method. [GitHub Pages](https://pages.github.com/) is a free static site hosting service can serve your documentation directly from your repository. In this workshop, we'll use the **manual deployment** method where you build locally and push to a `gh-pages` branch.

!!! warning "Make sure you are on a forked repository!"

    If you're following this workshop as part of the complete package-your-code workshop series, you're likely already working on your own fork. You can skip the forking step and continue with the repository you've been using.

    Find out how to fork the repository in the [Getting Started](../getting_started.md) guide.

??? tip "Automatic Deployment with GitHub Actions"
    You can also set up automatic deployment using GitHub Actions, which builds and deploys your documentation automatically when you push changes. This is covered in detail in the [CI/CD with GitHub Actions](../github_actions.md) workshop.

    The automated approach uses workflows that run on GitHub's servers, eliminating the need to build locally and ensuring documentation stays up-to-date with every code change.


### 4.1 Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll down to **Pages** section
4. Under **Source**, select **Deploy from a branch**
5. Choose **gh-pages** branch and **/ (root)** folder
6. Click **Save**

!!! warning "No gh-pages Branch Yet?"
    Don't worry! We'll create it in the next step. GitHub Pages will show an error until we deploy for the first time.

### 4.2 Deploy Using MkDocs

MkDocs has a built-in deployment command for GitHub Pages:

=== "With UV (If you've done Dependency Management)"

    If you've completed the [Dependency Management workshop](dependency_management.md):

    ```bash
    # Build and deploy to GitHub Pages with UV
    uv run mkdocs gh-deploy

    # This command:
    # 1. Runs mkdocs through UV's environment
    # 2. Builds your documentation
    # 3. Creates/updates the gh-pages branch
    # 4. Pushes to GitHub
    ```

=== "With pip + venv (Basic Setup)"

    Using the basic repository setup with requirements.txt:

    ```bash
    # Build and deploy to GitHub Pages
    mkdocs gh-deploy

    # This command:
    # 1. Builds your documentation
    # 2. Creates/updates the gh-pages branch
    # 3. Pushes to GitHub
    ```

!!! success "First Deployment"
    After the first `mkdocs gh-deploy`, your site will be available at:
    `https://YOUR-USERNAME.github.io/package-your-code-workshop/`

### 4.5 Test Your Deployment

After deployment:

1. Visit your GitHub Pages URL
2. Test all navigation links
3. Verify API documentation displays correctly
4. Check that images and styling work

!!! tip "Updates"
    To update your documentation, simply run `mkdocs gh-deploy` again after making changes to your documentation files.

## Checkpoint

Before moving to the next workshop, verify you can:

- [ ] Understand mkdocs.yml configuration structure
- [ ] Run `mkdocs serve` to preview documentation locally
- [ ] Create API documentation pages using mkdocstrings
- [ ] Add new pages to the navigation structure
- [ ] Deploy documentation to GitHub Pages using `mkdocs gh-deploy`
- [ ] Access your documentation at your GitHub Pages URL

## Next Steps

Excellent work! You've created professional documentation that meets RAP standards.

**Continue your learning journey** - these workshops can be done in any order:

- [**Dependency Management**](dependency_management.md) - Modern Python dependency management
- [**Packaging with pyproject.toml**](packaging_pyproject.md) - Make your code installable and reusable
- [**Pre-Commit Hooks**](precommit_hooks.md) - Automate code quality checks
- [**CI/CD with GitHub Actions**](github_actions.md) - Automate testing and deployment

??? info "Additional Resources"

    ### MkDocs and Material Theme

    - [MkDocs Documentation](https://www.mkdocs.org/) - Official MkDocs guide
    - [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - Complete Material theme documentation
    - [MkDocs Configuration](https://www.mkdocs.org/user-guide/configuration/) - mkdocs.yml reference
    - [Material Theme Setup](https://squidfunk.github.io/mkdocs-material/getting-started/) - Getting started with Material

    ### API Documentation

    - [mkdocstrings Documentation](https://mkdocstrings.github.io/) - Automatic API documentation
    - [mkdocstrings Python Handler](https://mkdocstrings.github.io/python/) - Python-specific configuration
    - [NumPy Docstring Guide](https://numpydoc.readthedocs.io/en/latest/format.html) - Docstring formatting standards
    - [Google Style Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) - Alternative docstring format

    ### GitHub Pages and Deployment

    - [GitHub Pages Documentation](https://docs.github.com/en/pages) - Official GitHub Pages guide
    - [MkDocs Deployment](https://www.mkdocs.org/user-guide/deploying-your-docs/) - Deployment options and strategies
    - [GitHub Actions for MkDocs](https://github.com/marketplace/actions/deploy-mkdocs) - Automated deployment options

    ### RAP Documentation Standards

    - [RAP Documentation Requirements](https://nhsdigital.github.io/rap-community-of-practice/introduction_to_RAP/levels_of_RAP/#silver-rap-implementing-best-practice) - Silver RAP documentation standards
    - [NHS Digital Documentation Style](https://service-manual.nhs.uk/content) - NHS content and style guidelines
