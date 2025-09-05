# Upsun Demo Ecosystem Generator

A configuration-driven system for creating and managing complete demo ecosystems in Upsun. This tool generates executable shell scripts from JSON configuration files, making it easy to set up realistic demo environments with organizations, projects, and users.

## How It Works

1. **Configure**: Edit a JSON file to define your demo ecosystem
2. **Generate**: Run the Python script to create executable shell scripts
3. **Execute**: Run the generated scripts to create/delete your demo environment
4. **Cleanup**: Use the cleanup script to remove everything when done

## Files

- `setup-demo.sh` - **One-command setup script** with prerequisites check and progress indicators
- `cleanup-demo.sh` - **Complete cleanup script** that removes all projects and organizations
- `demo-setup.py` - Main Python script that generates CLI commands from JSON configuration
- `demo-config.json` - Complete BMC Global Group Inc. yacht industry demo configuration
- `example-config.json` - Example configuration with detailed documentation
- `final-test-config.json` - Tested configuration with real GitHub repositories
- `clilist.md` - Reference of available Upsun CLI commands

## Quick Start

### 🚀 One-Command Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/gregqualls/upsun-demo-ecosystem.git
cd upsun-demo-ecosystem

# Run the yacht industry demo (includes all prerequisites checks)
./setup-demo.sh

# Clean up when done
./cleanup-demo.sh
```

### 📋 Prerequisites

The setup script will check for these automatically:
- Python 3.6+
- Upsun Staging CLI (`upsunstg`) installed and authenticated
- Access to Upsun staging environment
- Git (for GitHub repository projects)

### 🔧 Manual Setup (Advanced)

If you prefer to run the components manually:

```bash
# 1. Authenticate with Upsun
upsunstg auth:browser-login

# 2. Generate and run setup script
python3 demo-setup.py --config demo-config.json --action setup
chmod +x setup-demo-ecosystem.sh
./setup-demo-ecosystem.sh

# 3. Clean up when done
python3 demo-setup.py --config demo-config.json --action cleanup
chmod +x cleanup-demo-ecosystem.sh
./cleanup-demo-ecosystem.sh
```

## Typical Workflow

1. **Plan your demo**: Decide what organizations, projects, and users you need
2. **Create configuration**: Copy `example-config.json` and customize it
3. **Test small**: Start with 1-2 organizations to verify everything works
4. **Generate scripts**: Run `python3 demo-setup.py --config your-config.json`
5. **Execute setup**: Run `./setup-demo-ecosystem.sh` to create your demo
6. **Verify creation**: Check `upsunstg organization:list` and `upsunstg project:list`
7. **Run your demo**: Use the created environment for demonstrations
8. **Clean up**: Run `./cleanup-demo-ecosystem.sh` when finished

## Configuration Structure

### Organizations
- **Fixed Organizations**: For monolithic applications (CMS, e-commerce)
  - Created with: `upsunstg a:curl -X POST organizations -H "Content-Type: application/json" -d '{"label": "org-name", "type": "fixed"}'`
  - Provide set resource levels applied automatically to containers
- **Flex Organizations**: For microservices and custom applications
  - Created with: `upsunstg organization:create --label "org-name" --name "org-name" --yes`
  - Offer granular control over resources at container level

### Projects
Each project includes:
- **Name and title**: Project identifier and display name
- **Organization**: Which organization owns the project
- **Source**: Either local directory path or GitHub repository URL
- **Region**: Deployment region (default: `bk3.recreation.plat.farm` for staging)

### Users
- **Email addresses**: Must be valid email addresses
- **Roles**: `admin` (full access) or `viewer` (read-only access)
- **Environment roles**: Non-admin users get `production:viewer` role
- **Invitations**: Users receive email invitations and must accept them

### Teams
- **Note**: Teams are not supported in the Upsun staging environment
- **Workaround**: Users are assigned directly to projects

## Best Practices

### 1. Configuration Management
- **Start with examples**: Use `example-config.json` or `final-test-config.json` as templates
- **Test incrementally**: Start with 1-2 organizations and projects before scaling up
- **Validate JSON**: Use `python3 -m json.tool your-config.json` to check syntax
- **Version control**: Keep configuration files in version control for reproducibility

### 2. Project Sources
- **GitHub repositories**: Use for production-ready templates with Upsun configuration
- **Local directories**: Use for custom projects (requires manual connection after creation)
- **Subdirectories**: GitHub repos with subdirectories may need manual configuration

### 3. User Management
- **Email invitations**: Users must accept email invitations before they appear in user lists
- **Role assignment**: Admin users get full access, others get `production:viewer`
- **Project assignment**: Users are assigned to the first project in the configuration

### 4. Organization Types
- **Fixed Organizations**: Best for CMS, e-commerce, monolithic applications
- **Flex Organizations**: Best for microservices, custom applications, API services
- **Naming**: Use lowercase with hyphens for organization names (e.g., `bmc-development-labs`)

### 5. Testing Strategy
- **Small scale first**: Test with 1-2 organizations before full ecosystem
- **Verify cleanup**: Always test cleanup scripts to ensure complete removal
- **Check status**: Use `upsunstg organization:list` and `upsunstg project:list` to verify
- **Robust cleanup**: Script handles fake names in config vs real project titles

## Customization Examples

### Adding a New Project

```json
{
  "name": "new-project",
  "title": "New Project",
  "description": "Description of the new project",
  "organization": "bmc-development-labs",
  "source": {
    "type": "github",
    "repository": "https://github.com/your-org/your-repo",
    "path": "optional/subdirectory"
  }
}
```

### Adding a Local Project

```json
{
  "name": "local-project",
  "title": "Local Project",
  "description": "Project with local source code",
  "organization": "bmc-development-labs",
  "source": {
    "type": "local",
    "path": "./projects/local-project"
  }
}
```

### Adding a New User

```json
{
  "email": "new.user@bmcglobalgroup.com",
  "role": "viewer",
  "first_name": "New",
  "last_name": "User",
  "title": "Developer"
}
```

## Common Issues & Solutions

### Organization Creation Fails
- **Fixed orgs**: Use the special `a:curl` command format
- **Flex orgs**: Use standard `organization:create` with `--yes` flag
- **Duplicate names**: Check existing organizations with `upsunstg organization:list`

### Project Creation Issues
- **Invalid region**: Use `bk3.recreation.plat.farm` for staging environment
- **Organization restricted**: New organizations may be in "restricted" status initially
- **GitHub subdirectories**: May require manual configuration after creation

### User Management Problems
- **Users not appearing**: They must accept email invitations first
- **Invalid roles**: Use only `admin` or `viewer` roles
- **Environment roles**: Non-admin users need `production:viewer` role

### Cleanup Issues
- **Project deletion**: Script automatically uses project IDs from `upsunstg project:list --pipe`
- **Organization deletion**: Script automatically uses organization IDs from `upsunstg organization:list`
- **User deletion**: Only works for users who have accepted invitations
- **Complete cleanup**: Script removes all projects first, then all organizations

## Benefits

1. **Reusable**: Easy to modify and reuse for different demos
2. **Maintainable**: All configuration in one JSON file
3. **Flexible**: Easy to add/remove organizations, projects, users
4. **Version Controlled**: Track changes to demo configurations
5. **Automated**: Generate all CLI commands automatically
6. **Safe**: Includes complete cleanup procedures
7. **Tested**: Based on real-world testing with Upsun staging environment
8. **Ready-to-use**: Includes complete yacht industry demo with 16 projects

## Troubleshooting

### Authentication Issues
```bash
# Check authentication status
upsunstg auth:info

# Login if needed
upsunstg auth:browser-login
```

### Configuration Validation
```bash
# Validate JSON syntax
python3 -m json.tool your-config.json

# Test with small configuration first
python3 demo-setup.py --config test-config.json
```

### Debugging Commands
```bash
# List current organizations
upsunstg organization:list

# List current projects
upsunstg project:list

# Check project details
upsunstg project:info --project PROJECT_ID
```

## Support

For issues or questions:
1. Check the generated shell scripts for errors
2. Verify Upsun CLI commands are correct
3. Review the configuration file for syntax errors
4. Test with a small subset of resources first
5. Check the `clilist.md` for available commands
6. Use `upsunstg help COMMAND` for specific command help
