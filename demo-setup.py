#!/usr/bin/env python3
"""
Upsun Demo Ecosystem Setup Script

This script reads the demo-config.json file and generates CLI commands
for setting up and tearing down a demo ecosystem.
"""

import json
import os
import sys
import argparse
from typing import Dict, List, Any

class DemoEcosystemManager:
    def __init__(self, config_file: str = "demo-config.json"):
        """Initialize the demo ecosystem manager with configuration."""
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file '{self.config_file}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in configuration file: {e}")
            sys.exit(1)
    
    def _get_default_org(self) -> str:
        """Get the first available organization name."""
        if self.config['organizations']['flex']:
            return self.config['organizations']['flex'][0]['name'].lower().replace(' ', '-')
        elif self.config['organizations']['fixed']:
            return self.config['organizations']['fixed'][0]['name'].lower().replace(' ', '-')
        return "default-org"
    
    def generate_setup_commands(self) -> List[str]:
        """Generate all setup commands based on configuration."""
        commands = []
        
        # Phase 1: Authentication & Initial Setup
        commands.extend(self.generate_auth_commands())
        
        # Phase 2: Organizations
        commands.extend(self.generate_organization_commands())
        
        # Phase 3: Teams
        commands.extend(self.generate_team_commands())
        
        # Phase 4: Users
        commands.extend(self.generate_user_commands())
        
        # Phase 5: Projects
        commands.extend(self.generate_project_commands())
        
        # Phase 6: Team-Project Assignments
        commands.extend(self.generate_team_project_assignments())
        
        # Phase 7: Environment Setup
        commands.extend(self.generate_environment_commands())
        
        # Phase 8: Domain Configuration
        commands.extend(self.generate_domain_commands())
        
        # Phase 9: SSL Certificates
        commands.extend(self.generate_certificate_commands())
        
        # Phase 10: Environment Variables
        commands.extend(self.generate_variable_commands())
        
        
        # Phase 11: Integrations
        commands.extend(self.generate_integration_commands())
        
        # Phase 12: Backups
        commands.extend(self.generate_backup_commands())
        
        return commands
    
    def generate_cleanup_commands(self) -> List[str]:
        """Generate all cleanup commands based on configuration."""
        commands = []
        
        # Delete all projects
        for project in self.config['projects']:
            commands.append(f"upsunstg project:delete --project {project['name']} --yes")
        
        # Delete all teams
        commands.append("# Note: Teams may not be available in staging environment")
        for team in self.config['teams']:
            commands.append(f"upsunstg team:delete --team \"{team['name']}\" --yes")
        
        # Delete all users
        for user in self.config['users']:
            if 'projects' in self.config and self.config['projects']:
                project_id = self.config['projects'][0]['name']
                commands.append(f"upsunstg user:delete \"{user['email']}\" --project \"{project_id}\" --yes")
            else:
                commands.append(f"# No projects available for user deletion {user['email']}")
        
        # Delete all organizations (both fixed and flex use the same delete command)
        for org in self.config['organizations']['fixed'] + self.config['organizations']['flex']:
            org_name = org['name'].lower().replace(' ', '-')
            commands.append(f"upsunstg organization:delete --org {org_name} --yes")
        
        return commands
    
    def generate_auth_commands(self) -> List[str]:
        """Generate authentication commands."""
        return [
            "# Note: User should already be logged in to Upsun",
            "# If not logged in, run: upsunstg auth:browser-login",
            "upsunstg auth:info"
        ]
    
    def generate_organization_commands(self) -> List[str]:
        """Generate organization creation commands."""
        commands = []
        
        # Fixed organizations
        for org in self.config['organizations']['fixed']:
            org_name = org['name'].lower().replace(' ', '-')
            if org['type'] == 'fixed':
                commands.append(f'upsunstg a:curl -X POST organizations -H "Content-Type: application/json" -d \'{{"label": "{org["label"]}", "type": "fixed"}}\'')
            else:
                commands.append(f"upsunstg organization:create --label \"{org['label']}\" --name \"{org_name}\" --yes")
        
        # Flex organizations
        for org in self.config['organizations']['flex']:
            org_name = org['name'].lower().replace(' ', '-')
            commands.append(f"upsunstg organization:create --label \"{org['label']}\" --name \"{org_name}\" --yes")
        
        return commands
    
    def generate_team_commands(self) -> List[str]:
        """Generate team creation commands."""
        commands = []
        # Note: Teams may not be available in all environments (e.g., staging)
        # Check if teams are supported before running these commands
        commands.append("# Note: Teams may not be available in staging environment")
        commands.append("# Check team support with: upsunstg team:list")
        for team in self.config['teams']:
            commands.append(f"upsunstg team:create --label \"{team['title']}\" --org \"{self._get_default_org()}\" --yes")
        return commands
    
    def generate_user_commands(self) -> List[str]:
        """Generate user creation commands."""
        commands = []
        commands.append("# Note: Users will receive email invitations and must accept them")
        commands.append("# Users don't appear in user list until they accept invitations")
        
        for user in self.config['users']:
            # Get the first project for user assignment
            if 'projects' in self.config and self.config['projects']:
                project_id = self.config['projects'][0]['name']
                if user['role'] == 'admin':
                    commands.append(f"upsunstg user:add \"{user['email']}\" --role \"{user['role']}\" --project \"{project_id}\" --yes")
                else:
                    # Non-admin users need environment-specific roles
                    commands.append(f"upsunstg user:add \"{user['email']}\" --role \"production:{user['role']}\" --project \"{project_id}\" --yes")
            else:
                commands.append(f"# No projects available for user {user['email']}")
        return commands
    
    def generate_project_commands(self) -> List[str]:
        """Generate project creation commands."""
        commands = []
        if 'projects' in self.config and self.config['projects']:
            for project in self.config['projects']:
                org_name = project['organization'].lower().replace(' ', '-')
                
                if project.get('source', {}).get('type') == 'github':
                    # For GitHub projects, use the repository URL
                    repo_url = project['source']['repository']
                    if 'path' in project['source']:
                        # For repositories with subdirectories, note that manual setup may be required
                        commands.append(f"upsunstg project:create --title \"{project['title']}\" --org \"{org_name}\" --region \"bk3.recreation.plat.farm\" --init-repo \"{repo_url}\" --yes")
                        commands.append(f"# Note: This project uses a subdirectory ({project['source']['path']}) - manual configuration may be required")
                    else:
                        commands.append(f"upsunstg project:create --title \"{project['title']}\" --org \"{org_name}\" --region \"bk3.recreation.plat.farm\" --init-repo \"{repo_url}\" --yes")
                else:
                    # For local projects, create without init-repo
                    commands.append(f"upsunstg project:create --title \"{project['title']}\" --org \"{org_name}\" --region \"bk3.recreation.plat.farm\" --yes")
                    commands.append(f"# Note: Local project {project['name']} will need to be connected manually")
        else:
            commands.append("# No projects configured")
        
        return commands
    
    def generate_team_project_assignments(self) -> List[str]:
        """Generate team-project assignment commands."""
        commands = []
        
        # Note: Teams may not be available in staging environment
        commands.append("# Note: Teams may not be available in staging environment")
        commands.append("# Check team support with: upsunstg team:list")
        
        # Assign projects to teams
        if 'projects' in self.config and self.config['projects']:
            for project in self.config['projects']:
                if 'team' in project:
                    commands.append(f"upsunstg team:project:add --team \"{project['team']}\" --project \"{project['name']}\" --yes")
        
        # Assign users to teams
        for user in self.config['users']:
            if 'team' in user:
                commands.append(f"upsunstg team:user:add --team \"{user['team']}\" --user \"{user['email']}\" --yes")
        
        return commands
    
    def generate_environment_commands(self) -> List[str]:
        """Generate environment setup commands."""
        commands = []
        if 'projects' in self.config and self.config['projects']:
            for project in self.config['projects']:
                for env in project['environments']:
                    if env == 'production':
                        commands.append(f"upsunstg environment:activate --project {project['name']} --environment production")
                    else:
                        commands.append(f"upsunstg environment:branch --project {project['name']} --environment {env}")
        else:
            commands.append("# No projects configured")
        return commands
    
    def generate_domain_commands(self) -> List[str]:
        """Generate domain configuration commands."""
        commands = []
        if 'projects' in self.config and self.config['projects']:
            for project in self.config['projects']:
                if 'domains' in project:
                    for env, domains in project['domains'].items():
                        for domain in domains:
                            commands.append(f"upsunstg domain:add --project {project['name']} --domain {domain}")
        else:
            commands.append("# No projects configured")
        return commands
    
    def generate_certificate_commands(self) -> List[str]:
        """Generate SSL certificate commands."""
        commands = []
        if 'projects' in self.config and self.config['projects']:
            for project in self.config['projects']:
                if 'domains' in project and 'production' in project['domains']:
                    for domain in project['domains']['production']:
                        cert_name = domain.replace('.', '-')
                        commands.append(f"upsunstg certificate:add --project {project['name']} --certificate-file {cert_name}.crt --key-file {cert_name}.key")
        else:
            commands.append("# No projects configured")
        return commands
    
    def generate_variable_commands(self) -> List[str]:
        """Generate environment variable commands."""
        commands = []
        if 'projects' in self.config and self.config['projects']:
            for project in self.config['projects']:
                # Global variables
                if 'environment_variables' in self.config and 'global' in self.config['environment_variables']:
                    for key, value in self.config['environment_variables']['global'].items():
                        commands.append(f"upsunstg variable:create --project {project['name']} --name {key} --value \"{value}\"")
                
                # Environment-specific variables
                for env in project['environments']:
                    if 'environment_variables' in self.config and env in self.config['environment_variables']:
                        for key, value in self.config['environment_variables'][env].items():
                            commands.append(f"upsunstg variable:create --project {project['name']} --environment {env} --name {key} --value \"{value}\"")
        else:
            commands.append("# No projects configured")
        return commands
    
    
    def generate_integration_commands(self) -> List[str]:
        """Generate integration commands."""
        commands = []
        if 'projects' in self.config and self.config['projects']:
            for project in self.config['projects']:
                if 'integrations' in self.config:
                    for integration in self.config['integrations']:
                        if integration['type'] == 'github':
                            commands.append(f"upsunstg integration:add --project {project['name']} --type github --repository bmc-global/{project['name']}")
                        elif integration['type'] in ['newrelic', 'datadog']:
                            commands.append(f"upsunstg integration:add --project {project['name']} --type {integration['type']} --api-key \"your-{integration['type']}-key\"")
        else:
            commands.append("# No projects configured")
        return commands
    
    def generate_backup_commands(self) -> List[str]:
        """Generate backup commands."""
        commands = []
        if 'projects' in self.config and self.config['projects']:
            for project in self.config['projects']:
                commands.append(f"upsunstg backup:create --project {project['name']} --environment production")
        else:
            commands.append("# No projects configured")
        return commands
    
    def create_local_directories(self) -> List[str]:
        """Create local project directories."""
        commands = []
        for project in self.config['projects']:
            if 'local_directory' in project:
                commands.append(f"mkdir -p {project['local_directory']}")
        return commands
    
    def save_commands_to_file(self, commands: List[str], filename: str):
        """Save commands to a shell script file."""
        with open(filename, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# BMC Global Group Inc. - Upsun Demo Ecosystem Commands\n")
            f.write("# Generated from demo-config.json\n\n")
            f.write("set -e  # Exit on any error\n\n")
            
            for i, command in enumerate(commands, 1):
                f.write(f"# Step {i}\n")
                f.write(f"{command}\n")
                f.write("echo \"✓ Completed: {}\"\n\n".format(command))
        
        # Make the file executable
        os.chmod(filename, 0o755)
        print(f"Commands saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='BMC Global Group Inc. - Upsun Demo Ecosystem Manager')
    parser.add_argument('--config', default='demo-config.json', help='Configuration file path')
    parser.add_argument('--action', choices=['setup', 'cleanup', 'both'], default='both', help='Action to perform')
    parser.add_argument('--output', help='Output file for generated commands')
    parser.add_argument('--create-dirs', action='store_true', help='Create local project directories')
    
    args = parser.parse_args()
    
    manager = DemoEcosystemManager(args.config)
    
    if args.action in ['setup', 'both']:
        print("Generating setup commands...")
        setup_commands = manager.generate_setup_commands()
        
        if args.create_dirs:
            setup_commands = manager.create_local_directories() + setup_commands
        
        if args.output:
            manager.save_commands_to_file(setup_commands, args.output)
        else:
            manager.save_commands_to_file(setup_commands, 'setup-demo-ecosystem.sh')
    
    if args.action in ['cleanup', 'both']:
        print("Generating cleanup commands...")
        cleanup_commands = manager.generate_cleanup_commands()
        
        if args.output:
            cleanup_filename = args.output.replace('.sh', '-cleanup.sh')
        else:
            cleanup_filename = 'cleanup-demo-ecosystem.sh'
        
        manager.save_commands_to_file(cleanup_commands, cleanup_filename)
    
    print("Done! Generated command files are ready to execute.")

if __name__ == "__main__":
    main()
