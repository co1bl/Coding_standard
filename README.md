# Git Standards and Workflow Documentation

## Overview

This document establishes the Git standards, branching strategies, and development workflows for our engineering team. These guidelines ensure code quality, maintainability, and consistent collaboration practices across all projects.

**Compliance with these standards is mandatory for all team members.**

## Table of Contents

- [Prerequisites](#prerequisites)
- [Branching Strategy](#branching-strategy)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Commit Message Standards](#commit-message-standards)
- [Development Workflow](#development-workflow)
- [Repository Setup](#repository-setup)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Troubleshooting](#troubleshooting)
- [Enforcement and Review](#enforcement-and-review)

## Prerequisites

All developers must ensure the following requirements are met before contributing:

### Required Tools
- **Git**: Version 2.30+ installed and configured
- **GitHub Account**: With appropriate repository access
- **IDE/Editor**: Configured with Git integration

### Repository Requirements
- Remote repository must be created on GitHub
- Repository must have an initial commit (empty repositories cannot be pushed to)
- All team members must have appropriate branch protection rules configured

### Knowledge Requirements
- Understanding of Git fundamentals (branching, merging, rebasing)
- Familiarity with Conventional Commits specification
- Knowledge of pull request workflows

## Branching Strategy

We implement a **Git Flow-inspired** branching model with the following permanent and temporary branches:

### Permanent Branches

| Branch | Purpose | Stability | Deployment Target |
|--------|---------|-----------|-------------------|
| `main` | Production-ready code | Stable | Production environment |
| `tst` | Staging and testing | Semi-stable | Testing/Staging environment |
| `dev` | Integration and development | Unstable | Development environment |

### Temporary Branches

| Branch Type | Purpose | Created From | Merged Into | Lifespan |
|-------------|---------|--------------|-------------|----------|
| `feature/*` | New features and enhancements | `dev` | `dev` | Short-term |
| `bugfix/*` | Non-critical bug fixes | `dev` | `dev` | Short-term |
| `hotfix/*` | Critical production fixes | `main` | `main` + `dev` | Immediate |

### Branch Protection Rules

- **`main`**: Requires pull request reviews, status checks must pass
- **`tst`**: Requires pull request reviews
- **`dev`**: Pull request recommended, direct pushes allowed for authorized developers

## Branch Naming Conventions

All branch names must follow these conventions:

### Feature Branches
```
feature/<ticket-id>-<short-description>
feature/PROJ-123-user-authentication
feature/add-payment-gateway
```

### Bug Fix Branches
```
bugfix/<ticket-id>-<short-description>
bugfix/PROJ-456-fix-login-validation
bugfix/resolve-memory-leak
```

### Hotfix Branches
```
hotfix/<version>-<critical-issue>
hotfix/1.2.1-security-patch
hotfix/database-connection-fix
```

### Naming Rules
- Use **kebab-case** (lowercase with hyphens)
- Include ticket/issue ID when applicable
- Keep descriptions concise but descriptive
- Avoid special characters except hyphens
- Maximum length: 50 characters

## Commit Message Standards

We adhere to the [Conventional Commits](https://www.conventionalcommits.org/) specification for all commit messages.

### Format
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(api): add user registration endpoint` |
| `fix` | Bug fix | `fix(auth): resolve password validation issue` |
| `docs` | Documentation changes | `docs(readme): update installation instructions` |
| `style` | Code style changes (formatting, etc.) | `style(components): fix indentation and spacing` |
| `refactor` | Code refactoring | `refactor(utils): simplify date formatting logic` |
| `test` | Adding or modifying tests | `test(auth): add integration tests for login flow` |
| `chore` | Maintenance tasks | `chore(deps): update dependencies to latest versions` |
| `perf` | Performance improvements | `perf(api): optimize database queries` |
| `ci` | CI/CD changes | `ci(github): add automated testing workflow` |

### Commit Message Rules

1. **Use imperative mood**: "add feature" not "added feature"
2. **Start with lowercase**: Unless it's a proper noun
3. **No period at the end**: Keep it concise
4. **Limit first line to 72 characters**
5. **Use body for detailed explanations** when necessary
6. **Reference issues**: Include ticket numbers in footer

### Examples

```bash
# Simple feature commit
feat(api): add user profile update endpoint

# Bug fix with detailed explanation
fix(payment): resolve checkout validation error

The validation was failing for users with special characters
in their address fields. Updated regex pattern to handle
international addresses properly.

Fixes: #123
```

## Development Workflow

### 1. Feature Development

```bash
# Start from the latest dev branch
git checkout dev
git pull origin dev

# Create and switch to feature branch
git checkout -b feature/PROJ-123-user-dashboard

# Make your changes and commit
git add .
git commit -m "feat(dashboard): add user statistics widgets"

# Push branch and create pull request
git push -u origin feature/PROJ-123-user-dashboard
```

### 2. Bug Fix Process

```bash
# Create bugfix branch from dev
git checkout dev
git pull origin dev
git checkout -b bugfix/PROJ-456-fix-validation-error

# Implement fix and commit
git add .
git commit -m "fix(validation): resolve email format checking"

# Push and create pull request
git push -u origin bugfix/PROJ-456-fix-validation-error
```

### 3. Hotfix Process

```bash
# Create hotfix from main for urgent production fixes
git checkout main
git pull origin main
git checkout -b hotfix/1.2.1-critical-security-fix

# Implement critical fix
git add .
git commit -m "fix(security): patch authentication vulnerability"

# Push and create pull request to main
git push -u origin hotfix/1.2.1-critical-security-fix

# After merging to main, also merge to dev
git checkout dev
git merge hotfix/1.2.1-critical-security-fix
```

### 4. Release Process

```bash
# Merge dev to tst for testing
git checkout tst
git pull origin tst
git merge dev

# After testing approval, merge tst to main
git checkout main
git pull origin main
git merge tst

# Tag the release
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0
```

## Repository Setup

### Initial Repository Setup

```bash
# Initialize new repository
git init

# Add remote origin
git remote add origin https://github.com/organization/repository-name.git

# Create initial commit
git add .
git commit -m "chore: initialize repository with project structure"

# Set main as default branch
git branch -M main

# Push to remote
git push -u origin main

# Create and push dev branch
git checkout -b dev
git push -u origin dev

# Create and push tst branch
git checkout -b tst
git push -u origin tst
```

### Branch Protection Configuration

Configure the following branch protection rules in GitHub:

**Main Branch:**
- Require pull request reviews before merging
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Restrict pushes to main branch

**TST Branch:**
- Require pull request reviews before merging
- Require status checks to pass before merging

## Pull Request Guidelines

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)

## Related Issues
Fixes #(issue number)
```

### Review Requirements

- **Minimum Reviewers**: 2 for main, 1 for dev/tst
- **Required Checks**: All CI/CD pipelines must pass
- **Merge Strategy**: Squash and merge for feature branches

## Troubleshooting

### Common Issues and Solutions

#### Error: `src refspec main does not match any`

**Cause**: Attempting to push before making initial commit.

**Solution**:
```bash
git add .
git commit -m "chore: initialize repository"
git branch -M main
git push -u origin main
```

#### Error: `remote origin already exists`

**Cause**: Remote origin already configured.

**Solution**:
```bash
# Update existing remote
git remote set-url origin https://github.com/organization/new-repository.git

# Or remove and re-add
git remote rm origin
git remote add origin https://github.com/organization/repository.git
```

#### Error: `Updates were rejected because the remote contains work`

**Cause**: Remote branch has commits not in local branch.

**Solution**:
```bash
# Pull and merge remote changes
git pull origin main --rebase

# Or force push (use with caution)
git push --force-with-lease origin main
```

## Enforcement and Review

### Code Review Standards

- All pull requests must be reviewed by at least one team member
- Reviewers must verify adherence to these standards
- Non-compliant commits may be rejected

### Automated Checks

- Commit message format validation
- Branch naming convention checks
- Code style and linting verification
- Test coverage requirements

### Violations and Remediation

- **Minor violations**: Request changes in pull request review
- **Major violations**: Reject pull request until standards are met
- **Repeated violations**: Escalate to team lead for additional training

## Contact and Support

For questions about these standards or Git-related issues:

- **Primary Contact**: [Team Lead Name]
- **Documentation**: [Internal Wiki/Confluence Link]
- **Training Resources**: [Training Material Links]

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Next Review**: [Review Date]
