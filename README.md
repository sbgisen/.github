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
  Default is empty.

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
  Default is empty.

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
