# Changelog Messages

This directory contains changelog messages.

# Adding a new changelog message

Create a file in this directory named in the following format:

{issuenum}.{changetype}.md

issuenum - Is the issue number for the change.

changetype - Is the type of change, it can be one of the following:

- feature - A new feature
- bugfix - The change fixes a bug
- doc - The change is an improvement to the documentation
- removal - The changed involved removing code or features
- misc - Other kinds of changes

The changes are automatically added to the changelog of the release that contains
the new change file.
