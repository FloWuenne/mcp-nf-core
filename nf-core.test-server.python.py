import subprocess
from mcp.server.fastmcp import FastMCP
from typing import Optional
import sys
from pathlib import Path

# Import the correct module creation class
from nf_core.modules.create import ModuleCreate

# Initialize the server
mcp = FastMCP("nf-core-mcp-python")

@mcp.tool()
def create_module(
    tool_name: str,
    directory: Optional[str] = None,
    author: str = "@nf-core-user",
    label: str = "process_single",
    meta: bool = True,
    force: bool = False,
    conda_name: Optional[str] = None,
    conda_package_version: Optional[str] = None,
    empty_template: bool = False,
    migrate_pytest: bool = False,
):
    """
    Creates a new DSL2 module from the nf-core template.
    
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
        
    Returns:
        Output of the creation command
    """
    try:
        # Convert directory to Path if provided
        dir_path = Path(directory) if directory else Path(".")
        
        # Create the module using the ModuleCreate class
        module_creator = ModuleCreate(
            directory=dir_path,
            module=tool_name,
            author=author,
            process_label=label,
            has_meta=meta,
            force=force,
            conda_name=conda_name,
            conda_version=conda_package_version,
            empty_template=empty_template,
            migrate_pytest=migrate_pytest,
        )
        
        # This will create the module and handle all the necessary steps
        module_creator.create()
        
        return f"Successfully created module: {tool_name}"
    except Exception as e:
        return f"Error creating module: {str(e)}"

# Run the server
if __name__ == "__main__":
    mcp.run()