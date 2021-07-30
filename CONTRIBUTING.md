# How can I contribute?

Thank you for taking your time to view and possibly contribute to SImple-Matrix-Bot-Lib!

### Reporting Bugs

To report a bug in Simple-Matrix-Bot-Lib, select the bug report template from [here](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/issues/new/choose) and replace the default and blank values with the appropriate information. You can also join Simple-Matrix-Bot-Lib's Matrix room located at [#simplematrixbotlib:matrix.org](https://matrix.to/#/#simplematrixbotlib:matrix.org) to discuss your problem with members.

### Suggesting Features

To suggest a feature for Simple-Matrix-Bot-Lib, select the feature request template from [here](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/issues/new/choose) and add clear and precise details concerning your suggestion.

### Improving the Source Code

If you want to contribute to Simple-Matrix-Bot-Lib, the most direct method is to improve the source code. 

# How do I improve the Source Code?

This project follows a variation of the Github Flow workflow. You may find the information located [here](https://guides.github.com/introduction/flow/) to be useful.

### Ask First

Before you begin, please discuss your planned improvements with a maintainer in our [Matrix Room](https://matrix.to/#/#simplematrixbotlib:matrix.org). This is to make sure that your changes are aligned with the goals of this project, which can help you avoid wasting your time and effort.

### Fork the Repository

Fork the repository by clicking on the "Fork" button.

### Create a Feature Branch

Create a branch specifically for your feature with a descriptive name. Over the course of your development, commit your changes to this branch.

### Keep your Branch up-to-date

While you develop, other branches such as the master branch may receive commits. To make sure that your branch has the latest changes, it is recommended that you rebase your master branch (master) onto the upstream master branch (upstream/master), the rebase your feature branch (example-branch) on your master branch. If you decide to push your changes, it may be necessary to use the --force flag. The process may resemble the following:

```bash
# Commit to your feature branch
git commit -m "example commit"
# Add upstream repository remote
git remote add upstream https://github.com/KrazyKirby99999/simple-matrix-bot-lib.git
# Update your master branch with upstream changes
git fetch && git checkout master
git rebase upstream/master
git push origin master --force
# Update your feature branch with upstream changes
git checkout feature-branch
git rebase master
git push origin feature-branch --force
```

### Create a pull request

When you consider your feature to be ready to merge, create a pull request on [Github](https://github.com/KrazyKirby99999/simple-matrix-bot-lib/compare). Make sure to link to any relevant issues, and provide a description for each commit. If your pull request is considered incomplete, you may be requested to make changes to your feature branch.

### 