# .github

GitHub meta repository for sbgisen.

## Reusable workflow

### Linter for ROS packages

The workflow can check the following items automatically.

- C++
  - Format (clang-format)
- Python
  - Format (autopep8)
  - Lint (flake8)
- Cmake
  - Format (cmake-format)
- Yaml
  - Lint (yamllint)
- XML (launch files, package.xml, xacro files, urdf files)
  - Format (xmllint)
  - Lint (xmllint)
    - Only launch files and package.xml

#### Input parameters

- inputs.python_version (Optional)

  Use to lint python code.
  Default is `3.8`.

#### Usage

1. Create a GitHub actions workflow file in your repository. e.g. `[repository_root]/.github/workflows/[your_workflow_name].yml`
2. Just add `uses` as in the example file.

    You should set trigger to `on: [pull_request]`.
    Because the workflow suggest format and comment lint error with Pull Request review API.

```yaml
name: [your_workflow_name]

on: [pull_request]

jobs:
  linter_for_ROS_packages:
    name: Linter for ROS packages
    uses: sbgisen/.github/.github/workflows/linter_ros_package.yaml@main
```

### Linter for ROS2 packages

The workflow can check the following items automatically.

- C++
  - Format (clang-format)
- Python
  - Format (yapf)
  - Lint (ruff)
- Cmake
  - Format (cmake-format)
- Yaml
  - Lint (yamllint)
- XML (package.xml, xacro files, urdf files)
  - Format (xmllint)
  - Lint (xmllint)
    - Only launch files and package.xml

#### Input parameters

- inputs.python_version (Optional)

  Use to lint python code.
  Default is `3.12`.

#### Usage

1. Create a GitHub actions workflow file in your repository. e.g. `[repository_root]/.github/workflows/[your_workflow_name].yml`
2. Just add `uses` as in the example file.

    You should set trigger to `on: [pull_request]`.
    Because the workflow suggest format and comment lint error with Pull Request review API.

```yaml
name: [your_workflow_name]

on: [pull_request]

jobs:
  linter:
    name: Linter
    uses: sbgisen/.github/.github/workflows/ros2_style.yaml@main
```

### [Release Drafter](https://github.com/release-drafter/release-drafter)

This repository contains Release Drafter config file.
`.github/release-drafter.yml`

You can call workflow, with the following:

```
    uses: sbgisen/.github/.github/workflows/release-drafter.yml@main
```

### Build ROS package on docker

`ros-build.yml` can be verified that the build of the ROS package located in the repository passes.

#### Input parameters

- secrets.ssh_key

  Use to execute `wstool`.
  Set private SSH key to secrets on the repository/organization.

- secrets.known_hosts

  Use to execute `wstool`.
  Set the result of `ssh-keyscan github.com` to secrets on the repository/organization.

- inputs.package_name (Optional)

  ROS package name.
  Default is `github.event.repository.name`.

- inputs.install_libfreenect2 (Optional)

  Whether the workflow install libfreenect2.
  Default is `false`.

- inputs.run_test (Optional)

  Whether the workflow run rostest.
  Default is `false`.

- inputs.runs_on (Optional)

  Select environment.
  Default is `ubuntu-latest`.
  To use self hosted runner, set tags to this parameter such as `[self-hosted, lab]`

- inputs.setup_script (Optional)

  Setup script filename.
  Default is empty.
  To install/setup dependencies not supported by `wstool` or `rosdep`.

- inputs.ignore_rosinstalls (Optional)

  Specify relative paths from `/path/to/workspace/src` as in `./ros-package/.rosinstall`, separated by commas.
  Default is `./eband_local_planner/.travis.rosinstall`.

#### Usage

You can call workflow, with the following:

```yaml
jobs:
  Build_ROS_package:
    name: Build ROS package
    uses: sbgisen/.github/.github/workflows/ros-build.yml@main
    secrets:
      ssh_key: ${{ secrets.SSH_KEY }}
      known_hosts: ${{ secrets.KNOWN_HOSTS }}
    with:
      install_libfreenect2: false
      run_test: false
      runs_on: ubuntu-latest
```

### Run ROS test

`ros-test.yml` can run ros test.

#### Input parameters

- inputs.package_name (Optional)

  ROS package name.
  Default is `github.event.repository.name`.

- inputs.install_libfreenect2 (Optional)

  Whether the workflow install libfreenect2.
  Default is `false`.

- inputs.setup_script (Optional)

  Setup script filename.
  Default is empty.
  To install/setup dependencies not supported by `wstool` or `rosdep`.

- inputs.ignore_rosinstalls (Optional)

  Specify relative paths from `/path/to/workspace/src` as in `./ros-package/.rosinstall`, separated by commas.
  Default is `./eband_local_planner/.travis.rosinstall`.

#### Usage

1. Please add [self-hosted-runner](https://docs.github.com/ja/actions/hosting-your-own-runners/adding-self-hosted-runners) to the repository/organization to use this job.
    - The job is run on the self hosted server with `self-hosted` and `lab` labels.
1. You can call workflow, with the following:

```yaml
jobs:
  Run_ROS_test:
    name: Run ROS test
    uses: sbgisen/.github/.github/workflows/ros-test.yml@main
    with:
      install_libfreenect2: false
```

### PR agent

`pr-agent.yml` can be used to automatically write descriptions of PRs, review PRs, improve comments, and so on.

#### Input parameters

- inputs.common_extra_instructions

  Common extra instructions for all commands.
  It will be used if the specific instructions are not provided.
  Default is empty.

- inputs.description_extra_instructions

  Description extra instructions.
  Default is empty.

- inputs.review_extra_instructions

  Review extra instructions.
  Default is empty.

- inputs.improve_extra_instructions

  Improve extra instructions.
  Default is empty.

- secrets.openai_key

  Use to call OpenAI API.
  Set OpenAI API key to secrets on the repository/organization.

#### Usage

1. Create a GitHub actions workflow file in your repository. e.g. `[repository_root]/.github/workflows/[your_workflow_name].yml`
2. Just add `uses` as in the example file.

  If you want to automatically comment on PRs created by PR agent when a PR is created, specify `opened` in `pull_request`.

  :warning: Including triggers such as `synchronize` and `reopened` will cause PR agent to run when you add a commit to a PR, etc., consuming a large number of tokens.

  If you don't need to run PR agent automatically on all PRs, but only when you post `/describe` (or `/review`, `/improve` ...) in a comment, specify `created` (or `edited`) in `issue_comment`.

  If you want to generate content in Japanese, you can specify `Please answer in Japanese.` in `**_extra_instructions`.

```yaml
name: [your_workflow_name]

on:
  # For automatically comment on PRs created by PR agent when a PR is created
  pull_request:
    types: [opened]
  # For run PR agent only when you post command in a comment
  issue_comment:
    types: [created, edited]

jobs:
  PR_agent:
    name: PR agent
    uses: sbgisen/.github/.github/workflows/pr_agent.yml@main
    with:
      common_extra_instructions: "Please answer in Japanese." # Optional
    secrets:
      openai_key: ${{ secrets.OPENAI_KEY }}
```

### Claude PR Review

`claude_pr_review.yml` runs [Claude Code](https://github.com/anthropics/claude-code-action) as an automated PR reviewer.
Claude reviews the diff following the org-wide review instructions (`.github/pr-review-instructions.md` in this repository) and submits its feedback as a formal PR review (approve / comment / request changes) with inline comments. A repository can swap in its own instructions file via the `instructions_path` input.

:warning: The [Claude GitHub App](https://github.com/apps/claude) must be installed on the organization (or the repository). Reviews are posted as `claude[bot]` via the app token, which the workflow obtains through OIDC (`id-token: write`).

#### Input parameters

- inputs.model (Optional)

  Model used for the review.
  Default is `claude-sonnet-5`.

- inputs.max_turns (Optional)

  Maximum number of agent turns to avoid runaway costs.
  Default is `50`.

- inputs.instructions_path (Optional)

  Workspace-relative path to the review instructions file. Set this to a file in your
  repository (e.g. `.github/pr-review-instructions.md`) to use repository-specific
  instructions.
  Default is `.sbgisen-github/.github/pr-review-instructions.md` (the org-wide
  instructions checked out from this repository).

- inputs.config_ref (Optional)

  Git ref of this repository (sbgisen/.github) to fetch the org-wide review
  instructions and formatter configs from.
  Default is `main`. Override this only when testing an unmerged branch of the
  reusable workflow.

#### Secrets

Pass the secrets explicitly as in the usage example below:

- secrets.anthropic_api_key (Optional)

  Anthropic API key (Console credits).

- secrets.claude_code_oauth_token (Optional)

  OAuth token for a Claude Pro/Max subscription, generated locally with `claude setup-token`.
  Note that the token is tied to a personal subscription and shares its rate limits; prefer
  `anthropic_api_key` for organization-wide use.

At least one of the two must be set. When both are set, the OAuth token is used.

- secrets.ssh_key (Required)

  SSH private key used to check out dependency repositories.

- secrets.known_hosts (Required)

  SSH known_hosts entries for the dependency repository hosts.

When the repository contains vcstool dependency files (`*.repos` / `*.rosinstall`), the workflow uses `ssh_key` and `known_hosts` to check out the dependency repositories under `.deps/`. Claude consults them read-only to verify cross-repo interfaces (message definitions, API signatures, parameter/topic names); they are never reviewed themselves.

#### Usage

1. Create a GitHub actions workflow file in your repository. e.g. `[repository_root]/.github/workflows/claude_pr_review.yml`
2. Just add `uses` as in the example file.

  Repository-specific context for the review (design policies, constraints, focus areas) should be written in the repository's `CLAUDE.md`, which Claude reads automatically.

  The example below triggers a review when the `sbgisen/claude` team is requested as a reviewer on the PR (the team needs read access to the repository to appear in the Reviewers list). To also review every new PR automatically, add `opened` to `types` and extend the `if` condition with `github.event.action == 'opened'`.

  :warning: Triggering on `synchronize` runs a review on every push to the PR, consuming a large number of tokens.

  :warning: Secrets are not passed to workflows triggered by pull requests from forks, so this workflow does not run for external contributors' PRs.

```yaml
name: Claude PR Review

on:
  pull_request:
    types: [review_requested]

permissions:
  contents: read
  issues: write
  pull-requests: write
  id-token: write

jobs:
  claude_pr_review:
    if: github.event.requested_team.slug == 'claude'
    name: Claude PR review
    uses: sbgisen/.github/.github/workflows/claude_pr_review.yml@main
    secrets:
      anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
      claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
      ssh_key: ${{ secrets.GISEN_ROBO_GIT }}
      known_hosts: ${{ secrets.KNOWN_HOSTS }}
```
