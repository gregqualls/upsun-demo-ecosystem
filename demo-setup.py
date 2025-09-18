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
        
        # Phase 3: Organization Verification
        commands.extend(self.generate_organization_verification_commands())
        
        # Phase 4: Users (handled in user invitation phase)
        
        # Phase 5: Projects
        commands.extend(self.generate_project_commands())
        
        # Phase 6: User Invitations
        commands.extend(self.generate_user_invitation_commands())
        
        # Phase 8: Environment Setup
        commands.extend(self.generate_environment_commands())
        
        # Phase 9: Domain Configuration
        commands.extend(self.generate_domain_commands())
        
        # Phase 10: SSL Certificates
        commands.extend(self.generate_certificate_commands())
        
        # Phase 11: Environment Variables
        commands.extend(self.generate_variable_commands())
        
        # Phase 12: Integrations
        commands.extend(self.generate_integration_commands())
        
        # Phase 13: Backups
        commands.extend(self.generate_backup_commands())
        
        return commands
    
    def generate_cleanup_commands(self) -> List[str]:
        """Generate all cleanup commands based on configuration."""
        commands = []
        
        # Delete all projects
        commands.append("# Phase 1: Delete all projects")
        commands.append("echo 'Deleting all projects...'")
        commands.append("upsunstg project:list --pipe | while read project_id; do")
        commands.append("  if [ ! -z \"$project_id\" ]; then")
        commands.append("    echo \"Deleting project: $project_id\"")
        commands.append("    upsunstg project:delete --project \"$project_id\" --yes")
        commands.append("  fi")
        commands.append("done")
        
        # Wait for projects to be fully deleted from system cache
        commands.append("# Phase 2: Wait for projects to be fully deleted from system cache")
        commands.append("echo 'Waiting for projects to be fully deleted from system cache...'")
        commands.append("for i in {1..5}; do")
        commands.append("  remaining_projects=$(upsunstg project:list --pipe | wc -l)")
        commands.append("  if [ \"$remaining_projects\" -eq 0 ]; then")
        commands.append("    echo 'All projects successfully deleted'")
        commands.append("    break")
        commands.append("  else")
        commands.append("    echo \"$remaining_projects projects still exist, waiting 10 seconds... (attempt $i/5)\"")
        commands.append("    sleep 10")
        commands.append("  fi")
        commands.append("done")
        
        # Delete all users (if any)
        commands.append("# Phase 3: Delete users (if any)")
        if 'users' in self.config and self.config['users']:
            for user in self.config['users']:
                commands.append(f"echo \"Deleting user {user['email']} from all projects...\"")
                commands.append("upsunstg project:list --pipe | while read project_id; do")
                commands.append(f"  if [ ! -z \"$project_id\" ]; then")
                commands.append(f"    echo \"  Removing user from project: $project_id\"")
                commands.append(f"    upsunstg user:delete \"{user['email']}\" --project \"$project_id\" --yes 2>/dev/null || echo \"    ⚠ Failed to remove user from project $project_id\"")
                commands.append("  fi")
                commands.append("done")
        else:
            commands.append("# No users to delete")
        
        # Delete all organizations
        commands.append("# Phase 4: Delete all organizations")
        commands.append("echo 'Deleting all organizations...'")
        commands.append("upsunstg organization:list --format plain --no-header | awk '{print $1}' | while read org_id; do")
        commands.append("  if [ ! -z \"$org_id\" ] && [ \"$org_id\" != \"01k4606e9hqxyxdn2ph0k06ee1\" ]; then")
        commands.append("    echo \"Deleting organization: $org_id\"")
        commands.append("    upsunstg organization:delete --org \"$org_id\" --yes")
        commands.append("  fi")
        commands.append("done")
        
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
        commands.append("# Phase 2: Create Organizations")
        commands.append("echo 'Creating organizations...'")
        
        # Check if organizations already exist by label only
        commands.append("# Check for existing organizations by label")
        commands.append("existing_orgs=$(upsunstg organization:list --format plain --no-header | awk '{for(i=2;i<=NF;i++) printf \"%s \", $i; print \"\"}' | tr '[:upper:]' '[:lower:]' | sed 's/ $//')")
        
        # Fixed organizations (use unique names to avoid conflicts)
        for org in self.config['organizations']['fixed']:
            org_label = org['label'].lower()
            commands.append(f"echo 'Checking Fixed organization: {org['label']}'")
            commands.append(f"if echo \"$existing_orgs\" | grep -q \"{org_label}\"; then")
            commands.append(f"  echo '  {org['label']} already exists, skipping'")
            commands.append("else")
            commands.append(f"  echo '  Creating {org['label']}...'")
            commands.append(f"  # Generate unique name with timestamp")
            commands.append(f"  unique_name=\"{org['name'].lower().replace(' ', '-')}-$(date +%s)\"")
            commands.append(f"  if upsunstg a:curl -X POST organizations -H \"Content-Type: application/json\" -d \"{{\\\"label\\\": \\\"{org['label']}\\\", \\\"name\\\": \\\"$unique_name\\\", \\\"type\\\": \\\"fixed\\\"}}\" 2>/dev/null; then")
            commands.append(f"    echo \"  ✓ {org['label']} created successfully with name: $unique_name\"")
            commands.append(f"    sleep 10  # Rate limiting delay after creation")
            commands.append("  else")
            commands.append(f"    echo '  ❌ Failed to create {org['label']} - stopping setup'")
            commands.append(f"    exit 1")
            commands.append("  fi")
            commands.append("fi")
        
        # Flex organizations (use unique names to avoid conflicts)
        for org in self.config['organizations']['flex']:
            org_label = org['label'].lower()
            commands.append(f"echo 'Checking Flex organization: {org['label']}'")
            commands.append(f"if echo \"$existing_orgs\" | grep -q \"{org_label}\"; then")
            commands.append(f"  echo '  {org['label']} already exists, skipping'")
            commands.append("else")
            commands.append(f"  echo '  Creating {org['label']}...'")
            commands.append(f"  # Generate unique name with timestamp")
            commands.append(f"  unique_name=\"{org['name'].lower().replace(' ', '-')}-$(date +%s)\"")
            commands.append(f"  if upsunstg organization:create --label \"{org['label']}\" --name \"$unique_name\" --yes 2>/dev/null; then")
            commands.append(f"    echo \"  ✓ {org['label']} created successfully with name: $unique_name\"")
            commands.append(f"    sleep 15  # Rate limiting delay after creation")
            commands.append("  else")
            commands.append(f"    echo '  ⚠ Failed to create {org['label']} - continuing with existing organizations'")
            commands.append("  fi")
            commands.append("fi")
        
        return commands
    
    def generate_organization_verification_commands(self) -> List[str]:
        """Generate organization verification commands."""
        commands = []
        commands.append("# Phase 3: Verify Organizations are Active")
        commands.append("echo 'Verifying organizations are active...'")
        
        # Get all organization labels from config
        org_labels = []
        if 'organizations' in self.config:
            for org in self.config['organizations'].get('fixed', []):
                org_labels.append(org['label'].lower())
            for org in self.config['organizations'].get('flex', []):
                org_labels.append(org['label'].lower())
        
        # Add verification with retry logic
        commands.append("echo 'Checking organization status...'")
        commands.append("for i in {1..3}; do")
        commands.append("  echo \"Attempt $i: Checking organizations...\"")
        commands.append("  all_active=true")
        
        for org_label in org_labels:
            commands.append(f"  if ! upsunstg organization:list --format plain --no-header | awk '{{for(i=2;i<=NF;i++) printf \"%s \", $i; print \"\"}}' | tr '[:upper:]' '[:lower:]' | grep -q \"{org_label}\"; then")
            commands.append(f"    echo \"  {org_label} not found yet\"")
            commands.append("    all_active=false")
            commands.append("  else")
            commands.append(f"    echo \"  {org_label} is active\"")
            commands.append("  fi")
        
        commands.append("  if [ \"$all_active\" = true ]; then")
        commands.append("    echo 'All organizations are active!'")
        commands.append("    break")
        commands.append("  else")
        commands.append("    echo 'Some organizations not ready, waiting 10 seconds...'")
        commands.append("    sleep 10")
        commands.append("  fi")
        commands.append("done")
        
        commands.append("echo 'Organization verification complete'")
        
        return commands
    
    
    def generate_user_commands(self) -> List[str]:
        """Generate user creation commands."""
        commands = []
        commands.append("# Note: Users will receive email invitations and must accept them")
        commands.append("# Users don't appear in user list until they accept invitations")
        
        if 'users' in self.config and self.config['users']:
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
        else:
            commands.append("# No users configured - current logged-in user will have access")
        return commands
    
    def generate_user_invitation_commands(self) -> List[str]:
        """Generate user invitation commands."""
        commands = []
        commands.append("# Phase 4: Invite Users")
        commands.append("echo 'Inviting users to organizations and projects...'")
        
        if 'users' in self.config and self.config['users']:
            for user in self.config['users']:
                commands.append(f"echo 'Inviting {user['name']} ({user['email']})...'")
                
                # Get all organization IDs
                commands.append("# Get all organization IDs")
                commands.append("org_ids=$(upsunstg organization:list --format plain --no-header | awk '{print $1}')")
                
                # Invite to all organizations
                commands.append("# Invite to all organizations")
                commands.append("for org_id in $org_ids; do")
                commands.append(f"  echo '  Inviting to organization: $org_id'")
                commands.append(f"  upsunstg organization:user:add --org \"$org_id\" --email \"{user['email']}\" --role developer --yes 2>/dev/null || echo '    ⚠ Failed to invite to org $org_id'")
                commands.append("done")
                
                # Get all project IDs
                commands.append("# Get all project IDs")
                commands.append("project_ids=$(upsunstg project:list --pipe)")
                
                # Invite to all projects
                commands.append("# Invite to all projects")
                commands.append("for project_id in $project_ids; do")
                commands.append(f"  echo '  Inviting to project: $project_id'")
                commands.append(f"  upsunstg project:user:add --project \"$project_id\" --email \"{user['email']}\" --role developer --yes 2>/dev/null || echo '    ⚠ Failed to invite to project $project_id'")
                commands.append("done")
                
                commands.append(f"echo '✓ User {user['name']} invitation process completed'")
        else:
            commands.append("# No users configured for invitation")
        
        return commands
    
    def generate_project_commands(self) -> List[str]:
        """Generate project creation commands."""
        commands = []
        if 'projects' in self.config and self.config['projects']:
            commands.append("# Phase 6: Create Projects")
            commands.append("echo 'Creating projects...'")
            
            for project in self.config['projects']:
                org_name = project['organization'].lower().replace(' ', '-')
                org_label = project['organization'].replace('bmc-', 'BMC ').title()
                project_title = project['title']
                commands.append(f"echo 'Checking project: {project_title} in {org_label}'")
                
                # Check if project already exists
                commands.append(f"if upsunstg project:list --format plain --no-header | grep -q \"{project_title}\"; then")
                commands.append(f"  echo '  {project_title} already exists, skipping'")
                commands.append("else")
                commands.append(f"  echo '  Creating {project_title}...'")
                commands.append(f"  # Get organization ID by label")
                commands.append(f"  org_id=$(upsunstg organization:list --format plain --no-header | grep -i \"{org_label}\" | head -1 | awk '{{print $1}}')")
                commands.append(f"  if [ -z \"$org_id\" ]; then")
                commands.append(f"    echo \"Error: Organization {org_label} not found\"")
                commands.append(f"    exit 1")
                commands.append(f"  fi")
                
                if project.get('source', {}).get('type') == 'github':
                    # For GitHub projects, use the repository URL
                    repo_url = project['source']['repository']
                    if 'path' in project['source']:
                        # For repositories with subdirectories, note that manual setup may be required
                        commands.append(f"    upsunstg project:create --title \"{project['title']}\" --org \"$org_id\" --region \"plc.recreation.plat.farm\" --init-repo \"{repo_url}\" --yes")
                        commands.append(f"    # Note: This project uses a subdirectory ({project['source']['path']}) - manual configuration may be required")
                    else:
                        commands.append(f"    upsunstg project:create --title \"{project['title']}\" --org \"$org_id\" --region \"plc.recreation.plat.farm\" --init-repo \"{repo_url}\" --yes")
                else:
                    # For local projects, create without init-repo
                    commands.append(f"    upsunstg project:create --title \"{project['title']}\" --org \"$org_id\" --region \"plc.recreation.plat.farm\" --yes")
                    commands.append(f"    # Note: Local project {project['name']} will need to be connected manually")
                
                commands.append("fi")
        else:
            commands.append("# No projects configured")
        
        return commands
    
    
    def generate_environment_commands(self) -> List[str]:
        """Generate environment setup commands."""
        commands = []
        commands.append("# Note: Environment commands disabled - projects are created with production environment by default")
        commands.append("# To create additional environments, use the Upsun console or CLI manually")
        # if 'projects' in self.config and self.config['projects']:
        #     for project in self.config['projects']:
        #         for env in project['environments']:
        #             if env == 'production':
        #                 commands.append(f"upsunstg environment:activate --project {project['name']} --environment production")
        #             else:
        #                 commands.append(f"upsunstg environment:branch --project {project['name']} --environment {env}")
        # else:
        #     commands.append("# No projects configured")
        return commands
    
    def generate_domain_commands(self) -> List[str]:
        """Generate domain configuration commands."""
        commands = []
        commands.append("# Note: Domain commands disabled - configure domains manually in Upsun console")
        commands.append("# To add domains, use: upsunstg domain:add <domain-name> --project <project-id>")
        # if 'projects' in self.config and self.config['projects']:
        #     for project in self.config['projects']:
        #         if 'domains' in project:
        #             for env, domains in project['domains'].items():
        #                 for domain in domains:
        #                     commands.append(f"upsunstg domain:add --project {project['name']} --domain {domain}")
        # else:
        #     commands.append("# No projects configured")
        return commands
    
    def generate_certificate_commands(self) -> List[str]:
        """Generate SSL certificate commands."""
        commands = []
        commands.append("# Note: Certificate commands disabled - configure SSL certificates manually in Upsun console")
        commands.append("# To add certificates, use: upsunstg certificate:add <cert-name> --project <project-id>")
        # if 'projects' in self.config and self.config['projects']:
        #     for project in self.config['projects']:
        #         if 'domains' in project and 'production' in project['domains']:
        #             for domain in project['domains']['production']:
        #                 cert_name = domain.replace('.', '-')
        #                 commands.append(f"upsunstg certificate:add --project {project['name']} --certificate-file {cert_name}.crt --key-file {cert_name}.key")
        # else:
        #     commands.append("# No projects configured")
        return commands
    
    def generate_variable_commands(self) -> List[str]:
        """Generate environment variable commands."""
        commands = []
        commands.append("# Note: Variable commands disabled - configure environment variables manually in Upsun console")
        commands.append("# To add variables, use: upsunstg variable:create --project <project-id> --name <var-name> --value <var-value>")
        # if 'projects' in self.config and self.config['projects']:
        #     for project in self.config['projects']:
        #         # Global variables
        #         if 'environment_variables' in self.config and 'global' in self.config['environment_variables']:
        #             for key, value in self.config['environment_variables']['global'].items():
        #                 commands.append(f"upsunstg variable:create --project {project['name']} --name {key} --value \"{value}\"")
        #         
        #         # Environment-specific variables
        #         for env in project['environments']:
        #             if 'environment_variables' in self.config and env in self.config['environment_variables']:
        #                 for key, value in self.config['environment_variables'][env].items():
        #                     commands.append(f"upsunstg variable:create --project {project['name']} --environment {env} --name {key} --value \"{value}\"")
        # else:
        #     commands.append("# No projects configured")
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
        commands.append("# Note: Backup commands disabled - create backups manually in Upsun console")
        commands.append("# To create backups, use: upsunstg backup:create --project <project-id> --environment <env>")
        # if 'projects' in self.config and self.config['projects']:
        #     for project in self.config['projects']:
        #         commands.append(f"upsunstg backup:create --project {project['name']} --environment production")
        # else:
        #     commands.append("# No projects configured")
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
            
            for command in commands:
                f.write(f"{command}\n")
        
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
