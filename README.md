
<div class='myheader' style="padding: 60px;
  text-align: center;
  background: #1abc9c;
  color: white;
  font-size: 30px;">
  <h1>GitGorilla 🦍</h1>
<img src="/logo.jpg" alt='git gorilla logo' style=" display: block;
  margin-left: auto;
  margin-right: auto;
  width: 40%;"/>
</div>

**GitGorilla** is a powerful CLI tool that allows you to seamlessly merge multiple Git repositories into a single new repository on GitHub. It automates the creation of the new repository, merges the specified repositories, and provides real-time progress updates, making the process efficient and hassle-free.

## Features

- **Merge Multiple Repositories:** Combine multiple Git repositories into one, preserving their histories.
- **Automatic Remote Repository Creation:** Uses the `gh` tool to create a new repository on GitHub and sets it up for you.
- **Progress Tracking:** Displays a progress bar and status updates to keep you informed throughout the process.
- **Customizable Input:** Accepts various input formats for repository names and URLs.
- **Interactive Environment Setup:** Prompts for and sets a default GitHub username if not already configured.

## Installation

### Prerequisites

- **Python 3.6+**
- **`gh` GitHub CLI tool**: [Install the GitHub CLI](https://cli.github.com/)
- **Git**

### Install GitGorilla

You can install GitGorilla by cloning the repository and installing the dependencies.

```bash
git clone https://github.com/reedjones/gitgorilla.git
cd gitgorilla
pip install -r requirements.txt
```

## Usage

### Basic Command

```bash
python merge_repos.py <repo1> <repo2> <new_repo_name> --public
```

Example:

```bash
python merge_repos.py user/repo1 user/repo2 repo3 my-new-repo --public
```

This command will:

- Create a new public GitHub repository named my-new-repo.
- Merge repo1, repo2, and repo3 into my-new-repo.
- Push the merged content to the new GitHub repository.

## Options

- --public/--private: Set the visibility of the new repository.
- --clone: Automatically clone the new repository to your local machine (default behavior).

### Input Formats

- Full URLs: <https://github.com/user/repo1.git>
- Short URLs: user/repo1
- Repo Names Only: repo1 (defaults to the username set in your environment)

#### Setting Default GitHub Username

If a default GitHub username is not set in your environment, GitGorilla will prompt you to enter one. This will be saved for future use.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue if you encounter any problems.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

Created by Reed Jones - feel free to reach out!
