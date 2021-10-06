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
- XML (launch files, package.xml)
  - Format (xmllint)
  - Lint (xmllint)

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
