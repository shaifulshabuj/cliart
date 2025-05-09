# CLIArt

A powerful command-line tool for visualizing code structures, file directories, and code relationships as diagrams. CLIArt helps developers understand complex codebases by generating visual representations of code dependencies and structure.

## Features

- **Directory Structure Visualization**: Generate clear ASCII diagrams of file directory structures
- **Code Structure Analysis**: Visualize classes, functions, and their relationships within files
- **Dependency Mapping**: See which files import from which others across your codebase
- **Relation Diagrams**: Generate comprehensive diagrams showing dependencies between files and symbols
- **Function Call Graphs**: Visualize which functions call other functions across your codebase
- **Multi-Language Support**: Works with dozens of programming languages and project types
- **Project File Analysis**: Extracts dependencies from package managers and project files
- **Large Project Handling**: Efficiently processes large codebases with smart filtering

## Supported Languages & Technologies

### Programming Languages

#### Web Development
- JavaScript/TypeScript (including React, Vue, Svelte, Angular)
- HTML, CSS, SCSS, LESS
- PHP

#### Systems Programming
- C/C++
- Rust
- Go
- Zig

#### .NET Ecosystem
- C#
- F#
- VB.NET

#### JVM Languages
- Java
- Kotlin
- Scala
- Clojure
- Groovy

#### Scripting Languages
- Python
- Ruby
- Perl
- Shell scripts
- PowerShell
- Lua

#### Mobile Development
- Swift
- Objective-C
- Dart/Flutter

### Project Types

- **Web**: npm, yarn, webpack, rollup
- **Python**: pip, poetry, pipenv
- **.NET**: NuGet, MSBuild
- **JVM**: Maven, Gradle, SBT
- **Mobile**: CocoaPods, Gradle
- **DevOps**: Docker, Terraform, Kubernetes
- **CI/CD**: GitHub Actions, GitLab CI, Travis CI

## Installation

No external dependencies required! Just clone the repository and run the script:

```bash
git clone https://github.com/yourusername/cliart.git
cd cliart
```

## Usage

### Directory Structure Visualization

Generate an ASCII diagram of a directory structure:

```bash
python cliart.py directory --path /path/to/directory --output diagram.txt --max-depth 3
```

### Code Structure Visualization

Analyze and visualize the structure of code files (classes, functions, etc.):

```bash
python cliart.py code --path /path/to/file.py --output code_diagram.txt
```

You can also analyze an entire directory of code files:

```bash
python cliart.py code --path /path/to/src --output code_diagram.txt
```

### Code Relation Diagram

Generate a comprehensive diagram showing relationships between files, dependencies, and function calls:

```bash
python cliart.py relation --path /path/to/project --output relation_diagram.txt --depth 2
```

The `--depth` parameter controls the level of detail:
- `1`: Basic file dependencies
- `2`: File dependencies + symbol usage across files
- `3`: All of the above + function call graph

#### Examples

**Analyzing a Python project:**
```bash
python cliart.py relation --path /path/to/python_project --output python_relation.txt --depth 3
```

**Analyzing a JavaScript/TypeScript project:**
```bash
python cliart.py relation --path /path/to/js_project --output js_relation.txt --depth 3
```

**Analyzing a C# project:**
```bash
python cliart.py relation --path /path/to/csharp_project --output csharp_relation.txt --depth 3
```

**Analyzing a large project (with optimized performance):**
```bash
python cliart.py relation --path /path/to/large_project --output large_project_relation.txt --depth 2
```

## Command Options

### Directory Command

- `--path`: Path to the directory to visualize
- `--output`: Output file path (default: directory_diagram.txt)
- `--max-depth`: Maximum directory depth to visualize (default: unlimited)

### Code Command

- `--path`: Path to the code file or directory to analyze
- `--output`: Output file path (default: code_diagram.txt)
- `--language`: Programming language (auto-detected if not specified)

### Relation Command

- `--path`: Path to the project directory or file to analyze
- `--output`: Output file path (default: relation_diagram.txt)
- `--depth`: Level of detail (1-3, default: 1)

## Example Output

### Directory Structure

```
Directory Structure for: my_project
--------------------------------------------------
my_project/
├── src/
│   ├── components/
│   │   ├── Button.js
│   │   └── Header.js
│   ├── utils/
│   │   └── helpers.js
│   └── App.js
├── public/
│   ├── index.html
│   └── styles.css
└── package.json
```

### Code Relation Diagram

```
Code Relation Diagram for: my_project
============================================================

File Dependencies:

src/App.js
  └── imports from:
      └── ./components/Header (local)
      └── ./components/Button (local)
      └── ./utils/helpers (local)
      └── react (external)

src/components/Button.js
  └── imports from:
      └── react (external)
      └── ../utils/helpers (local)

src/components/Header.js
  └── imports from:
      └── react (external)
      └── ./Button (local)

src/utils/helpers.js
  └── imports from:
      └── react (external)


Symbol Usage Across Files:

src/components/Button.js defines:
  └── Button
      └── used by:
          └── src/App.js
          └── src/components/Header.js

src/utils/helpers.js defines:
  └── formatText
      └── used by:
          └── src/App.js
          └── src/components/Button.js


Function Call Graph:

App (in src/App.js)
  └── calls Button (in src/components/Button.js)
  └── calls Header (in src/components/Header.js)
  └── calls formatText (in src/utils/helpers.js)

Button (in src/components/Button.js)
  └── calls formatText (in src/utils/helpers.js)
```

## Performance Tips

- **Large Projects**: For very large projects, use `--depth 1` or `--depth 2` instead of `--depth 3` to improve performance
- **Excluded Directories**: CLIArt automatically excludes common directories like `node_modules`, `.git`, `venv`, etc.
- **File Size Limits**: Files larger than 1MB are automatically skipped to prevent memory issues

## Limitations

- CLIArt uses regex-based parsing, which may not be as accurate as a full AST parser for complex code analysis
- Some language features may not be fully supported, especially for less common languages
- Very large projects (10,000+ files) may take a long time to process

## Contributing

Contributions are welcome! Here are some ways you can contribute:

- Add support for additional programming languages
- Improve parsing accuracy for existing languages
- Enhance visualization formats
- Add new features or commands
- Fix bugs and improve performance

## License

MIT License
