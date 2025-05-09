"""
Helper module to parse .NET project files.
This is used by CLIArt to extract dependencies from .NET projects.
"""

import os
import re
import xml.etree.ElementTree as ET

def parse_dotnet_project_file(file_path, file_ext):
    """Parse a .NET project file (.csproj or .sln) and extract dependencies."""
    imports = []
    exports = []
    symbols = []
    
    try:
        if file_ext == '.csproj':
            # Parse .csproj XML file
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Extract project name
            project_name = os.path.basename(file_path).replace('.csproj', '')
            exports.append(f"Project:{project_name}")
            
            # Extract package references
            for package_ref in root.findall(".//PackageReference"):
                if 'Include' in package_ref.attrib:
                    package_name = package_ref.attrib['Include']
                    version = package_ref.attrib.get('Version', '')
                    imports.append(f"{package_name} ({version})")
            
            # Extract project references
            for project_ref in root.findall(".//ProjectReference"):
                if 'Include' in project_ref.attrib:
                    ref_path = project_ref.attrib['Include']
                    ref_name = os.path.basename(ref_path).replace('.csproj', '')
                    imports.append(f"ProjectRef:{ref_name}")
            
            # Extract assembly references
            for assembly_ref in root.findall(".//Reference"):
                if 'Include' in assembly_ref.attrib:
                    assembly_name = assembly_ref.attrib['Include']
                    imports.append(f"AssemblyRef:{assembly_name}")
            
            # Extract target framework
            for target_framework in root.findall(".//TargetFramework"):
                symbols.append(f"TargetFramework:{target_framework.text}")
            
        elif file_ext == '.sln':
            # Parse .sln file using regex
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract solution name
            solution_name = os.path.basename(file_path).replace('.sln', '')
            exports.append(f"Solution:{solution_name}")
            
            # Extract project references
            project_pattern = r'Project\("\{[^}]+\}"\)\s*=\s*"([^"]+)",\s*"([^"]+)",\s*"\{[^}]+\}"'
            for match in re.finditer(project_pattern, content):
                project_name = match.group(1)
                project_path = match.group(2)
                symbols.append(f"Project:{project_name}")
                imports.append(f"ProjectPath:{project_path}")
    
    except Exception as e:
        print(f"Warning: Error parsing .NET project file {file_path}: {str(e)}")
    
    return imports, exports, symbols
