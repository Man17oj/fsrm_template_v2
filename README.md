# 💳 Credit Risk Model Cookiecutter Template

A production-ready template for credit risk modeling projects.

---

## 🚀 Quickstart: Using This Template with Cruft

This template leverages [cookiecutter](https://cookiecutter.readthedocs.io/) for project scaffolding and is best managed with [cruft](https://cruft.github.io/cruft/) for easy template updates.

### 1️⃣ Install Cruft

     First, install `cruft` (preferably in a virtual environment):

     ```bash
     pip install cruft
     ```

### 2️⃣ Generate a New Project

     Use `cruft` to create a new project from this template:

     ```bash
     cruft create https://github.com/your-username/credit_risk_model.git
     ```

     You will be prompted to enter values for:
       - `project_name`
       - `project_slug`
       - `author_name`
       - `email`
       - `description`
       - `python_version`

     These are defined in [`cookiecutter.json`](cookiecutter.json).

### 3️⃣ Set Up Your Project

     Navigate into your new project directory:

     ```bash
     cd <your-project-slug>
     ```

     Create a virtual environment and install dependencies:

     ```bash
     make init
     ```

### 4️⃣ Code Formatting & Linting 🧹

     This template uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting, integrated with [pre-commit](https://pre-commit.com/):

     - **Install pre-commit hooks:**

       ```bash
       make precommit-install
       ```

     - **Run formatting and linting on all files:**

       ```bash
       make precommit-run
       ```

     - On every commit, Ruff will automatically fix formatting issues. ✨

---

## 🗂️ Project Structure Explained

Below is an overview of the generated project structure, with explanations for each key file and folder:

```text
cookiecutter.json
{{cookiecutter.project_slug}}/
├── .gitignore                  # 🚫 Specifies files and folders to be ignored by git
├── .pre-commit-config.yaml     # 🔄 Configuration for pre-commit hooks (e.g., Ruff)
├── Dockerfile                  # 🐳 Instructions to build a Docker image for the project
├── Makefile                    # 🛠️ Automation commands (setup, linting, testing, etc.)
├── pyproject.toml              # ⚙️ Project metadata and tool configuration (e.g., Ruff, pytest)
├── README.md                   # 📖 Project documentation (you're reading it!)
├── requirements.txt            # 📦 Python dependencies for the project
├── setup.py                    # 📦 Setup script for packaging and installation
├── .github/
│   ├── pull_request_template.md    # 🔀 Template for pull requests
│   └── ISSUE_TEMPLATE/            # 📝 Templates for GitHub issues
│       └── ...                    # (bug reports, feature requests, etc.)
│   └── workflows/
│       └── lint-and-test.yml      # 🤖 GitHub Actions workflow for CI (linting and testing)
├── config/                    # ⚙️ Configuration files (YAML, JSON, etc.)
├── data/
│   ├── interim/               # 🕓 Intermediate data that has been transformed
│   ├── processed/             # ✅ Final, cleaned data ready for modeling
│   └── raw/                   # 📥 Original, immutable data dump
├── models/                    # 🧠 Trained models and serialized model artifacts
├── notebooks/                 # 📓 Jupyter notebooks for exploration and analysis
├── reports/
│   └── figures/               # 📊 Generated plots and figures for reporting
├── src/
│   ├── __init__.py            # 📦 Marks the directory as a Python package
│   ├── data/                  # 📂 Data loading and preprocessing scripts
│   ├── features/              # 🏗️ Feature engineering scripts
│   ├── models/                # 🤖 Model training and evaluation code
│   └── utils/                 # 🛠️ Utility functions and helpers
└── tests/
    └── test_sample.py         # 🧪 Example unit test using pytest
```

### 📂 Folder & File Purpose

- **cookiecutter.json**:  
       Defines the template variables for project generation.
- **.gitignore**:  
       Prevents sensitive or unnecessary files from being tracked by git.
- **.pre-commit-config.yaml**:  
       Automates code formatting and linting before commits.
- **Dockerfile**:  
       Enables containerized development and deployment.
- **Makefile**:  
       Simplifies common tasks (setup, linting, testing) with `make` commands.
- **pyproject.toml**:  
       Centralizes configuration for Python tools and dependencies.
- **README.md**:  
       Provides project overview, setup, and usage instructions.
- **requirements.txt**:  
       Lists Python packages required for the project.
- **setup.py**:  
       Allows the project to be installed as a package.
- **.github/**:  
       Contains GitHub-specific templates and CI/CD workflows.
- **config/**:  
       Stores configuration files for experiments or environments.
- **data/**:  
       Organizes datasets into raw, interim, and processed stages.
- **models/**:  
       Stores trained models and related artifacts.
- **notebooks/**:  
       Houses Jupyter notebooks for prototyping and analysis.
- **reports/**:  
       Contains generated reports and visualizations.
- **src/**:  
       Main source code, organized by functionality (data, features, models, utils).
- **tests/**:  
       Unit and integration tests to ensure code quality.

---

> 💡 **Tip:**  
> Each folder is designed to separate concerns and promote best practices for reproducible, maintainable data science and machine learning projects.

---

### 5️⃣ Running Tests 🧪

     Tests are located in the [`tests/`](tests/) directory and use [pytest](https://docs.pytest.org/):

     ```bash
     pytest
     ```

### 6️⃣ Using Docker (Optional) 🐳

     A [Dockerfile](Dockerfile) is provided for containerized development:

     ```bash
     docker build -t my-credit-risk-model .
     docker run -it my-credit-risk-model
     ```

---

## 🛠️ Updating Your Project with Cruft

If the template is updated, you can update your project with:

     ```bash
     cruft update
     ```

---

## 📄 License

This template is provided under the MIT License.

---

## 🙋 Need Help?

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/) 🍪
- [Cruft Documentation](https://cruft.github.io/cruft/) 🧰
- [Ruff Documentation](https://docs.astral.sh/ruff/) 🐕