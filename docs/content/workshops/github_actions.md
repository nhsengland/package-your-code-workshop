# CI/CD with GitHub Actions: Automate Testing and Documentation Deployment

!!! tip "Bonus Workshop - Self-Paced"
    This is an optional, self-paced workshop. You can complete it at your own speed and refer back to it as needed.

!!! info "CI/CD Definitions"
    **Continuous Integration (CI)** automatically tests your code every time you make changes, catching problems early.

    **Continuous Deployment (CD)** automatically deploys your applications when changes are merged, ensuring your users always have the latest version.

    **GitHub Actions** is GitHub's built-in CI/CD platform that runs workflows when events happen in your repository (like pushes, pull requests, or releases).

### Why Use GitHub Actions?

**Catch Issues Early**: Test every change before it's merged into main
**Automate Repetitive Tasks**: No more manual testing and deployment
**Consistent Quality**: Same checks run for everyone, every time
**Fast Feedback**: Know immediately if your changes break something
**Always Up-to-Date Docs**: Documentation deploys automaticallytip "Bonus Workshop - Self-Paced"
    This is an optional, self-paced workshop. You can complete it at your own speed and refer back to it as needed.

Learn how to automate code quality checks, testing, and documentation deployment using GitHub Actions - making your development workflow more professional and reliable.

!!! success "Learning Objectives"

    - Understand GitHub Actions fundamentals and workflow structure
    - Create automated code quality checks with Ruff and pytest
    - Set up conditional documentation building and testing
    - Automate documentation deployment to GitHub Pages
    - Follow CI/CD best practices for Python projects

??? info "Why This Matters for RAP"
    Automated testing and deployment directly supports [Silver RAP](https://nhsdigital.github.io/rap-community-of-practice/introduction_to_RAP/levels_of_RAP/#silver-rap-implementing-best-practice) by ensuring code quality and [Gold RAP](https://nhsdigital.github.io/rap-community-of-practice/introduction_to_RAP/levels_of_RAP/#gold-rap-analysis-as-a-product) by automating the publication process. GitHub Actions helps you maintain consistent code standards, catch issues early, and deploy documentation automatically - essential for professional analytical pipelines.

??? info "What is CI/CD?"

    * **Continuous Integration (CI)** automatically tests your code every time you make changes, catching problems early.
    * **Continuous Deployment (CD)** automatically deploys your applications when changes are merged, ensuring your users always have the latest version.
    * **GitHub Actions** is GitHub's built-in CI/CD platform that runs workflows when events happen in your repository (like pushes, pull requests, or releases).

!!! info "Why Use GitHub Actions?"

    * **Catch Issues Early**: Test every change before it's merged into main
    * **Automate Repetitive Tasks**: No more manual testing and deployment
    * **Consistent Quality**: Same checks run for everyone, every time
    * **Fast Feedback**: Know immediately if your changes break something
    * **Always Up-to-Date Docs**: Documentation deploys automatically

## Task 1: Understanding GitHub Actions Structure

Let's start by understanding how GitHub Actions workflows are organized and what we'll build.

### 1.1 Workflow Structure

GitHub Actions workflows are defined in YAML files stored in `.github/workflows/` directory. Each workflow consists of:

- **Triggers** (when to run): push, pull request, schedule, etc.
- **Jobs** (what to do): groups of steps that run together
- **Steps** (individual tasks): run commands, use actions, etc.

### 1.2 Our CI/CD Strategy

We'll create two workflows following the KISS principle:

```
┌─────────────────────┐    ┌──────────────────────┐
│   Pull Request      │    │    Main Branch       │
│   Quality Checks    │    │    Documentation     │
│                     │    │    Deployment        │
│ ✓ Code Quality      │    │                      │
│ ✓ Tests             │    │ ✓ Build Docs         │
│ ✓ Docs Build        │    │ ✓ Deploy to Pages    │
└─────────────────────┘    └──────────────────────┘
```

**Workflow 1: Quality Checks** (runs on pull requests)
- Code quality with Ruff
- Run pytest test suite  
- Test documentation builds (if docs changed)

**Workflow 2: Deploy Documentation** (runs on main branch)
- Build and deploy documentation to GitHub Pages

## Task 2: Setting Up Quality Checks Workflow

Let's create our first workflow to automatically check code quality when pull requests are opened.

### 2.1 Create the Workflows Directory

First, create the directory structure for GitHub Actions:

```bash
# Create the workflows directory
mkdir -p .github/workflows

# Verify the structure
ls -la .github/
```

### 2.2 Create the Quality Checks Workflow

Create a new file `.github/workflows/quality-checks.yml` and choose the version that matches your project setup:

=== "With pyproject.toml"

    Use this version if you've completed the dependency management workshop:

    ```yaml
    name: Quality Checks # (1)!

    on: # (2)!
      pull_request:
        branches: [ main ]
      push:
        branches: [ main ]

    jobs:
      quality-checks: # (3)!
        runs-on: ubuntu-latest # (4)!
        
        steps:
        - name: Checkout code # (5)!
          uses: actions/checkout@v4
          
        - name: Set up Python # (6)!
          uses: actions/setup-python@v4
          with:
            python-version: '3.12'
            
        - name: Install dependencies # (7)!
          run: |
            pip install ruff pytest
            pip install -e .
            
        - name: Run Ruff linting # (8)!
          run: ruff check practice_level_gp_appointments/
            
        - name: Run Ruff formatting check # (9)!
          run: ruff format --check practice_level_gp_appointments/
            
        - name: Run pytest # (10)!
          run: pytest tests/ -v
            
      docs-check: # (11)!
        runs-on: ubuntu-latest
        if: contains(github.event.pull_request.changed_files, 'docs/') || github.event_name == 'push' # (12)!
        
        steps:
        - name: Checkout code
          uses: actions/checkout@v4
          
        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: '3.12'
            
        - name: Install dependencies # (13)!
          run: |
            pip install mkdocs mkdocs-material
            pip install -e .
            
        - name: Test documentation build # (14)!
          run: mkdocs build --strict
    ```

=== "With requirements.txt"

    Use this version if you haven't set up pyproject.toml yet:

    ```yaml
    name: Quality Checks # (1)!

    on: # (2)!
      pull_request:
        branches: [ main ]
      push:
        branches: [ main ]

    jobs:
      quality-checks: # (3)!
        runs-on: ubuntu-latest # (4)!
        
        steps:
        - name: Checkout code # (5)!
          uses: actions/checkout@v4
          
        - name: Set up Python # (6)!
          uses: actions/setup-python@v4
          with:
            python-version: '3.12'
            
        - name: Install dependencies # (7)!
          run: |
            pip install ruff pytest
            pip install -r requirements.txt
            
        - name: Run Ruff linting # (8)!
          run: ruff check practice_level_gp_appointments/
            
        - name: Run Ruff formatting check # (9)!
          run: ruff format --check practice_level_gp_appointments/
            
        - name: Run pytest # (10)!
          run: pytest tests/ -v
            
      docs-check: # (11)!
        runs-on: ubuntu-latest
        if: contains(github.event.pull_request.changed_files, 'docs/') || github.event_name == 'push' # (12)!
        
        steps:
        - name: Checkout code
          uses: actions/checkout@v4
          
        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: '3.12'
            
        - name: Install dependencies # (13)!
          run: |
            pip install mkdocs mkdocs-material
            pip install -r requirements.txt
            
        - name: Test documentation build # (14)!
          run: mkdocs build --strict
    ```

1. **Workflow name** - appears in GitHub Actions UI
2. **Triggers** - when this workflow runs (pull requests and pushes to main)
3. **First job** - runs code quality checks
4. **Runner environment** - uses latest Ubuntu (free for public repos)
5. **Checkout step** - downloads your repository code
6. **Python setup** - installs Python 3.12
7. **Dependencies** - installs tools and your project dependencies
8. **Linting** - checks code quality with Ruff
9. **Formatting** - ensures consistent code formatting
10. **Testing** - runs the test suite with pytest
11. **Second job** - checks documentation building
12. **Conditional execution** - only runs if docs files changed
13. **Documentation dependencies** - installs MkDocs and your package
14. **Documentation test** - ensures docs build without errors

### 2.3 Understanding the Workflow

Let's break down what this workflow does:

!!! tip "Two Separate Jobs"
    We split this into **two jobs** that run in parallel:
    
    - **`quality-checks`** - Always runs, checks code and tests
    - **`docs-check`** - Only runs if documentation files changed
    
    This saves time and resources when you're only changing code (not docs).

!!! info "Why `--strict` for MkDocs?"
    The `--strict` flag makes MkDocs fail if there are any warnings. This catches issues like:
    
    - Broken internal links
    - Missing pages in navigation  
    - Invalid markdown syntax
    - Plugin configuration errors

## Task 3: Creating the Documentation Deployment Workflow

Now let's create a workflow that automatically deploys documentation to GitHub Pages when changes are merged to main.

### 3.1 Create the Deployment Workflow

Create `.github/workflows/deploy-docs.yml`:

=== "With pyproject.toml"

    ```yaml
    name: Deploy Documentation # (1)!

    on: # (2)!
      push:
        branches: [ main ]
        paths: [ 'docs/**', 'mkdocs.yml', 'pyproject.toml' ]

    permissions: # (3)!
      contents: write

    jobs:
      deploy-docs:
        runs-on: ubuntu-latest
          
        steps:
        - name: Checkout code # (4)!
          uses: actions/checkout@v4
          with:
            fetch-depth: 0
          
        - name: Set up Python # (5)!
          uses: actions/setup-python@v4
          with:
            python-version: '3.12'
            
        - name: Install dependencies # (6)!
          run: |
            pip install mkdocs mkdocs-material
            pip install -e .
            
        - name: Deploy to GitHub Pages # (7)!
          run: mkdocs gh-deploy --force
    ```

=== "With requirements.txt"

    ```yaml
    name: Deploy Documentation # (1)!

    on: # (2)!
      push:
        branches: [ main ]
        paths: [ 'docs/**', 'mkdocs.yml', 'requirements.txt' ]

    permissions: # (3)!
      contents: write

    jobs:
      deploy-docs:
        runs-on: ubuntu-latest
          
        steps:
        - name: Checkout code # (4)!
          uses: actions/checkout@v4
          with:
            fetch-depth: 0
          
        - name: Set up Python # (5)!
          uses: actions/setup-python@v4
          with:
            python-version: '3.12'
            
        - name: Install dependencies # (6)!
          run: |
            pip install mkdocs mkdocs-material
            pip install -r requirements.txt
            
        - name: Deploy to GitHub Pages # (7)!
          run: mkdocs gh-deploy --force
    ```

1. **Deployment workflow** - focuses only on publishing documentation
2. **Specific triggers** - only runs when docs-related files change on main
3. **Permissions** - only needs write access to push to gh-pages branch
4. **Full git history** - fetch-depth: 0 gets complete history for gh-deploy
5. **Python setup** - installs Python 3.12
6. **Install dependencies** - gets MkDocs and your project dependencies
7. **Deploy with MkDocs** - builds and deploys to GitHub Pages in one command

### 3.2 Configure GitHub Pages

!!! info "Skip This Step If..."
    If you've already completed the [**MkDocs Documentation workshop**](mkdocs_documentation.md), you can skip this step as GitHub Pages is already configured for your repository.

If you haven't set up GitHub Pages yet, you need to configure it to serve from the gh-pages branch:

1. **Go to your repository** on GitHub
2. **Click Settings** tab
3. **Scroll down to Pages** section
4. **Under "Source"** select **"Deploy from a branch"**
5. **Choose "gh-pages" branch** and **"/ (root)" folder**
6. **Click Save**

!!! warning "No gh-pages Branch Yet?"
    Don't worry! The `mkdocs gh-deploy` command will create the gh-pages branch automatically on first deployment. GitHub Pages will show an error until we deploy for the first time.

## Task 4: Testing Your Workflows

Now let's test both workflows to make sure they work correctly.

### 4.1 Test the Quality Checks Workflow

First, let's test the quality checks by creating a pull request:

```bash
# Create a new branch
git checkout -b test-github-actions

# Add the workflow files
git add .github/workflows/

# Commit the changes
git commit -m "feat: add GitHub Actions workflows for CI/CD

- Add quality checks workflow for pull requests
- Add documentation deployment workflow
- Includes code linting, testing, and docs building"

# Push the branch
git push origin test-github-actions
```

Now create a pull request on GitHub:

1. **Go to your repository** on GitHub
2. **Click "Compare & pull request"** 
3. **Add a title**: "Add GitHub Actions CI/CD workflows"
4. **Add a description** explaining what you've added
5. **Click "Create pull request"**

!!! success "Watch It Work"
    After creating the pull request, you should see the GitHub Actions workflows start running automatically. Click on the "Checks" tab to see the progress.

### 4.2 Trigger a Documentation Deployment

Once your pull request is merged, test the documentation deployment:

```bash
# Switch back to main and pull the changes
git checkout main
git pull origin main

# Make a small change to documentation
echo "This page was last updated: $(date)" >> docs/content/index.md

# Commit and push
git add docs/content/index.md
git commit -m "docs: add last updated timestamp"
git push origin main
```

This should trigger the documentation deployment workflow automatically.

### 4.3 Verify Everything Works

Check that both workflows are working:

1. **Go to Actions tab** in your GitHub repository
2. **Verify quality checks ran** on your pull request
3. **Verify docs deployment ran** when you pushed to main
4. **Check your GitHub Pages site** is updated

Your documentation should be available at: `https://YOUR-USERNAME.github.io/package-your-code-workshop`

## Task 5: Understanding and Debugging Workflow Results

Let's learn how to interpret workflow results and debug issues when they occur.

### 5.1 Reading Workflow Status

After your workflows run, GitHub Actions provides clear visual indicators in the repository:

1. **Navigate to the Actions tab** in your GitHub repository
2. **Look at the workflow status icons** next to each workflow run
3. **Click on any workflow** to see detailed results

!!! success "Green checkmark - All checks passed"
    Your workflow completed successfully. All tests passed, code quality checks passed, and any deployment steps succeeded.

!!! failure "Red X - Something failed"
    One or more steps in your workflow failed. Click on the workflow to see which step failed and why.

!!! warning "Yellow dot - Workflow is running"
    Your workflow is currently executing. You can click to watch the progress in real-time.

!!! info "Gray circle - Workflow was skipped"
    The workflow didn't run, usually because the trigger conditions weren't met (e.g., no documentation files changed).

### 5.2 Debug a Failed Workflow

When a workflow fails, follow these steps to identify and fix the problem:

1. **Click on the failed workflow** in the Actions tab
2. **Click on the failed job** (it will have a red X icon)
3. **Expand the failed step** to see the detailed error output
4. **Look for the actual error message** (often at the bottom of the log)

!!! tip "Common Issues and Fixes"
    
    **Ruff linting fails:**
    ```bash
    # Fix locally first
    ruff check practice_level_gp_appointments/ --fix
    ruff format practice_level_gp_appointments/
    git commit -am "fix: resolve linting issues"
    ```
    
    **Tests fail:**
    ```bash
    # Run tests locally to debug
    pytest tests/ -v
    # Fix the failing tests, then commit
    ```
    
    **Documentation build fails:**
    ```bash
    # Test docs build locally
    mkdocs build --strict
    # Fix any broken links or syntax errors
    ```

### 5.3 Add Workflow Status Badges

Status badges show the current state of your workflows directly in your README:

1. **Open your README.md file**
2. **Add badge markdown** at the top of the file:

```markdown
# Package Your Code Workshop

![Quality Checks](https://github.com/YOUR-USERNAME/package-your-code-workshop/workflows/Quality%20Checks/badge.svg)
![Deploy Documentation](https://github.com/YOUR-USERNAME/package-your-code-workshop/workflows/Deploy%20Documentation/badge.svg)

Your workshop description here...
```

!!! info "Why Use Badges?"
    Status badges provide immediate visual feedback about your project's health. They show visitors whether your tests are passing and if your documentation is building successfully.



## Best Practices for CI/CD

### Workflow Organization

!!! tip "Keep It Simple"
    
    **Do:**
    - ✅ **One purpose per workflow** - separate quality checks from deployment
    - ✅ **Descriptive names** - "Quality Checks", not "CI"
    - ✅ **Conditional execution** - only run what's needed
    - ✅ **Fast feedback** - fail fast on code quality issues
    
    **Don't:**
    - ❌ **Monolithic workflows** - one massive workflow that does everything
    - ❌ **Unnecessary runs** - testing docs when only code changed
    - ❌ **Silent failures** - always check workflow results

### Security Best Practices

!!! warning "Security Considerations"
    
    **Permissions:**
    - Only grant the minimum permissions needed
    - Use `contents: read` by default
    - Only add `pages: write` for deployment workflows
    
    **Secrets:**
    - Never commit API keys or passwords
    - Use GitHub repository secrets for sensitive data
    - Prefer GitHub's built-in authentication when possible

### Resource Management

!!! info "GitHub Actions Limits"
    
    **Public repositories** get:
    - ✅ **Unlimited minutes** for public repos
    - ✅ **2,000 minutes/month** for private repos (free tier)
    
    **Best practices:**
    - Cache dependencies to speed up builds
    - Skip unnecessary jobs with conditions
    - Use matrix builds carefully (they multiply resource usage)

## Troubleshooting

### Common Workflow Issues

!!! warning "Workflow Not Triggering"
    **Check:**
    - File is in `.github/workflows/` directory
    - YAML syntax is correct (use a YAML validator)
    - Triggers match your intended events
    - Branch names are correct

!!! warning "Permission Denied"
    **For GitHub Pages deployment:**
    - Enable GitHub Pages in repository settings
    - Set source to "GitHub Actions" 
    - Check workflow permissions section

!!! warning "Dependencies Install Fails"
    **Common fixes:**
    - Ensure pyproject.toml is valid
    - Check all dependency groups exist
    - Verify UV installation completed successfully

### Debugging Workflow Files

```bash
# Validate YAML syntax locally
python -c "import yaml; yaml.safe_load(open('.github/workflows/quality-checks.yml'))"

# Check file encoding (should be UTF-8)
file .github/workflows/quality-checks.yml
```

## Checkpoint

Before finishing this workshop, verify you can:

- [ ] Create GitHub Actions workflow files in the correct directory
- [ ] Set up automated code quality checks with Ruff and pytest
- [ ] Configure conditional documentation building
- [ ] Deploy documentation automatically to GitHub Pages
- [ ] Understand workflow status and debug failures
- [ ] Apply CI/CD best practices to your projects

## Next Steps

Congratulations! You've set up professional CI/CD workflows for your Python project.

**Your project now automatically:**

- ✅ **Tests all code changes** before they're merged
- ✅ **Maintains code quality** with automated linting
- ✅ **Deploys documentation** when changes are made
- ✅ **Provides immediate feedback** on pull requests

**Continue improving your workflows:**

- Add more comprehensive tests to your test suite
- Set up notifications for workflow failures
- Create workflows for releasing new versions
- Add security scanning with tools like CodeQL

**Explore other workshop topics:**

- [**Dependency Management**](dependency_management.md) - Modern Python dependency management
- [**Packaging with pyproject.toml**](packaging_pyproject.md) - Professional Python packaging  
- [**Documentation with MkDocs**](mkdocs_documentation.md) - Create beautiful documentation
- [**Pre-Commit Hooks**](precommit_hooks.md) - Catch issues before they reach CI

??? info "Additional Resources"

    ### GitHub Actions

    - [GitHub Actions Documentation](https://docs.github.com/en/actions) - Complete official guide
    - [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) - YAML reference
    - [GitHub Actions Marketplace](https://github.com/marketplace?type=actions) - Pre-built actions
    - [GitHub Actions Examples](https://github.com/actions/starter-workflows) - Template workflows

    ### CI/CD Best Practices

    - [CI/CD Best Practices](https://docs.github.com/en/actions/learn-github-actions/essential-features-of-github-actions) - GitHub's recommendations
    - [Testing Python Applications](https://docs.pytest.org/en/7.1.x/) - pytest documentation
    - [Code Coverage](https://coverage.readthedocs.io/) - Python coverage measurement

    ### GitHub Pages

    - [GitHub Pages Documentation](https://docs.github.com/en/pages) - Official GitHub Pages guide
    - [Custom Domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site) - Using your own domain
    - [MkDocs Deployment](https://www.mkdocs.org/user-guide/deploying-your-docs/) - MkDocs-specific deployment guide

    ### Security

    - [Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions) - Secure workflow practices
    - [Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) - Managing sensitive data
    - [OIDC with GitHub Actions](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect) - Advanced authentication
