# Repository Baseline

Every repository in the Microsoft Architecture practice must ship these baseline files. They eliminate tab-vs-space debates, enforce deterministic line endings, and make CI logs readable across Windows, macOS, and Linux contributors.

---

## Conventional Commits

All commit messages MUST follow the [Conventional Commits 1.0.0](https://www.conventionalcommits.org/) specification.

### Format

```text
<type>(<scope>): <short description>

[optional body]

[optional footer(s)]
```

### Types

| Type | When to use |
|---|---|
| `feat` | A new user-facing feature |
| `fix` | A bug fix |
| `chore` | Maintenance, dependency bumps, tooling (no production code change) |
| `docs` | Documentation changes only |
| `refactor` | Code restructuring with no behavior change |
| `test` | Adding or updating tests |
| `build` | Changes to build system or external dependencies (MSBuild, NuGet, npm) |
| `ci` | Changes to CI/CD pipeline configuration |
| `perf` | Performance improvement |
| `style` | Formatting, whitespace (no logic change) |

### Scope

Use the component or layer name: `feat(orders-api)`, `fix(auth-middleware)`, `ci(github-actions)`. Omit scope only for truly cross-cutting changes.

### Breaking Changes

Append `!` after the type/scope: `feat(payments-api)!: remove legacy charge endpoint`

Always add a `BREAKING CHANGE:` footer with migration instructions.

### Examples

```text
feat(order-service): add idempotency key support to PlaceOrder endpoint

Callers can now pass X-Idempotency-Key header to safely retry order placement
without creating duplicate orders. Key is stored in Redis with 24h TTL.

Closes #142
```

```text
fix(ef-migrations): correct nullable column on CustomerAddress

Addresses data loss when updating address with null Region field.

Fixes #201
```

---

## .editorconfig

Place at repository root. IDEs and most formatters respect this file automatically.

```editorconfig
# EditorConfig baseline: Contoso / Microsoft Architecture practice
# https://editorconfig.org
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

# C#: 4-space indentation per .NET conventions
[*.{cs,csx}]
indent_style = space
indent_size = 4
max_line_length = 120

# F#
[*.{fs,fsx,fsi}]
indent_style = space
indent_size = 4

# JSON: 2-space indentation (matches VS Code defaults)
[*.json]
indent_style = space
indent_size = 2

# YAML: 2-space indentation (YAML spec best practice)
[*.{yml,yaml}]
indent_style = space
indent_size = 2

# Markdown: preserve trailing spaces (line breaks in MD)
[*.md]
indent_style = space
indent_size = 2
trim_trailing_whitespace = false

# XML / project files
[*.{xml,csproj,props,targets,config}]
indent_style = space
indent_size = 2

# Bicep / ARM
[*.{bicep,json}]
indent_style = space
indent_size = 2

# Shell scripts: keep 2-space for readability
[*.{sh,bash,zsh}]
indent_style = space
indent_size = 2

# Makefiles require tabs
[Makefile]
indent_style = tab
```

**Note on `end_of_line = lf`**: Windows contributors using Git must configure `core.autocrlf = false` or `core.autocrlf = input`. The `.gitattributes` file below enforces this at the Git level.

---

## .gitattributes

```gitattributes
# Force LF line endings in the repository for all text files.
# Overrides per-user Git config. Source of truth is the repo.
* text=auto eol=lf

# Explicitly mark binary files so Git never tries to merge or diff them as text.
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.pdf binary
*.zip binary
*.tar.gz binary
*.tgz binary
*.nupkg binary
*.snupkg binary
*.dll binary
*.exe binary
*.pdb binary
*.woff binary
*.woff2 binary
*.ttf binary
*.eot binary

# Lock files: no merge, keep ours on conflict
package-lock.json merge=ours
yarn.lock merge=ours

# Linguist: mark generated files so they don't inflate language stats
*.generated.cs linguist-generated=true
*.Designer.cs linguist-generated=true
**/Migrations/*.cs linguist-generated=true
wwwroot/lib/** linguist-vendored=true
```

---

## .gitignore

Covers .NET, Node.js, and Python in a single monorepo-friendly file. Add project-specific entries below the separator.

```gitignore
##########
# .NET / C#
##########
[Bb]in/
[Oo]bj/
[Ll]og/
[Ll]ogs/
*.user
*.suo
*.userosscache
*.sln.docstates
.vs/
.vscode/settings.json
TestResults/
[Rr]elease/
[Dd]ebug/
x64/
x86/
[Ww][Ii][Nn]32/
[Aa][Rr][Mm]/
[Aa][Rr][Mm]64/
bld/
msbuild.log
msbuild.err
msbuild.wrn
*.nupkg
*.snupkg
.nuget/
packages/
*.trx

# ASP.NET Core
wwwroot/dist/

# Entity Framework
*.ef.migrations.log

##########
# Node.js
##########
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.yarn/cache
.yarn/unplugged
.pnp.*
dist/
.next/
.nuxt/
.output/
.cache/
.parcel-cache/

##########
# Python
##########
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/
ENV/
*.egg-info/
dist/
build/
.eggs/
.pytest_cache/
.mypy_cache/
.ruff_cache/
*.pyc

##########
# Secrets / sensitive: NEVER commit these
##########
*.env
.env.*
!.env.example
appsettings.*.json
!appsettings.Development.json
local.settings.json
secrets.json
*.pem
*.key
*.pfx
*.p12
*.cer

##########
# OS / Editor
##########
.DS_Store
.DS_Store?
._*
Thumbs.db
ehthumbs.db
Desktop.ini
*.swp
*.swo
*~
.idea/
*.iml

##########
# CI / Infrastructure artifacts
##########
terraform.tfstate
terraform.tfstate.backup
.terraform/
*.tfplan
crash.log
override.tf
override.tf.json
*_override.tf
*_override.tf.json
```

---

## Trade-offs and Exceptions

- **`trim_trailing_whitespace = false` for Markdown**: Two trailing spaces create a `<br>` in CommonMark. If your team never uses trailing-space line breaks and uses blank lines instead, set `trim_trailing_whitespace = true` for `*.md` too.
- **`end_of_line = lf` on Windows-only teams**: If every contributor and CI runner is Windows and downstream tooling requires CRLF, keep `eol=crlf` in `.gitattributes` for `.cs` and `.csproj`. Document the decision in the repo README.
- **Conventional Commits enforcement**: Add `commitlint` to a Git `commit-msg` hook or a CI check. Without enforcement, the convention erodes within weeks. `cz-conventional-changelog` provides an interactive commit wizard.
- **`packages/` in `.gitignore`**: Modern .NET projects use `<PackageReference>` and restore via NuGet, so the packages directory should not be committed. If you use `packages.config` (legacy), remove this line and commit the packages folder.
- **Bicep alongside ARM JSON**: If your team generates ARM JSON from Bicep, add `*.json` under `linguist-generated=true` in `.gitattributes` for the output path to avoid polluting language statistics.
