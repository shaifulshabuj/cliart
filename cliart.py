#!/usr/bin/env python3
"""
CLIArt - A command-line tool for visualizing code structures and file directories as diagrams.
"""

import os
import sys
import re
import argparse
import json
from collections import defaultdict
from parse_dotnet import parse_dotnet_project_file
from project_parsers import parse_project_file

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='CLIArt - Generate diagrams from code and directories')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Directory command
    dir_parser = subparsers.add_parser('directory', help='Generate a directory structure diagram')
    dir_parser.add_argument('--path', required=True, help='Path to the directory to visualize')
    dir_parser.add_argument('--output', default='directory_diagram.txt', help='Output file path')
    dir_parser.add_argument('--format', default='ascii', choices=['ascii'], help='Output format')
    dir_parser.add_argument('--max-depth', type=int, help='Maximum directory depth to visualize')
    
    # Code command
    code_parser = subparsers.add_parser('code', help='Generate a source code relationship diagram')
    code_parser.add_argument('--path', required=True, help='Path to the source code to visualize')
    code_parser.add_argument('--output', default='code_diagram.txt', help='Output file path')
    code_parser.add_argument('--format', default='ascii', choices=['ascii'], help='Output format')
    code_parser.add_argument('--language', help='Programming language (auto-detect if not specified)')
    
    # Relation command
    relation_parser = subparsers.add_parser('relation', help='Generate a code relation diagram showing dependencies')
    relation_parser.add_argument('--path', required=True, help='Path to the source code or directory to analyze')
    relation_parser.add_argument('--output', default='relation_diagram.txt', help='Output file path')
    relation_parser.add_argument('--format', default='ascii', choices=['ascii'], help='Output format')
    relation_parser.add_argument('--depth', type=int, default=1, help='Depth of relation analysis (1-3, higher values analyze deeper relationships)')
    
    return parser.parse_args()

def directory_command(args):
    """Generate a directory structure diagram."""
    print(f"Generating directory diagram for {args.path}")
    
    if not os.path.exists(args.path):
        print(f"Error: Path {args.path} does not exist")
        sys.exit(1)
    
    try:
        diagram = create_directory_diagram(args.path, args.max_depth)
        with open(args.output, 'w') as f:
            f.write(diagram)
        print(f"Success: Diagram saved to {args.output}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def code_command(args):
    """Generate a source code relationship diagram."""
    print(f"Generating code diagram for {args.path}")
    
    if not os.path.exists(args.path):
        print(f"Error: Path {args.path} does not exist")
        sys.exit(1)
    
    try:
        diagram = create_code_diagram(args.path, args.language)
        with open(args.output, 'w') as f:
            f.write(diagram)
        print(f"Success: Diagram saved to {args.output}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def create_directory_diagram(path, max_depth=None):
    """Create an ASCII diagram representing the directory structure."""
    result = []
    root_name = os.path.basename(os.path.abspath(path))
    result.append(root_name)
    
    _process_directory_for_ascii(result, path, "", 0, max_depth)
    
    return "\n".join(result)

def _process_directory_for_ascii(result, path, prefix, current_depth, max_depth):
    """Process a directory and add its contents to the ASCII diagram."""
    if max_depth is not None and current_depth >= max_depth:
        return
    
    items = sorted(os.listdir(path))
    for i, item in enumerate(items):
        item_path = os.path.join(path, item)
        is_last = i == len(items) - 1
        
        # Choose the appropriate connector
        connector = "└── " if is_last else "├── "
        result.append(f"{prefix}{connector}{item}")
        
        if os.path.isdir(item_path):
            # Process subdirectory with updated prefix
            new_prefix = prefix + ("    " if is_last else "│   ")
            _process_directory_for_ascii(result, item_path, new_prefix, current_depth + 1, max_depth)

def create_code_diagram(path, language=None):
    """Create an ASCII diagram representing code relationships."""
    result = []
    
    if os.path.isdir(path):
        # Process directory of code files
        result.append(f"Code Diagram for Directory: {os.path.basename(path)}")
        result.append("=" * 50)
        
        # Process all code files in the directory
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                # Skip non-code files
                if file_ext not in ['.py', '.js', '.java', '.cpp', '.c', '.rb', '.go']:
                    continue
                    
                # Detect language from extension if not specified
                file_language = language or detect_language_from_extension(file_ext)
                
                # Process the file
                rel_path = os.path.relpath(file_path, path)
                result.append(f"\nFile: {rel_path} ({file_language})")
                result.append("-" * 50)
                
                file_structure = extract_code_structure(file_path, file_language)
                result.extend(file_structure)
    else:
        # Process single code file
        file_ext = os.path.splitext(path)[1].lower()
        file_language = language or detect_language_from_extension(file_ext)
        
        result.append(f"Code Diagram for File: {os.path.basename(path)}")
        result.append("=" * 50)
        
        file_structure = extract_code_structure(path, file_language)
        result.extend(file_structure)
    
    return "\n".join(result)

def detect_language_from_extension(ext):
    """Detect programming language from file extension."""
    languages = {
        # Web Development
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.less': 'less',
        '.php': 'php',
        '.vue': 'vue',
        '.svelte': 'svelte',
        '.astro': 'astro',
        '.cshtml': 'razor',
        '.razor': 'razor',
        '.jsp': 'jsp',
        '.aspx': 'aspx',
        
        # Mobile Development
        '.java': 'java',
        '.kt': 'kotlin',
        '.kts': 'kotlin',
        '.swift': 'swift',
        '.m': 'objective-c',
        '.h': 'objective-c',
        '.dart': 'dart',
        '.gradle': 'gradle',
        '.plist': 'plist',
        '.xcodeproj': 'xcode',
        
        # Systems Programming
        '.c': 'c',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.hpp': 'cpp',
        '.rs': 'rust',
        '.go': 'go',
        '.zig': 'zig',
        '.d': 'd',
        '.nim': 'nim',
        '.nims': 'nim',
        
        # .NET Ecosystem
        '.cs': 'csharp',
        '.fs': 'fsharp',
        '.fsx': 'fsharp',
        '.vb': 'vb',
        '.csproj': 'csproj',
        '.fsproj': 'fsproj',
        '.vbproj': 'vbproj',
        '.sln': 'sln',
        '.xaml': 'xaml',
        '.cshtml': 'cshtml',
        '.cake': 'cake',
        '.props': 'msbuild',
        '.targets': 'msbuild',
        
        # JVM Languages
        '.java': 'java',
        '.scala': 'scala',
        '.kt': 'kotlin',
        '.kts': 'kotlin',
        '.groovy': 'groovy',
        '.gradle': 'gradle',
        '.clj': 'clojure',
        '.cljs': 'clojure',
        '.cljc': 'clojure',
        
        # Scripting Languages
        '.rb': 'ruby',
        '.erb': 'erb',
        '.rake': 'ruby',
        '.pl': 'perl',
        '.pm': 'perl',
        '.t': 'perl',
        '.sh': 'shell',
        '.bash': 'shell',
        '.zsh': 'shell',
        '.fish': 'fish',
        '.ps1': 'powershell',
        '.psm1': 'powershell',
        '.lua': 'lua',
        '.tcl': 'tcl',
        
        # Functional Languages
        '.hs': 'haskell',
        '.lhs': 'haskell',
        '.elm': 'elm',
        '.ml': 'ocaml',
        '.mli': 'ocaml',
        '.ex': 'elixir',
        '.exs': 'elixir',
        '.erl': 'erlang',
        '.hrl': 'erlang',
        '.rkt': 'racket',
        '.scm': 'scheme',
        
        # Data Science & ML
        '.r': 'r',
        '.rmd': 'rmarkdown',
        '.jl': 'julia',
        '.ipynb': 'jupyter',
        '.mat': 'matlab',
        '.m': 'matlab',
        '.stan': 'stan',
        
        # Configuration & Data
        '.json': 'json',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.conf': 'conf',
        '.properties': 'properties',
        '.env': 'env',
        '.sql': 'sql',
        '.graphql': 'graphql',
        '.proto': 'protobuf',
        '.avsc': 'avro',
        '.thrift': 'thrift',
        
        # Documentation
        '.md': 'markdown',
        '.rst': 'restructuredtext',
        '.tex': 'latex',
        '.adoc': 'asciidoc',
        '.wiki': 'wiki',
        
        # Hardware & Low-level
        '.v': 'verilog',
        '.sv': 'systemverilog',
        '.vhd': 'vhdl',
        '.vhdl': 'vhdl',
        '.f': 'fortran',
        '.for': 'fortran',
        '.f90': 'fortran',
        '.f95': 'fortran',
        '.f03': 'fortran',
        '.f08': 'fortran',
        '.s': 'assembly',
        '.asm': 'assembly',
        
        # Project Files
        '.csproj': 'csproj',
        '.fsproj': 'fsproj',
        '.vbproj': 'vbproj',
        '.vcxproj': 'vcxproj',
        '.proj': 'msbuild',
        '.pbxproj': 'xcode',
        '.xcodeproj': 'xcode',
        '.xcworkspace': 'xcode',
        '.pro': 'qmake',
        '.pri': 'qmake',
        '.cmake': 'cmake',
        '.make': 'make',
        '.mk': 'make',
        '.bazel': 'bazel',
        '.bzl': 'bazel',
        'BUILD': 'bazel',
        'WORKSPACE': 'bazel',
        'Makefile': 'make',
        'CMakeLists.txt': 'cmake',
        'package.json': 'npm',
        'Cargo.toml': 'cargo',
        'Gemfile': 'bundler',
        'Pipfile': 'pipenv',
        'pyproject.toml': 'python-project',
        'setup.py': 'setuptools',
        'pom.xml': 'maven',
        'build.gradle': 'gradle',
        'build.sbt': 'sbt',
        'mix.exs': 'mix',
        'rebar.config': 'rebar',
        'composer.json': 'composer',
        'go.mod': 'go-modules',
        'Dockerfile': 'docker',
        'docker-compose.yml': 'docker-compose',
        'Jenkinsfile': 'jenkins',
        '.gitlab-ci.yml': 'gitlab-ci',
        '.travis.yml': 'travis-ci',
        'appveyor.yml': 'appveyor',
        'azure-pipelines.yml': 'azure-pipelines',
        'cloudbuild.yaml': 'cloud-build',
        'serverless.yml': 'serverless',
        'terraform.tf': 'terraform',
        '.tf': 'terraform',
        '.tfvars': 'terraform',
        '.hcl': 'hcl',
        'Chart.yaml': 'helm',
        'kustomization.yaml': 'kustomize',
        'Vagrantfile': 'vagrant',
        'Brewfile': 'homebrew'
    }
    return languages.get(ext.lower(), 'unknown')

def extract_code_structure(file_path, language):
    """Extract code structure from a file based on language."""
    result = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if language == 'python':
            # Extract Python code structure
            classes = {}
            standalone_functions = []
            
            # Find classes
            class_pattern = r'class\s+(\w+)(?:\(([^)]+)\))?\s*:'
            class_matches = re.finditer(class_pattern, content)
            
            for match in class_matches:
                class_name = match.group(1)
                parent_class = match.group(2) if match.group(2) else None
                classes[class_name] = {'parent': parent_class, 'methods': []}
            
            # Find methods and functions
            func_pattern = r'def\s+(\w+)\s*\(([^)]*)\)\s*:'
            func_matches = re.finditer(func_pattern, content)
            
            for match in func_matches:
                func_name = match.group(1)
                func_params = match.group(2)
                
                # Check if this is a method (indented inside a class)
                is_method = False
                for class_name in classes:
                    if re.search(rf'class\s+{class_name}.*?\n\s+def\s+{func_name}\s*\(', content, re.DOTALL):
                        classes[class_name]['methods'].append((func_name, func_params))
                        is_method = True
                        break
                
                if not is_method:
                    standalone_functions.append((func_name, func_params))
            
            # Format the output
            for class_name, class_info in classes.items():
                parent_str = f" extends {class_info['parent']}" if class_info['parent'] else ""
                result.append(f"\nClass: {class_name}{parent_str}")
                
                if class_info['methods']:
                    for method_name, method_params in class_info['methods']:
                        result.append(f"  └── Method: {method_name}({method_params})")
            
            if standalone_functions:
                result.append("\nFunctions:")
                for func_name, func_params in standalone_functions:
                    result.append(f"  └── {func_name}({func_params})")
        
        elif language in ['javascript', 'js', 'typescript', 'ts']:
            # JavaScript/TypeScript parsing
            classes = []
            functions = []
            interfaces = []
            variables = []
            imports = []
            
            # Find imports (ES6 style)
            import_patterns = [
                r'import\s+{([^}]*)}\s+from\s+[\"\'](.*?)[\"\'](;)?',  # Named imports
                r'import\s+(\w+)\s+from\s+[\"\'](.*?)[\"\'](;)?',  # Default import
                r'import\s+\*\s+as\s+(\w+)\s+from\s+[\"\'](.*?)[\"\'](;)?'  # Namespace import
            ]
            
            for pattern in import_patterns:
                for match in re.finditer(pattern, content):
                    if pattern == import_patterns[0]:  # Named imports
                        imports.append(f"Import: {{{match.group(1)}}} from '{match.group(2)}'")
                    else:  # Default or namespace import
                        imports.append(f"Import: {match.group(1)} from '{match.group(2)}'")
            
            # Find classes (ES6 style)
            class_pattern = r'(?:export\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w,\s]+))?\s*{'
            class_matches = re.finditer(class_pattern, content)
            
            for match in class_matches:
                class_name = match.group(1)
                parent_class = match.group(2) if match.group(2) else None
                implements = match.group(3) if match.group(3) else None
                
                class_info = f"Class: {class_name}"
                if parent_class:
                    class_info += f" extends {parent_class}"
                if implements:
                    class_info += f" implements {implements}"
                    
                classes.append(class_info)
            
            # Find interfaces (TypeScript)
            if language in ['typescript', 'ts']:
                interface_pattern = r'(?:export\s+)?interface\s+(\w+)(?:\s+extends\s+([\w,\s]+))?\s*{'
                interface_matches = re.finditer(interface_pattern, content)
                
                for match in interface_matches:
                    interface_name = match.group(1)
                    extends = match.group(2) if match.group(2) else None
                    
                    interface_info = f"Interface: {interface_name}"
                    if extends:
                        interface_info += f" extends {extends}"
                        
                    interfaces.append(interface_info)
            
            # Find functions (various styles)
            func_patterns = [
                r'(?:export\s+)?function\s+(\w+)\s*\(([^)]*)\)',  # Regular functions
                r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*function\s*\(([^)]*)\)',  # Function expressions
                r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*\(([^)]*)\)\s*=>',  # Arrow functions
                r'(?:public|private|protected)?\s*(?:static)?\s*(\w+)\s*\(([^)]*)\)\s*{',  # Class methods
                r'(?:public|private|protected)?\s*(?:static)?\s*(\w+)\s*\(([^)]*)\)\s*:.*?{',  # TypeScript methods with return type
                r'(?:export\s+)?(?:async\s+)?function\s*\*\s*(\w+)\s*\(([^)]*)\)'  # Generator functions
            ]
            
            for pattern in func_patterns:
                for match in re.finditer(pattern, content):
                    func_name = match.group(1)
                    func_params = match.group(2)
                    
                    # Skip if this is likely a class method (already captured in class)
                    if pattern in [func_patterns[3], func_patterns[4]]:
                        # Check if this is a class method
                        class_method = False
                        for class_match in re.finditer(r'class\s+(\w+)', content):
                            class_name = class_match.group(1)
                            if re.search(rf'class\s+{class_name}.*?{func_name}\s*\(', content, re.DOTALL):
                                class_method = True
                                break
                        if class_method:
                            continue
                        
                    functions.append(f"Function: {func_name}({func_params})")
            
            # Find top-level variables
            var_pattern = r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?!function|\(.*\)\s*=>)'
            for match in re.finditer(var_pattern, content):
                var_name = match.group(1)
                variables.append(f"Variable: {var_name}")
            
            # Format the output
            if imports:
                result.append("\nImports:")
                for imp in imports[:5]:  # Limit to first 5 imports to avoid clutter
                    result.append(f"  └── {imp}")
                if len(imports) > 5:
                    result.append(f"  └── ... and {len(imports) - 5} more imports")
            
            if interfaces:
                result.append("\nInterfaces:")
                for interface in interfaces:
                    result.append(f"  └── {interface}")
            
            if classes:
                result.append("\nClasses:")
                for cls in classes:
                    result.append(f"  └── {cls}")
            
            if functions:
                result.append("\nFunctions:")
                for func in functions:
                    result.append(f"  └── {func}")
            
            if variables:
                result.append("\nTop-level Variables:")
                for var in variables[:10]:  # Limit to first 10 variables
                    result.append(f"  └── {var}")
                if len(variables) > 10:
                    result.append(f"  └── ... and {len(variables) - 10} more variables")
        
        elif language in ['rust', 'rs']:
            # Rust parsing
            structs = []
            enums = []
            traits = []
            impls = []
            functions = []
            
            # Find structs
            struct_pattern = r'(?:pub\s+)?struct\s+(\w+)(?:<[^>]*>)?\s*(?:\{|;)'
            struct_matches = re.finditer(struct_pattern, content)
            for match in struct_matches:
                struct_name = match.group(1)
                structs.append(f"Struct: {struct_name}")
            
            # Find enums
            enum_pattern = r'(?:pub\s+)?enum\s+(\w+)(?:<[^>]*>)?\s*\{'
            enum_matches = re.finditer(enum_pattern, content)
            for match in enum_matches:
                enum_name = match.group(1)
                enums.append(f"Enum: {enum_name}")
            
            # Find traits
            trait_pattern = r'(?:pub\s+)?trait\s+(\w+)(?:<[^>]*>)?(?:\s*:\s*([^{]*))?\s*\{'
            trait_matches = re.finditer(trait_pattern, content)
            for match in trait_matches:
                trait_name = match.group(1)
                trait_bounds = match.group(2).strip() if match.group(2) else None
                trait_info = f"Trait: {trait_name}"
                if trait_bounds:
                    trait_info += f" : {trait_bounds}"
                traits.append(trait_info)
            
            # Find implementations
            impl_pattern = r'impl(?:<[^>]*>)?\s+(?:([^\s{]+)\s+for\s+)?([^\s{<]+)(?:<[^>]*>)?\s*\{'
            impl_matches = re.finditer(impl_pattern, content)
            for match in re.finditer(impl_pattern, content):
                trait_name = match.group(1) if match.group(1) else None
                type_name = match.group(2)
                if trait_name:
                    impls.append(f"Impl: {trait_name} for {type_name}")
                else:
                    impls.append(f"Impl: {type_name}")
            
            # Find functions
            func_pattern = r'(?:pub(?:\([^)]*\))?\s+)?(?:async\s+)?fn\s+(\w+)(?:<[^>]*>)?\s*\(([^)]*)\)'
            func_matches = re.finditer(func_pattern, content)
            for match in func_matches:
                func_name = match.group(1)
                func_params = match.group(2)
                functions.append(f"Function: {func_name}({func_params})")
            
            # Format the output
            if structs:
                result.append("\nStructs:")
                for struct in structs:
                    result.append(f"  └── {struct}")
            
            if enums:
                result.append("\nEnums:")
                for enum in enums:
                    result.append(f"  └── {enum}")
            
            if traits:
                result.append("\nTraits:")
                for trait in traits:
                    result.append(f"  └── {trait}")
            
            if impls:
                result.append("\nImplementations:")
                for impl in impls:
                    result.append(f"  └── {impl}")
            
            if functions:
                result.append("\nFunctions:")
                for func in functions:
                    result.append(f"  └── {func}")
                    
        elif language in ['cpp', 'c++', 'c']:
            # C/C++ parsing
            classes = []
            structs = []
            functions = []
            namespaces = []
            
            # Find namespaces (C++ only)
            if language in ['cpp', 'c++']:
                namespace_pattern = r'namespace\s+(\w+)\s*\{'
                for match in re.finditer(namespace_pattern, content):
                    namespace_name = match.group(1)
                    namespaces.append(f"Namespace: {namespace_name}")
            
            # Find classes (C++ only)
            if language in ['cpp', 'c++']:
                class_pattern = r'(?:class|struct)\s+(\w+)(?:\s*:\s*(?:public|protected|private)\s+([^{]*))?\s*\{'
                for match in re.finditer(class_pattern, content):
                    class_name = match.group(1)
                    inheritance = match.group(2).strip() if match.group(2) else None
                    class_info = f"Class: {class_name}"
                    if inheritance:
                        class_info += f" : {inheritance}"
                    classes.append(class_info)
            
            # Find structs (C)
            struct_pattern = r'struct\s+(\w+)\s*\{'
            for match in re.finditer(struct_pattern, content):
                struct_name = match.group(1)
                structs.append(f"Struct: {struct_name}")
            
            # Find functions
            func_pattern = r'(?:(?:static|inline|extern)\s+)?(?:[\w:]+\s+)+([\w:]+)\s*\(([^)]*)\)\s*(?:\{|;)'
            for match in re.finditer(func_pattern, content):
                func_name = match.group(1)
                func_params = match.group(2)
                # Skip if this is likely a constructor/destructor or operator overload
                if re.match(r'^[~]?\w+$', func_name) and not re.match(r'^operator', func_name):
                    functions.append(f"Function: {func_name}({func_params})")
            
            # Format the output
            if namespaces:
                result.append("\nNamespaces:")
                for namespace in namespaces:
                    result.append(f"  └── {namespace}")
            
            if classes:
                result.append("\nClasses:")
                for cls in classes:
                    result.append(f"  └── {cls}")
            
            if structs:
                result.append("\nStructs:")
                for struct in structs:
                    result.append(f"  └── {struct}")
            
            if functions:
                result.append("\nFunctions:")
                for func in functions[:15]:  # Limit to 15 functions to avoid clutter
                    result.append(f"  └── {func}")
                if len(functions) > 15:
                    result.append(f"  └── ... and {len(functions) - 15} more functions")
                    
        elif language in ['java']:
            # Java parsing
            classes = []
            interfaces = []
            enums = []
            methods = []
            imports = []
            package = None
            
            # Find package declaration
            package_pattern = r'package\s+([\w.]+)\s*;'
            package_match = re.search(package_pattern, content)
            if package_match:
                package = package_match.group(1)
            
            # Find imports
            import_pattern = r'import\s+(?:static\s+)?([\w.*]+)\s*;'
            for match in re.finditer(import_pattern, content):
                import_name = match.group(1)
                imports.append(f"Import: {import_name}")
            
            # Find classes
            class_pattern = r'(?:public|protected|private)?\s*(?:abstract|final)?\s*class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]*))?\s*\{'
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                extends = match.group(2) if match.group(2) else None
                implements = match.group(3).strip() if match.group(3) else None
                
                class_info = f"Class: {class_name}"
                if extends:
                    class_info += f" extends {extends}"
                if implements:
                    class_info += f" implements {implements}"
                classes.append(class_info)
            
            # Find interfaces
            interface_pattern = r'(?:public|protected|private)?\s*interface\s+(\w+)(?:\s+extends\s+([^{]*))?\s*\{'
            for match in re.finditer(interface_pattern, content):
                interface_name = match.group(1)
                extends = match.group(2).strip() if match.group(2) else None
                
                interface_info = f"Interface: {interface_name}"
                if extends:
                    interface_info += f" extends {extends}"
                interfaces.append(interface_info)
            
            # Find enums
            enum_pattern = r'(?:public|protected|private)?\s*enum\s+(\w+)(?:\s+implements\s+([^{]*))?\s*\{'
            for match in re.finditer(enum_pattern, content):
                enum_name = match.group(1)
                implements = match.group(2).strip() if match.group(2) else None
                
                enum_info = f"Enum: {enum_name}"
                if implements:
                    enum_info += f" implements {implements}"
                enums.append(enum_info)
            
            # Find methods
            method_pattern = r'(?:public|protected|private|static|final|abstract|synchronized)?\s+(?:static\s+)?[\w<>\[\],\s]+\s+(\w+)\s*\(([^)]*)\)\s*(?:throws\s+[\w,\s]+)?\s*(?:\{|;)'
            for match in re.finditer(method_pattern, content):
                method_name = match.group(1)
                method_params = match.group(2)
                # Skip if this is likely a constructor
                if not any(method_name == class_name for class_name in [m.split(":")[1].strip() for m in classes]):
                    methods.append(f"Method: {method_name}({method_params})")
            
            # Format the output
            if package:
                result.append(f"\nPackage: {package}")
            
            if imports:
                result.append("\nImports:")
                for imp in imports[:5]:  # Limit to first 5 imports
                    result.append(f"  └── {imp}")
                if len(imports) > 5:
                    result.append(f"  └── ... and {len(imports) - 5} more imports")
            
            if classes:
                result.append("\nClasses:")
                for cls in classes:
                    result.append(f"  └── {cls}")
            
            if interfaces:
                result.append("\nInterfaces:")
                for interface in interfaces:
                    result.append(f"  └── {interface}")
            
            if enums:
                result.append("\nEnums:")
                for enum in enums:
                    result.append(f"  └── {enum}")
            
            if methods:
                result.append("\nMethods:")
                for method in methods[:15]:  # Limit to 15 methods
                    result.append(f"  └── {method}")
                if len(methods) > 15:
                    result.append(f"  └── ... and {len(methods) - 15} more methods")
                    
        else:
            # Generic code structure for other languages
            result.append(f"\nLanguage '{language}' parsing not fully implemented.")
            result.append("Showing basic file information:")
            
            # Count lines of code
            lines = content.split('\n')
            result.append(f"  └── Lines of code: {len(lines)}")
            
            # Count non-empty, non-comment lines
            non_empty = sum(1 for line in lines if line.strip() and not line.strip().startswith(('//', '#', '/*', '*', '*/'))) 
            result.append(f"  └── Non-empty, non-comment lines: {non_empty}")
    
    except Exception as e:
        result.append(f"Error parsing file: {str(e)}")
    
    return result

def relation_command(args):
    """Generate a code relation diagram showing dependencies."""
    print(f"Generating code relation diagram for {args.path}")
    
    if not os.path.exists(args.path):
        print(f"Error: Path {args.path} does not exist")
        sys.exit(1)
    
    try:
        diagram = create_relation_diagram(args.path, args.depth)
        with open(args.output, 'w') as f:
            f.write(diagram)
        print(f"Success: Relation diagram saved to {args.output}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def create_relation_diagram(path, depth=1, max_files=500):
    """Create a diagram showing code relationships and dependencies."""
    result = []
    
    # Check if path exists
    if not os.path.exists(path):
        print(f"Error: Path {path} does not exist")
        return "\n".join(result)
        
    # Set a timeout for regex operations to prevent hanging
    # This is a workaround for the re.search timeout parameter not being available in all Python versions
    import signal
    
    # Define a timeout handler
    def timeout_handler(signum, frame):
        raise TimeoutError("Regex operation timed out")
    
    # Set the timeout signal handler
    signal.signal(signal.SIGALRM, timeout_handler)

    # Collect all code files
    code_files = []
    if os.path.isdir(path):
        # Directories to exclude
        exclude_dirs = ['node_modules', 'venv', '.venv', 'env', '.env', '.git', '__pycache__', 'dist', 'build', 'target', 'bin', 'obj']
        
        for root, dirs, files in os.walk(path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip files that are too large
                try:
                    if os.path.getsize(file_path) > 1024 * 1024:  # Skip files larger than 1MB
                        continue
                except (OSError, IOError):
                    continue  # Skip files we can't access
                
                file_ext = os.path.splitext(file)[1].lower()
                
                # Code files
                code_extensions = [
                    # Web Development
                    '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.scss', '.sass', '.less', '.php', '.vue', '.svelte', '.astro',
                    # Mobile & Desktop
                    '.java', '.kt', '.kts', '.swift', '.m', '.h', '.dart', '.cs', '.fs', '.fsx', '.vb', '.xaml', '.cshtml',
                    # Systems Programming
                    '.c', '.cpp', '.cc', '.cxx', '.hpp', '.rs', '.go', '.zig', '.d', '.nim',
                    # Scripting
                    '.rb', '.erb', '.pl', '.pm', '.sh', '.bash', '.zsh', '.ps1', '.lua', '.tcl',
                    # Functional
                    '.hs', '.elm', '.ml', '.ex', '.exs', '.erl', '.clj', '.cljs',
                    # Data Science
                    '.r', '.jl', '.ipynb',
                    # Configuration
                    '.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.sql', '.graphql', '.proto'
                ]
                
                # Project files
                project_extensions = [
                    # .NET
                    '.csproj', '.fsproj', '.vbproj', '.sln', '.props', '.targets',
                    # JVM
                    '.gradle', 'pom.xml', 'build.gradle', 'build.sbt',
                    # JavaScript
                    'package.json', 'tsconfig.json', 'webpack.config.js', 'rollup.config.js', 'next.config.js', 'nuxt.config.js',
                    # Python
                    'pyproject.toml', 'setup.py', 'Pipfile', 'requirements.txt',
                    # Ruby
                    'Gemfile', 'Rakefile',
                    # Rust
                    'Cargo.toml',
                    # Go
                    'go.mod',
                    # Build systems
                    'CMakeLists.txt', 'Makefile', '.cmake', '.make', '.mk',
                    # CI/CD
                    '.gitlab-ci.yml', '.travis.yml', 'appveyor.yml', 'azure-pipelines.yml', 'Jenkinsfile',
                    # Container
                    'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml',
                    # Infrastructure
                    '.tf', '.tfvars', '.hcl', 'serverless.yml', 'Chart.yaml', 'kustomization.yaml'
                ]
                
                if file_ext.lower() in code_extensions or os.path.basename(file_path) in project_extensions or any(file_path.endswith(ext) for ext in project_extensions):
                    code_files.append(file_path)
    else:
        code_files = [path]
    
    # Extract imports and dependencies from each file
    file_dependencies = {}
    file_exports = {}
    file_symbols = {}
    
    for file_path in code_files:
        rel_path = os.path.relpath(file_path, path) if os.path.isdir(path) else os.path.basename(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        language = detect_language_from_extension(file_ext)
        
        imports, exports, symbols = extract_dependencies(file_path, language)
        
        file_dependencies[rel_path] = imports
        file_exports[rel_path] = exports
        file_symbols[rel_path] = symbols
    
    # Generate the relation diagram
    if len(code_files) == 1 and not os.path.isdir(path):
        # Single file analysis - show internal relationships
        result.append("Internal Symbol Relationships:")
        file_path = code_files[0]
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        language = detect_language_from_extension(file_ext)
        
        # Get internal relationships and symbol types
        internal_relations, symbol_types = analyze_internal_relations(file_path, language)
        
        # Display symbol types first
        result.append("Symbol Types:")
        for symbol, symbol_type in symbol_types.items():
            result.append(f"  └── {symbol} [{symbol_type}]")
        
        # Display internal relationships
        result.append("\nRelationships:")
        for source, targets in internal_relations.items():
            # Skip if no relationships
            if not targets:
                continue
                
            source_type = symbol_types.get(source, '')
            result.append(f"\n{source} [{source_type}]")
            for target in targets:
                if target.startswith("inherits from") or target.startswith("has method"):
                    result.append(f"  └── {target}")
                else:
                    target_type = symbol_types.get(target, '')
                    result.append(f"  └── uses {target} [{target_type}]")
    else:
        # Multiple files - show file dependencies
        result.append("File Dependencies:")
        
        # Map file exports to their respective files
        export_to_file = {}
        for file, exports in file_exports.items():
            for export in exports:
                if export not in export_to_file:
                    export_to_file[export] = []
                export_to_file[export].append(file)
        
        # Find connections between files
        for file, imports in file_dependencies.items():
            if imports:
                result.append(f"\n{file}")
                result.append("  └── imports from:")
                
                for imported in imports:
                    # Find which files export this symbol
                    source_files = export_to_file.get(imported, [])
                    
                    if source_files:
                        for source in source_files:
                            result.append(f"      └── {imported} (from {source})")
                    else:
                        # External dependency
                        result.append(f"      └── {imported} (external)")
        
        # If depth > 1, show more detailed symbol usage across files
        if depth >= 2:
            result.append("\n\nSymbol Usage Across Files:")
            
            # Create a map of symbols to their defining files
            symbol_to_file = {}
            for file, symbols in file_symbols.items():
                for symbol in symbols:
                    if symbol not in symbol_to_file:
                        symbol_to_file[symbol] = []
                    symbol_to_file[symbol].append(file)
            
            # Create a map of which symbols are used in which files
            symbol_usage = {}
            for file, imports in file_dependencies.items():
                for imported in imports:
                    base_symbol = imported.split('.')[-1]  # Get the base symbol name
                    if base_symbol not in symbol_usage:
                        symbol_usage[base_symbol] = []
                    symbol_usage[base_symbol].append(file)
            
            # Show symbol definitions and usage
            for file, symbols in file_symbols.items():
                if symbols:
                    result.append(f"\n{file} defines:")
                    for symbol in symbols:
                        result.append(f"  └── {symbol}")
                        
                        # Find which files import/use this symbol
                        using_files = symbol_usage.get(symbol, [])
                        if using_files:
                            result.append("      └── used by:")
                            for using_file in using_files:
                                if using_file != file:  # Don't show self-usage
                                    result.append(f"          └── {using_file}")
            
            # If depth >= 3, show function call graph
            if depth >= 3:
                result.append("\n\nFunction Call Graph:")
                
                # Analyze each file for function calls
                function_calls = {}
                for file_path in code_files:
                    rel_path = os.path.relpath(file_path, path) if os.path.isdir(path) else os.path.basename(file_path)
                    file_ext = os.path.splitext(file_path)[1].lower()
                    language = detect_language_from_extension(file_ext)
                    
                    # Get internal relationships
                    file_relations, _ = analyze_internal_relations(file_path, language)
                    
                    # Add to global function call map
                    for caller, callees in file_relations.items():
                        if caller not in function_calls:
                            function_calls[caller] = []
                        
                        for callee in callees:
                            if not callee.startswith("inherits from") and not callee.startswith("has method"):
                                function_calls[caller].append((callee, rel_path))
                
                # Display function call graph
                for caller, callees in function_calls.items():
                    if callees:  # Only show functions that call others
                        defining_files = symbol_to_file.get(caller, ['unknown'])
                        result.append(f"\n{caller} (in {', '.join(defining_files)})")
                        for callee, file in callees:
                            result.append(f"  └── calls {callee} (in {file})")
    
    return "\n".join(result)

def extract_dependencies(file_path, language):
    """Extract imports, exports, and symbols from a file."""
    imports = []
    exports = []
    symbols = []
    
    try:
        # Special handling for project files
        file_ext = os.path.splitext(file_path)[1].lower()
        file_name = os.path.basename(file_path)
        
        # .NET project files
        if file_ext in ['.csproj', '.fsproj', '.vbproj', '.sln']:
            return parse_dotnet_project_file(file_path, file_ext)
        
        # Other project files
        project_file_patterns = [
            'package.json', 'requirements.txt', 'Dockerfile', 'docker-compose.yml',
            'go.mod', 'pom.xml', 'build.gradle', 'Cargo.toml', 'Gemfile',
            'pyproject.toml', 'setup.py', 'Pipfile', '.gitlab-ci.yml', '.travis.yml',
            'webpack.config.js', 'tsconfig.json', 'CMakeLists.txt', 'Makefile'
        ]
        
        if file_name in project_file_patterns or file_ext in ['.gradle', '.tf', '.yaml', '.yml'] and any(file_name.endswith(pattern) for pattern in ['.tf', 'docker-compose.yml', 'docker-compose.yaml', 'serverless.yml', 'Chart.yaml', 'kustomization.yaml']):
            return parse_project_file(file_path)
            
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if language in ['python']:
            # Python imports
            import_patterns = [
                r'import\s+([\w.]+)',  # import module
                r'from\s+([\w.]+)\s+import\s+([^\n]+)'  # from module import symbol
            ]
            
            for pattern in import_patterns:
                for match in re.finditer(pattern, content):
                    if pattern == import_patterns[0]:
                        imports.append(match.group(1))
                    else:  # from ... import ...
                        module = match.group(1)
                        symbols_str = match.group(2)
                        for symbol in re.findall(r'\b(\w+)\b', symbols_str):
                            imports.append(f"{module}.{symbol}")
            
            # Python classes and functions (potential exports)
            class_pattern = r'class\s+(\w+)'
            func_pattern = r'def\s+(\w+)'
            
            # Check for __all__ declaration
            all_exports = []
            all_pattern = r'__all__\s*=\s*\[([^\]]+)\]'
            all_match = re.search(all_pattern, content)
            if all_match:
                all_content = all_match.group(1)
                # Extract symbols from __all__ list
                for symbol in re.finditer(r'[\'\"]([\w_]+)[\'\",\s]', all_content):
                    all_exports.append(symbol.group(1))
            
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                symbols.append(class_name)
                # Add to exports if it's in __all__ or looks like a public class
                if class_name in all_exports or not class_name.startswith('_'):
                    exports.append(class_name)
            
            for match in re.finditer(func_pattern, content):
                func_name = match.group(1)
                # Skip private functions (starting with single underscore)
                if not func_name.startswith('_') or (func_name.startswith('__') and func_name.endswith('__')):
                    symbols.append(func_name)
                    # Add to exports if it's in __all__ or looks like a public function
                    if func_name in all_exports or not func_name.startswith('_'):
                        exports.append(func_name)
        
        elif language in ['javascript', 'typescript', 'js', 'ts']:
            # JS/TS imports
            import_patterns = [
                r'import\s+{([^}]*)}\s+from\s+[\'"]([^\'"]*)[\'"](;)?',  # import {symbols} from 'module'
                r'import\s+(\w+)\s+from\s+[\'"]([^\'"]*)[\'"](;)?',  # import symbol from 'module'
                r'import\s+\*\s+as\s+(\w+)\s+from\s+[\'"]([^\'"]*)[\'"](;)?',  # import * as symbol from 'module'
                r'require\([\'"]([^\'"]*)[\'"]\)'  # require('module')
            ]
            
            for pattern in import_patterns:
                for match in re.finditer(pattern, content):
                    if pattern == import_patterns[0]:  # Named imports
                        module = match.group(2)
                        for symbol in re.findall(r'\b(\w+)\b', match.group(1)):
                            imports.append(f"{module}.{symbol}")
                    elif pattern == import_patterns[3]:  # require
                        imports.append(match.group(1))
                    else:  # Default or namespace import
                        imports.append(f"{match.group(2)}.{match.group(1)}")
            
            # JS/TS exports
            export_patterns = [
                r'export\s+(?:default\s+)?(?:class|function|const|let|var)\s+(\w+)',  # export class/function/variable
                r'export\s+{([^}]*)}(;)?',  # export {symbols}
                r'export\s+default\s+(\w+)(;)?'  # export default symbol
            ]
            
            for pattern in export_patterns:
                for match in re.finditer(pattern, content):
                    if pattern == export_patterns[1]:  # Named exports
                        for symbol in re.findall(r'\b(\w+)\b', match.group(1)):
                            exports.append(symbol)
                    else:  # Default or direct export
                        exports.append(match.group(1))
            
            # JS/TS classes, functions, and variables
            symbol_patterns = [
                r'(?:export\s+)?class\s+(\w+)',  # class
                r'(?:export\s+)?(?:function|const|let|var)\s+(\w+)',  # function or variable
                r'(?:export\s+)?interface\s+(\w+)'  # interface (TS)
            ]
            
            for pattern in symbol_patterns:
                for match in re.finditer(pattern, content):
                    symbols.append(match.group(1))
        
        elif language in ['java']:
            # Java imports
            import_pattern = r'import\s+(?:static\s+)?([\w.]+)\s*;'
            for match in re.finditer(import_pattern, content):
                imports.append(match.group(1))
            
            # Java classes, interfaces, and enums (exports)
            class_patterns = [
                r'(?:public|protected)\s+(?:class|interface|enum)\s+(\w+)',  # public class/interface/enum
            ]
            
            for pattern in class_patterns:
                for match in re.finditer(pattern, content):
                    symbol = match.group(1)
                    symbols.append(symbol)
                    exports.append(symbol)
            
            # Java methods
            method_pattern = r'(?:public|protected)\s+(?:static\s+)?[\w<>\[\],\s]+\s+(\w+)\s*\(([^)]*)\)'
            for match in re.finditer(method_pattern, content):
                symbols.append(match.group(1))
        
        elif language in ['rust', 'rs']:
            # Rust imports (use statements)
            import_pattern = r'use\s+([^;]+);'
            for match in re.finditer(import_pattern, content):
                imports.append(match.group(1))
            
            # Rust exports (pub items)
            export_patterns = [
                r'pub\s+(?:struct|enum|trait|fn|type|mod)\s+(\w+)',  # pub struct/enum/trait/fn/type/mod
                r'pub\s+use\s+([^;]+);'  # pub use
            ]
            
            for pattern in export_patterns:
                for match in re.finditer(pattern, content):
                    if pattern == export_patterns[1]:  # pub use
                        for symbol in re.findall(r'\b(\w+)\b', match.group(1)):
                            exports.append(symbol)
                    else:  # Direct pub item
                        exports.append(match.group(1))
            
            # Rust symbols
            symbol_patterns = [
                r'(?:pub\s+)?(?:struct|enum|trait|fn|type|mod)\s+(\w+)',  # struct/enum/trait/fn/type/mod
                r'impl(?:<[^>]*>)?\s+(?:([^\s{]+)\s+for\s+)?([^\s{<]+)'  # impl or impl Trait for Type
            ]
            
            for pattern in symbol_patterns:
                for match in re.finditer(pattern, content):
                    if pattern == symbol_patterns[1]:  # impl
                        if match.group(1):  # impl Trait for Type
                            symbols.append(match.group(1))
                        symbols.append(match.group(2))
                    else:  # Direct symbol
                        symbols.append(match.group(1))
        
        elif language in ['csharp', 'cs']:
            # C# using statements (imports)
            import_pattern = r'using\s+([\w.]+)\s*;'
            for match in re.finditer(import_pattern, content):
                imports.append(match.group(1))
            
            # C# namespace
            namespace_pattern = r'namespace\s+([\w.]+)\s*{'
            namespace = None
            namespace_match = re.search(namespace_pattern, content)
            if namespace_match:
                namespace = namespace_match.group(1)
                exports.append(f"namespace:{namespace}")
            
            # C# classes, interfaces, structs, enums
            type_patterns = [
                r'(?:public|internal|private|protected)?\s*(?:abstract|sealed|static)?\s*class\s+(\w+)(?:\s*:\s*([^{]*))?\s*{',  # class
                r'(?:public|internal|private|protected)?\s*(?:abstract|sealed|static)?\s*interface\s+(\w+)(?:\s*:\s*([^{]*))?\s*{',  # interface
                r'(?:public|internal|private|protected)?\s*(?:abstract|sealed|static)?\s*struct\s+(\w+)(?:\s*:\s*([^{]*))?\s*{',  # struct
                r'(?:public|internal|private|protected)?\s*enum\s+(\w+)\s*{',  # enum
                r'(?:public|internal|private|protected)?\s*record\s+(\w+)(?:\s*\(([^)]*)\))?(?:\s*:\s*([^{]*))?\s*{?'  # record
            ]
            
            for pattern in type_patterns:
                for match in re.finditer(pattern, content):
                    type_name = match.group(1)
                    symbols.append(type_name)
                    if namespace:
                        exports.append(f"{namespace}.{type_name}")
                    else:
                        exports.append(type_name)
            
            # C# methods
            method_pattern = r'(?:public|internal|private|protected)?\s*(?:static|virtual|abstract|override|async)?\s*(?:[\w<>\[\],\s.]+)\s+(\w+)\s*\(([^)]*)\)\s*(?:{|=>)'
            for match in re.finditer(method_pattern, content):
                method_name = match.group(1)
                # Skip constructor names (same as class names)
                if method_name not in symbols:
                    symbols.append(method_name)
            
            # C# properties
            property_pattern = r'(?:public|internal|private|protected)?\s*(?:static|virtual|abstract|override)?\s*(?:[\w<>\[\],\s.]+)\s+(\w+)\s*{\s*(?:get|set)'
            for match in re.finditer(property_pattern, content):
                property_name = match.group(1)
                symbols.append(property_name)
        
        elif language in ['csharp', 'cs']:
            # C# using statements (imports)
            import_pattern = r'using\s+([\w.]+)\s*;'
            for match in re.finditer(import_pattern, content):
                imports.append(match.group(1))
            
            # C# namespace
            namespace_pattern = r'namespace\s+([\w.]+)\s*{'
            namespace = None
            namespace_match = re.search(namespace_pattern, content)
            if namespace_match:
                namespace = namespace_match.group(1)
                exports.append(f"namespace:{namespace}")
            
            # C# classes, interfaces, structs, enums
            type_patterns = [
                r'(?:public|internal|private|protected)?\s*(?:abstract|sealed|static)?\s*class\s+(\w+)(?:\s*:\s*([^{]*))?\s*{',  # class
                r'(?:public|internal|private|protected)?\s*(?:abstract|sealed|static)?\s*interface\s+(\w+)(?:\s*:\s*([^{]*))?\s*{',  # interface
                r'(?:public|internal|private|protected)?\s*(?:abstract|sealed|static)?\s*struct\s+(\w+)(?:\s*:\s*([^{]*))?\s*{',  # struct
                r'(?:public|internal|private|protected)?\s*enum\s+(\w+)\s*{',  # enum
                r'(?:public|internal|private|protected)?\s*record\s+(\w+)(?:\s*\(([^)]*)\))?(?:\s*:\s*([^{]*))?\s*{?'  # record
            ]
            
            for pattern in type_patterns:
                for match in re.finditer(pattern, content):
                    type_name = match.group(1)
                    symbols.append(type_name)
                    if namespace:
                        exports.append(f"{namespace}.{type_name}")
                    else:
                        exports.append(type_name)
            
            # C# methods
            method_pattern = r'(?:public|internal|private|protected)?\s*(?:static|virtual|abstract|override|async)?\s*(?:[\w<>\[\],\s.]+)\s+(\w+)\s*\(([^)]*)\)\s*(?:{|=>)'
            for match in re.finditer(method_pattern, content):
                method_name = match.group(1)
                # Skip constructor names (same as class names)
                if method_name not in symbols:
                    symbols.append(method_name)
            
            # C# properties
            property_pattern = r'(?:public|internal|private|protected)?\s*(?:static|virtual|abstract|override)?\s*(?:[\w<>\[\],\s.]+)\s+(\w+)\s*{\s*(?:get|set)'
            for match in re.finditer(property_pattern, content):
                property_name = match.group(1)
                symbols.append(property_name)
        
        # Remove duplicates
        imports = list(set(imports))
        exports = list(set(exports))
        symbols = list(set(symbols))
    
    except Exception as e:
        print(f"Warning: Error extracting dependencies from {file_path}: {str(e)}")
    
    return imports, exports, symbols

def analyze_internal_relations(file_path, language):
    """Analyze internal relationships between symbols in a file."""
    relations = defaultdict(list)
    symbol_types = {}  # Track symbol types (class, function, method, etc.)
    class_methods = {}  # Track which methods belong to which classes
    inheritance = {}  # Track inheritance relationships
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract all symbols first
        symbols = []
    except Exception as e:
        print(f"Warning: Error reading file {file_path}: {str(e)}")
        return relations, symbol_types
        
    try:
        # First pass: identify all symbols and their types
        if language in ['python']:
            # Python classes
            class_pattern = r'class\s+(\w+)(?:\s*\(([^)]+)\))?\s*:'
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                parent_classes = match.group(2)
                symbols.append(class_name)
                symbol_types[class_name] = 'class'
                class_methods[class_name] = []
                
                # Track inheritance
                if parent_classes:
                    for parent in re.findall(r'\b(\w+)\b', parent_classes):
                        if parent not in ['object']:
                            inheritance[class_name] = inheritance.get(class_name, []) + [parent]
            
            # Python functions and methods
            func_pattern = r'def\s+(\w+)\s*\(([^)]*)\)\s*:'
            for match in re.finditer(func_pattern, content):
                func_name = match.group(1)
                params = match.group(2)
                
                # Check if this is a method (indented inside a class)
                is_method = False
                for class_name in symbol_types:
                    if symbol_types[class_name] == 'class':
                        # Look for method definition inside class
                        if re.search(rf'class\s+{class_name}[^\n]*:[^\n]*(?:\n+[^\n]*)*\n+\s+def\s+{func_name}\s*\(', content, re.DOTALL):
                            is_method = True
                            class_methods[class_name].append(func_name)
                            symbol_types[func_name] = f'method of {class_name}'
                            break
                
                if not is_method:
                    symbols.append(func_name)
                    symbol_types[func_name] = 'function'
        
        elif language in ['javascript', 'typescript', 'js', 'ts']:
            # JS/TS classes
            class_pattern = r'(?:export\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?\s*{'
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                parent_class = match.group(2)
                symbols.append(class_name)
                symbol_types[class_name] = 'class'
                class_methods[class_name] = []
                
                # Track inheritance
                if parent_class:
                    inheritance[class_name] = [parent_class]
            
            # JS/TS methods (inside classes)
            method_pattern = r'class\s+\w+[^{]*{([^}]*)}'
            for class_match in re.finditer(class_pattern, content):
                class_name = class_match.group(1)
                class_body_match = re.search(rf'class\s+{class_name}[^{{]*{{([^{{}}]*(?:{{[^{{}}]*}}[^{{}}]*)*)}}', content, re.DOTALL)
                
                if class_body_match:
                    class_body = class_body_match.group(1)
                    # Find methods in class body
                    for method_match in re.finditer(r'\b(\w+)\s*\(([^)]*)\)', class_body):
                        method_name = method_match.group(1)
                        if method_name not in ['constructor', 'super']:
                            class_methods[class_name].append(method_name)
                            symbol_types[method_name] = f'method of {class_name}'
            
            # JS/TS functions and variables
            func_patterns = [
                r'(?:export\s+)?function\s+(\w+)\s*\(([^)]*)\)',  # Regular functions
                r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*function\s*\(([^)]*)\)',  # Function expressions
                r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*\(([^)]*)\)\s*=>',  # Arrow functions
            ]
            
            for pattern in func_patterns:
                for match in re.finditer(pattern, content):
                    func_name = match.group(1)
                    # Skip if this is a method already identified
                    if func_name not in symbol_types:
                        symbols.append(func_name)
                        symbol_types[func_name] = 'function'
            
            # JS/TS variables
            var_pattern = r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?!function|\(.*\)\s*=>)'
            for match in re.finditer(var_pattern, content):
                var_name = match.group(1)
                if var_name not in symbol_types:
                    symbols.append(var_name)
                    symbol_types[var_name] = 'variable'
        
        elif language in ['java']:
            # Java classes and interfaces
            class_patterns = [
                r'(?:public|private|protected)?\s*(?:abstract|final)?\s*class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?\s*\{',  # class
                r'(?:public|private|protected)?\s*interface\s+(\w+)(?:\s+extends\s+([^{]+))?\s*\{'  # interface
            ]
            
            for pattern in class_patterns:
                for match in re.finditer(pattern, content):
                    class_name = match.group(1)
                    symbol_types[class_name] = 'class' if 'class' in pattern else 'interface'
                    
                    # Track inheritance
                    if len(match.groups()) > 1 and match.group(2):
                        parent = match.group(2)
                        inheritance[class_name] = inheritance.get(class_name, []) + [parent]
                    
                    # Track interface implementation
                    if len(match.groups()) > 2 and match.group(3) and 'implements' in pattern:
                        for interface in re.findall(r'\b(\w+)\b', match.group(3)):
                            inheritance[class_name] = inheritance.get(class_name, []) + [interface]
            
            # Java methods
            method_pattern = r'(?:public|private|protected)?\s*(?:static|final|abstract)?\s*(?:[\w<>\[\],\s.]+)\s+(\w+)\s*\(([^)]*)\)\s*(?:\{|;)'
            for match in re.finditer(method_pattern, content):
                method_name = match.group(1)
                # Skip constructor names (same as class names)
                if method_name not in symbol_types:
                    symbol_types[method_name] = 'method'
                    
                    # Try to determine which class this method belongs to
                    method_pos = match.start()
                    for class_match in re.finditer(r'(?:public|private|protected)?\s*(?:abstract|final)?\s*class\s+(\w+)', content):
                        class_name = class_match.group(1)
                        class_end_match = re.search(r'\}\s*$', content[class_match.end():])
                        if class_end_match and class_match.end() < method_pos < (class_match.end() + class_end_match.end()):
                            class_methods[class_name] = class_methods.get(class_name, []) + [method_name]
                            relations[method_name].append(class_name)
                            break
                            
        elif language in ['csharp', 'cs']:
            # Extract namespace
            namespace = None
            namespace_pattern = r'namespace\s+([\w.]+)\s*{'
            namespace_match = re.search(namespace_pattern, content)
            if namespace_match:
                namespace = namespace_match.group(1)
                symbol_types[f"namespace:{namespace}"] = 'namespace'
            
            # C# classes, interfaces, structs, enums, records
            type_patterns = [
                (r'(?:public|internal|private|protected)?\s*(?:abstract|sealed|static)?\s*class\s+(\w+)(?:\s*:\s*([^{]*))?\s*{', 'class'),
                (r'(?:public|internal|private|protected)?\s*(?:abstract|sealed|static)?\s*interface\s+(\w+)(?:\s*:\s*([^{]*))?\s*{', 'interface'),
                (r'(?:public|internal|private|protected)?\s*(?:abstract|sealed|static)?\s*struct\s+(\w+)(?:\s*:\s*([^{]*))?\s*{', 'struct'),
                (r'(?:public|internal|private|protected)?\s*enum\s+(\w+)\s*{', 'enum'),
                (r'(?:public|internal|private|protected)?\s*record\s+(\w+)(?:\s*\(([^)]*)\))?(?:\s*:\s*([^{]*))?\s*{?', 'record')
            ]
            
            for pattern, type_kind in type_patterns:
                for match in re.finditer(pattern, content):
                    class_name = match.group(1)
                    symbol_types[class_name] = type_kind
                    class_methods[class_name] = []
                    
                    # Check for inheritance/implementation
                    if len(match.groups()) > 1 and match.group(2):
                        base_types = re.findall(r'\b([\w.]+)\b', match.group(2))
                        for base_type in base_types:
                            if base_type not in ['where', 'class', 'struct', 'interface', 'record']:
                                inheritance[class_name] = inheritance.get(class_name, []) + [base_type]
            
            # C# methods and properties
            member_patterns = [
                (r'(?:public|internal|private|protected)?\s*(?:static|virtual|abstract|override|async)?\s*(?:[\w<>\[\],\s.]+)\s+(\w+)\s*\(([^)]*)\)\s*(?:{|=>)', 'method'),
                (r'(?:public|internal|private|protected)?\s*(?:static|virtual|abstract|override)?\s*(?:[\w<>\[\],\s.]+)\s+(\w+)\s*{\s*(?:get|set)', 'property')
            ]
            
            for pattern, member_type in member_patterns:
                for match in re.finditer(pattern, content):
                    member_name = match.group(1)
                    # Skip constructors (same name as class)
                    if member_name not in symbol_types:
                        symbol_types[member_name] = member_type
                        
                        # Find which class/type this member belongs to
                        member_pos = match.start()
                        for type_pattern, _ in type_patterns:
                            for type_match in re.finditer(type_pattern, content):
                                type_name = type_match.group(1)
                                # Find the end of the type declaration
                                type_content = content[type_match.end():]
                                brace_count = 1
                                end_pos = 0
                                for i, char in enumerate(type_content):
                                    if char == '{': brace_count += 1
                                    elif char == '}': brace_count -= 1
                                    if brace_count == 0:
                                        end_pos = i
                                        break
                                
                                # Check if the member is inside this type
                                if type_match.end() < member_pos < (type_match.end() + end_pos):
                                    class_methods[type_name] = class_methods.get(type_name, []) + [member_name]
                                    relations[member_name].append(type_name)
                                    break
                else:
                    # Not a method of any class
                    symbols.append(method_name)
                    symbol_types[method_name] = 'function'
        
        elif language in ['rust', 'rs']:
            # Rust structs and enums
            struct_pattern = r'(?:pub\s+)?struct\s+(\w+)'
            enum_pattern = r'(?:pub\s+)?enum\s+(\w+)'
            
            for match in re.finditer(struct_pattern, content):
                struct_name = match.group(1)
                symbols.append(struct_name)
                symbol_types[struct_name] = 'struct'
            
            for match in re.finditer(enum_pattern, content):
                enum_name = match.group(1)
                symbols.append(enum_name)
                symbol_types[enum_name] = 'enum'
            
            # Rust implementations
            impl_pattern = r'impl(?:<[^>]*>)?\s+(?:([^\s{]+)\s+for\s+)?([^\s{<]+)'
            for match in re.finditer(impl_pattern, content):
                trait_name = match.group(1)
                type_name = match.group(2)
                
                if trait_name:
                    # This is a trait implementation
                    if type_name not in inheritance:
                        inheritance[type_name] = []
                    inheritance[type_name].append(f"trait:{trait_name}")
            
            # Rust functions
            func_pattern = r'(?:pub\s+)?fn\s+(\w+)\s*\(([^)]*)\)'
            for match in re.finditer(func_pattern, content):
                func_name = match.group(1)
                # Check if this is a method in an impl block
                is_method = False
                for impl_match in re.finditer(impl_pattern, content):
                    type_name = impl_match.group(2) if impl_match.group(2) else impl_match.group(1)
                    impl_block_match = re.search(rf'impl[^{{]*{type_name}[^{{]*{{([^{{}}]*(?:{{[^{{}}]*}}[^{{}}]*)*)}}', content, re.DOTALL)
                    if impl_block_match and re.search(rf'fn\s+{func_name}\s*\(', impl_block_match.group(1)):
                        is_method = True
                        if type_name not in class_methods:
                            class_methods[type_name] = []
                        class_methods[type_name].append(func_name)
                        symbol_types[func_name] = f'method of {type_name}'
                        break
                
                if not is_method:
                    symbols.append(func_name)
                    symbol_types[func_name] = 'function'
        
        # Second pass: analyze relationships between symbols
        for symbol in symbols + list(symbol_types.keys()):
            # Skip if this is a method (will be analyzed with its class)
            if symbol in symbol_types and 'method of' in symbol_types.get(symbol, ''):
                continue
                
            # Get the definition of the symbol - with improved error handling
            symbol_def = ""
            try:
                if language in ['python']:
                    if symbol_types.get(symbol) == 'class':
                        try:
                            # Use re.escape to handle special characters in symbol names
                            pattern = rf'class\s+{re.escape(symbol)}[^:]*:'
                            class_match = re.search(pattern, content)
                            if class_match:
                                # Get a limited portion of the class definition to avoid memory issues
                                start_pos = class_match.end()
                                end_pos = min(start_pos + 2000, len(content))  # Limit to 2000 chars
                                symbol_def = content[start_pos:end_pos]
                        except re.error:
                            # Skip problematic regex patterns
                            pass
                    elif symbol_types.get(symbol) == 'function':
                        try:
                            pattern = rf'def\s+{re.escape(symbol)}[^:]*:'
                            func_match = re.search(pattern, content)
                            if func_match:
                                # Get a limited portion of the function definition
                                start_pos = func_match.end()
                                end_pos = min(start_pos + 1000, len(content))  # Limit to 1000 chars
                                symbol_def = content[start_pos:end_pos]
                        except re.error:
                            # Skip problematic regex patterns
                            pass
                            
                elif language in ['javascript', 'typescript', 'js', 'ts']:
                    if symbol_types.get(symbol) == 'class':
                        try:
                            pattern = rf'class\s+{re.escape(symbol)}[^{{]*{{'
                            class_match = re.search(pattern, content)
                            if class_match:
                                # Get a limited portion of the class definition
                                start_pos = class_match.end()
                                end_pos = min(start_pos + 2000, len(content))  # Limit to 2000 chars
                                symbol_def = content[start_pos:end_pos]
                        except re.error:
                            pass
                    elif symbol_types.get(symbol) == 'function':
                        try:
                            # Try different function patterns with timeouts
                            patterns = [
                                rf'function\s+{re.escape(symbol)}[^{{]*{{',
                                rf'(?:const|let|var)\s+{re.escape(symbol)}\s*=\s*\([^)]*\)\s*=>\s*{{'
                            ]
                            for pattern in patterns:
                                func_match = re.search(pattern, content)
                                if func_match:
                                    start_pos = func_match.end()
                                    end_pos = min(start_pos + 1000, len(content))  # Limit to 1000 chars
                                    symbol_def = content[start_pos:end_pos]
                                    break
                        except re.error:
                            pass
            except Exception as e:
                # If any error occurs during symbol definition extraction, just continue
                print(f"Warning: Error extracting definition for symbol {symbol} in {file_path}: {str(e)}")
                pass
            
            # Add inheritance relationships
            if symbol in inheritance:
                for parent in inheritance[symbol]:
                    relations[symbol].append(f"inherits from {parent}")
            
            # Add method relationships for classes
            if symbol in class_methods and class_methods[symbol]:
                for method in class_methods[symbol]:
                    relations[symbol].append(f"has method {method}")
    
    except Exception as e:
        print(f"Warning: Error analyzing internal relations in {file_path}: {str(e)}")
    
    return relations, symbol_types

def main():
    """Main entry point for the application."""
    args = parse_arguments()
    
    if args.command == 'directory':
        directory_command(args)
    elif args.command == 'code':
        code_command(args)
    elif args.command == 'relation':
        relation_command(args)
    else:
        print("Error: Please specify a command (directory, code, or relation)")
        sys.exit(1)

if __name__ == '__main__':
    main()
