import subprocess
from mcp.server.fastmcp import FastMCP

# Initialize the server
mcp = FastMCP("nf-core-mcp-cli")

@mcp.tool()
def list_remote_modules() -> str:
    """
    Lists all available remote nf-core modules.

    Returns:
        A string containing the list of remote modules.
    """
    try:
        # Execute the nf-core command
        result = subprocess.run(
            ['nf-core', 'modules', 'list', 'remote'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except FileNotFoundError:
        return "Error: 'nf-core' command not found. Make sure nf-core tools are installed and in your PATH."
    except subprocess.CalledProcessError as e:
        return f"Error executing nf-core command: {e.stderr}"
    
@mcp.tool()
def install_module(module_name: str, force: bool = False, directory: str = None, sha: str = None, repository_type: str = "pipeline") -> str:
    """
    Installs an nf-core module using 'nf-core modules install'.
    
    Args:
        module_name: Name of the module to install
        force: Whether to overwrite a previously installed version of the module
        directory: Pipeline directory other than the current working directory
        sha: Install the module at a specific commit
        repository_type: Type of repository, either 'pipeline' or 'modules'
        
    Returns:
        Output of the installation command
    """
    try:
        import os
        import tempfile
        
        # Determine the working directory
        work_dir = directory if directory else os.getcwd()
        
        # Validate repository_type
        if repository_type not in ["pipeline", "modules"]:
            return "Error: repository_type must be either 'pipeline' or 'modules'"
        
        # Check if .nf-core.yml already exists
        config_path = os.path.join(work_dir, '.nf-core.yml')
        temp_config_created = False
        
        if not os.path.exists(config_path):
            # Create temporary config file with the correct format
            with open(config_path, 'w') as config_file:
                config_file.write(f'repository_type: {repository_type}\n')
            temp_config_created = True
        
        # Prepare command
        cmd = ['nf-core', 'modules', 'install']
        
        # Add command options
        if force:
            cmd.append('--force')
            
        if directory:
            cmd.extend(['--dir', directory])
            
        if sha:
            cmd.extend(['--sha', sha])
        
        # Add the module name
        cmd.append(module_name)
        
        # Execute the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Clean up temporary file if created
        if temp_config_created:
            try:
                os.remove(config_path)
            except:
                pass
            
        return result.stdout
    except FileNotFoundError:
        return "Error: 'nf-core' command not found. Make sure nf-core tools are installed and in your PATH."
    except subprocess.CalledProcessError as e:
        return f"Error executing nf-core command: {e.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def create_module(tool_name: str, directory: str = None, author: str = "@nf-core-user", label: str = "process_single", 
                 meta: bool = True, force: bool = False, conda_name: str = None, 
                 conda_package_version: str = None, empty_template: bool = False,
                 migrate_pytest: bool = False, repository_type: str = "pipeline") -> str:
    """
    Creates a new DSL2 module from the nf-core template using 'nf-core modules create'.
    
    Args:
        tool_name: Name of the tool or tool/subtool to create
        directory: Pipeline directory other than the current working directory
        author: Module author's GitHub username prefixed with '@'
        label: Standard resource label for process
        meta: Use Groovy meta map for sample information
        force: Overwrite any files if they already exist
        conda_name: Name of the conda package to use
        conda_package_version: Version of conda package to use
        empty_template: Create a module from the template without TODOs or examples
        migrate_pytest: Migrate a module with pytest tests to nf-test
        repository_type: Type of repository, either 'pipeline' or 'modules'
        
    Returns:
        Output of the creation command
    """
    try:
        import os
        import subprocess
        import re
        import tempfile
        
        # Transform tool_name to comply with nf-core naming conventions
        transformed_tool_name = re.sub(r'[^a-z0-9]', '', tool_name.lower())
        
        # Create a shell script to handle the interactive prompts
        script_content = f"""#!/bin/bash
echo y | nf-core modules create {tool_name} --force --author {author} --label {label} {'--no-meta' if not meta else ''} > /dev/null 2>&1
echo n | echo > /dev/null 2>&1
echo {'n' if not meta else 'y'} | echo > /dev/null 2>&1
exit 0
"""
        
        # Create a temporary script file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as script_file:
            script_file.write(script_content)
            script_path = script_file.name
        
        # Make the script executable
        os.chmod(script_path, 0o755)
        
        # Run the script
        subprocess.run(script_path, shell=True)
        
        # Clean up the temporary script
        os.unlink(script_path)
        
        # Check if module was created
        module_dir = os.path.join(os.getcwd(), "modules", "local", transformed_tool_name)
        if os.path.exists(module_dir):
            return f"Successfully created module: {transformed_tool_name}"
        else:
            # Direct command line approach
            cmd = f"echo -e 'y\nn\n{'n' if not meta else 'y'}' | nf-core modules create {tool_name} --force --author {author} > /dev/null 2>&1"
            subprocess.run(cmd, shell=True)
            
            # Check again
            if os.path.exists(module_dir):
                return f"Successfully created module: {transformed_tool_name}"
            else:
                return "Error: Failed to create module."
            
    except Exception as e:
        return f"Error: {str(e)}"

# Run the server
if __name__ == "__main__":
    mcp.run()