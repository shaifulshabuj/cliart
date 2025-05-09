"""
Module for parsing various project file types.
This extends CLIArt's capability to understand different project structures.
"""

import os
import re
import json
import xml.etree.ElementTree as ET
from collections import defaultdict

def parse_project_file(file_path):
    """Parse a project file and extract dependencies."""
    imports = []
    exports = []
    symbols = []
    
    try:
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # JavaScript/Node.js Project Files
        if file_name == 'package.json':
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    data = json.load(f)
                    
                    # Extract package name and version
                    if 'name' in data:
                        package_name = data['name']
                        exports.append(f"Package:{package_name}")
                    
                    if 'version' in data:
                        symbols.append(f"Version:{data['version']}")
                    
                    # Extract dependencies
                    for dep_type in ['dependencies', 'devDependencies', 'peerDependencies']:
                        if dep_type in data:
                            for dep_name, dep_version in data[dep_type].items():
                                imports.append(f"{dep_type[:-1]}:{dep_name} ({dep_version})")
                    
                    # Extract scripts
                    if 'scripts' in data:
                        for script_name in data['scripts']:
                            symbols.append(f"Script:{script_name}")
            except (json.JSONDecodeError, IOError):
                pass
        
        # Python Project Files
        elif file_name == 'requirements.txt':
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            imports.append(f"Requirement:{line}")
            except IOError:
                pass
        
        # Docker Project Files
        elif file_name == 'Dockerfile':
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Extract base image
                from_match = re.search(r'FROM\s+([^\s]+)(?:\s+AS\s+([^\s]+))?', content, re.IGNORECASE)
                if from_match:
                    base_image = from_match.group(1)
                    imports.append(f"BaseImage:{base_image}")
                    if from_match.group(2):  # AS alias
                        symbols.append(f"Stage:{from_match.group(2)}")
                
                # Extract exposed ports
                for match in re.finditer(r'EXPOSE\s+([\d/]+)', content, re.IGNORECASE):
                    port = match.group(1)
                    symbols.append(f"Port:{port}")
                
                # Extract environment variables
                for match in re.finditer(r'ENV\s+([^\s=]+)(?:\s+|=)([^\s]+)', content, re.IGNORECASE):
                    env_name = match.group(1)
                    symbols.append(f"Env:{env_name}")
            except IOError:
                pass
        
        # Go Project Files
        elif file_name == 'go.mod':
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Extract module name
                module_match = re.search(r'module\s+([^\s]+)', content)
                if module_match:
                    module_name = module_match.group(1)
                    exports.append(f"Module:{module_name}")
                
                # Extract dependencies
                for match in re.finditer(r'require\s+([^\s]+)\s+([^\s]+)', content):
                    dep_name = match.group(1)
                    dep_version = match.group(2)
                    imports.append(f"Require:{dep_name} ({dep_version})")
            except IOError:
                pass
        
        # Maven Project Files
        elif file_name == 'pom.xml':
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                
                # Extract artifact info
                group_id = root.findtext('.//groupId')
                artifact_id = root.findtext('.//artifactId')
                version = root.findtext('.//version')
                
                if artifact_id:
                    exports.append(f"Artifact:{artifact_id}")
                    if group_id:
                        symbols.append(f"GroupId:{group_id}")
                    if version:
                        symbols.append(f"Version:{version}")
                
                # Extract dependencies
                for dependency in root.findall('.//dependencies/dependency'):
                    dep_group = dependency.findtext('groupId')
                    dep_artifact = dependency.findtext('artifactId')
                    dep_version = dependency.findtext('version')
                    if dep_group and dep_artifact:
                        dep_str = f"{dep_group}:{dep_artifact}"
                        if dep_version:
                            dep_str += f" ({dep_version})"
                        imports.append(f"Dependency:{dep_str}")
            except (ET.ParseError, IOError):
                pass
        
        # Gradle Project Files
        elif file_ext == '.gradle' or file_name == 'build.gradle':
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Extract dependencies
                for match in re.finditer(r'(implementation|api|testImplementation|compileOnly)\s+[\'\"]([-\w.:\d]+)[\'\"](\\s*\{[^}]*\})?', content):
                    dep_type = match.group(1)
                    dep_name = match.group(2)
                    imports.append(f"{dep_type}:{dep_name}")
                
                # Extract plugins
                for match in re.finditer(r'apply\s+plugin:\s+[\'\"]([-\w.:\d]+)[\'\"](\\s*\{[^}]*\})?', content):
                    plugin_name = match.group(1)
                    symbols.append(f"Plugin:{plugin_name}")
            except IOError:
                pass
    
    except Exception as e:
        print(f"Warning: Error parsing project file {file_path}: {str(e)}")
    
    return imports, exports, symbols
