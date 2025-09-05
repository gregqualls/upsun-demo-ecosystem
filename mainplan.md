# BMC Global Group Inc. - Upsun Demo Ecosystem Setup Plan

## Overview
This plan outlines the step-by-step process to create a realistic demo ecosystem for BMC Global Group Inc., a holding company that manages multiple technology subsidiaries. The ecosystem will include multiple organizations (Fixed and Flex billing entities), projects, and a small but efficient development team to demonstrate various Upsun platform capabilities.

## Configuration-Driven Approach

**NEW**: This plan now uses a configuration-driven approach with `demo-config.json` and `demo-setup.py`. See the README.md for the modern, automated setup process.

The configuration file contains all organizations, projects, users, and settings, making it easy to customize and reuse for different demos.

## Company Profile: BMC Global Group Inc.
- **Industry**: Technology Holding Company
- **Size**: Small to medium enterprise (50-100 employees)
- **Structure**: Holding company with multiple subsidiary billing entities
- **Focus**: Managing technology investments, cloud infrastructure, and software solutions across subsidiaries

## Phase 1: Authentication & Initial Setup

### 1.1 Authentication
- [ ] Login to Upsun staging environment
  ```bash
  upsunstg auth:browser-login
  ```
- [ ] Verify authentication status
  ```bash
  upsunstg auth:info
  ```

### 1.2 SSH Key Setup
- [ ] Add SSH key for secure access
  ```bash
  upsunstg ssh-key:add
  ```
- [ ] Verify SSH keys
  ```bash
  upsunstg ssh-key:list
  ```

## Phase 2: Organization Structure (Billing Entities)

### 2.1 Fixed Organizations (Monolithic Applications)
- [ ] Create "BMC Global Group Inc." (Main holding company - Fixed)
  ```bash
  upsunstg a:curl -X POST organizations -H "Content-Type: application/json" -d '{"label": "BMC Global Group Inc.", "type": "fixed"}'
  ```
- [ ] Create "BMC E-commerce Platform" (E-commerce site - Fixed)
  ```bash
  upsunstg a:curl -X POST organizations -H "Content-Type: application/json" -d '{"label": "BMC E-commerce Platform", "type": "fixed"}'
  ```
- [ ] Create "BMC Content Management" (CMS platform - Fixed)
  ```bash
  upsunstg a:curl -X POST organizations -H "Content-Type: application/json" -d '{"label": "BMC Content Management", "type": "fixed"}'
  ```

### 2.2 Flex Organizations (Microservices & Custom Applications)
- [ ] Create "BMC Development Labs" (R&D division - Flex)
  ```bash
  upsunstg organization:create --title "BMC Development Labs" --name "bmc-development-labs"
  ```
- [ ] Create "BMC Client Projects" (Client work division - Flex)
  ```bash
  upsunstg organization:create --title "BMC Client Projects" --name "bmc-client-projects"
  ```

### 2.3 Organization Configuration
- [ ] Set billing addresses for each organization
  ```bash
  upsunstg organization:billing:address --organization bmc-global-group
  upsunstg organization:billing:address --organization bmc-ecommerce-platform
  upsunstg organization:billing:address --organization bmc-content-management
  upsunstg organization:billing:address --organization bmc-development-labs
  upsunstg organization:billing:address --organization bmc-client-projects
  ```

## Phase 3: Team Structure (Upsun Handles Infrastructure)

### 3.1 Development Team
- [ ] Create "Full-Stack Development" team (handles all development work)
  ```bash
  upsunstg team:create --title "Full-Stack Development" --name "fullstack-dev"
  ```

### 3.2 Business & Support Teams
- [ ] Create "Executive & Management" team
  ```bash
  upsunstg team:create --title "Executive & Management" --name "executive-mgmt"
  ```
- [ ] Create "Finance & Billing" team
  ```bash
  upsunstg team:create --title "Finance & Billing" --name "finance-billing"
  ```

## Phase 4: User Management (Small Team)

### 4.1 Executive & Management Users
- [ ] Create CEO: Sarah Johnson
  ```bash
  upsunstg user:add --email sarah.johnson@bmcglobalgroup.com --role admin
  ```
- [ ] Create CTO: Michael Chen
  ```bash
  upsunstg user:add --email michael.chen@bmcglobalgroup.com --role admin
  ```

### 4.2 Development Team Users
- [ ] Create Lead Developer: Alex Thompson
  ```bash
  upsunstg user:add --email alex.thompson@bmcglobalgroup.com --role contributor
  ```
- [ ] Create Senior Developer: David Kim
  ```bash
  upsunstg user:add --email david.kim@bmcglobalgroup.com --role contributor
  ```
- [ ] Create Full-Stack Developer: Jennifer Martinez
  ```bash
  upsunstg user:add --email jennifer.martinez@bmcglobalgroup.com --role contributor
  ```
- [ ] Create Junior Developer: Robert Wilson
  ```bash
  upsunstg user:add --email robert.wilson@bmcglobalgroup.com --role contributor
  ```

### 4.3 Business & Support Users
- [ ] Create Finance Manager: Amanda Davis
  ```bash
  upsunstg user:add --email amanda.davis@bmcglobalgroup.com --role viewer
  ```
- [ ] Create Operations Manager: Kevin Lee
  ```bash
  upsunstg user:add --email kevin.lee@bmcglobalgroup.com --role viewer
  ```

## Phase 5: Project Creation (Focused Portfolio)

### 5.1 Monolithic Applications (Fixed Organizations)
- [ ] Create "BMC Corporate Website" project (BMC Global Group Inc.)
  ```bash
  upsunstg project:create --title "BMC Corporate Website" --name "bmc-corporate-website"
  ```
- [ ] Create "BMC E-commerce Store" project (BMC E-commerce Platform)
  ```bash
  upsunstg project:create --title "BMC E-commerce Store" --name "bmc-ecommerce-store"
  ```
- [ ] Create "BMC CMS Platform" project (BMC Content Management)
  ```bash
  upsunstg project:create --title "BMC CMS Platform" --name "bmc-cms-platform"
  ```

### 5.2 Microservices & Custom Applications (Flex Organizations)
- [ ] Create "BMC API Services" project (BMC Development Labs)
  ```bash
  upsunstg project:create --title "BMC API Services" --name "bmc-api-services"
  ```
- [ ] Create "Client Project Alpha" project (BMC Client Projects)
  ```bash
  upsunstg project:create --title "Client Project Alpha" --name "client-project-alpha"
  ```
- [ ] Create "Client Project Beta" project (BMC Client Projects)
  ```bash
  upsunstg project:create --title "Client Project Beta" --name "client-project-beta"
  ```

### 5.3 Shared Services Projects
- [ ] Create "BMC Analytics Dashboard" project
  ```bash
  upsunstg project:create --title "BMC Analytics Dashboard" --name "bmc-analytics-dashboard"
  ```

## Phase 6: Team-Project Assignments

### 6.1 Assign Projects to Teams
- [ ] Assign all projects to Full-Stack Development team (Upsun handles infrastructure)
  ```bash
  upsunstg team:project:add --team fullstack-dev --project bmc-corporate-website
  upsunstg team:project:add --team fullstack-dev --project bmc-ecommerce-store
  upsunstg team:project:add --team fullstack-dev --project bmc-cms-platform
  upsunstg team:project:add --team fullstack-dev --project bmc-api-services
  upsunstg team:project:add --team fullstack-dev --project client-project-alpha
  upsunstg team:project:add --team fullstack-dev --project client-project-beta
  upsunstg team:project:add --team fullstack-dev --project bmc-analytics-dashboard
  ```

### 6.2 Assign Users to Teams
- [ ] Add executive users to Executive & Management team
  ```bash
  upsunstg team:user:add --team executive-mgmt --user sarah.johnson@bmcglobalgroup.com
  upsunstg team:user:add --team executive-mgmt --user michael.chen@bmcglobalgroup.com
  ```
- [ ] Add developers to Full-Stack Development team
  ```bash
  upsunstg team:user:add --team fullstack-dev --user alex.thompson@bmcglobalgroup.com
  upsunstg team:user:add --team fullstack-dev --user david.kim@bmcglobalgroup.com
  upsunstg team:user:add --team fullstack-dev --user jennifer.martinez@bmcglobalgroup.com
  upsunstg team:user:add --team fullstack-dev --user robert.wilson@bmcglobalgroup.com
  ```
- [ ] Add business users to Finance & Billing team
  ```bash
  upsunstg team:user:add --team finance-billing --user amanda.davis@bmcglobalgroup.com
  upsunstg team:user:add --team finance-billing --user kevin.lee@bmcglobalgroup.com
  ```

## Phase 7: Environment Setup

### 7.1 Production Environments
- [ ] Set up production environment for each project
  ```bash
  upsunstg environment:activate --project bmc-core-platform --environment production
  upsunstg environment:activate --project bmc-web-portal --environment production
  # ... repeat for all projects
  ```

### 7.2 Development Environments
- [ ] Create development branches for each project
  ```bash
  upsunstg environment:branch --project bmc-core-platform --environment development
  upsunstg environment:branch --project bmc-web-portal --environment development
  # ... repeat for all projects
  ```

### 7.3 Staging Environments
- [ ] Create staging branches for each project
  ```bash
  upsunstg environment:branch --project bmc-core-platform --environment staging
  upsunstg environment:branch --project bmc-web-portal --environment staging
  # ... repeat for all projects
  ```

## Phase 8: Domain Configuration

### 8.1 Production Domains
- [ ] Add production domains for each project
  ```bash
  upsunstg domain:add --project bmc-core-platform --domain api.bmcglobal.com
  upsunstg domain:add --project bmc-web-portal --domain www.bmcglobal.com
  upsunstg domain:add --project bmc-admin-dashboard --domain admin.bmcglobal.com
  upsunstg domain:add --project bmc-customer-portal --domain customers.bmcglobal.com
  upsunstg domain:add --project bmc-analytics-dashboard --domain analytics.bmcglobal.com
  ```

### 8.2 Staging Domains
- [ ] Add staging domains for each project
  ```bash
  upsunstg domain:add --project bmc-core-platform --domain api-staging.bmcglobal.com
  upsunstg domain:add --project bmc-web-portal --domain staging.bmcglobal.com
  # ... repeat for all projects
  ```

## Phase 9: SSL Certificates

### 9.1 Production Certificates
- [ ] Add SSL certificates for production domains
  ```bash
  upsunstg certificate:add --project bmc-core-platform --certificate-file bmc-global-api.crt --key-file bmc-global-api.key
  upsunstg certificate:add --project bmc-web-portal --certificate-file bmc-global-web.crt --key-file bmc-global-web.key
  # ... repeat for all projects
  ```

## Phase 10: Environment Variables

### 10.1 Application Configuration
- [ ] Set up environment variables for each project
  ```bash
  upsunstg variable:create --project bmc-core-platform --name APP_ENV --value production
  upsunstg variable:create --project bmc-core-platform --name DATABASE_URL --value "mysql://user:pass@host:port/db"
  upsunstg variable:create --project bmc-core-platform --name REDIS_URL --value "redis://host:port"
  # ... repeat for all projects with appropriate values
  ```

### 10.2 API Keys and Secrets
- [ ] Set up API keys and secrets
  ```bash
  upsunstg variable:create --project bmc-core-platform --name JWT_SECRET --value "your-jwt-secret"
  upsunstg variable:create --project bmc-core-platform --name AWS_ACCESS_KEY --value "your-aws-key"
  upsunstg variable:create --project bmc-core-platform --name AWS_SECRET_KEY --value "your-aws-secret"
  # ... repeat for all projects
  ```

## Phase 11: Resource Configuration

### 11.1 Production Resources
- [ ] Set production resource levels for each project
  ```bash
  upsunstg resources:set --project bmc-core-platform --environment production --cpu 2 --memory 4G --disk 20G
  upsunstg resources:set --project bmc-web-portal --environment production --cpu 1 --memory 2G --disk 10G
  # ... repeat for all projects
  ```

### 11.2 Development Resources
- [ ] Set development resource levels for each project
  ```bash
  upsunstg resources:set --project bmc-core-platform --environment development --cpu 1 --memory 2G --disk 10G
  upsunstg resources:set --project bmc-web-portal --environment development --cpu 0.5 --memory 1G --disk 5G
  # ... repeat for all projects
  ```

## Phase 12: Integration Setup

### 12.1 CI/CD Integrations
- [ ] Set up GitHub integration for each project
  ```bash
  upsunstg integration:add --project bmc-core-platform --type github --repository bmc-global/bmc-core-platform
  upsunstg integration:add --project bmc-web-portal --type github --repository bmc-global/bmc-web-portal
  # ... repeat for all projects
  ```

### 12.2 Monitoring Integrations
- [ ] Set up monitoring integrations
  ```bash
  upsunstg integration:add --project bmc-core-platform --type newrelic --api-key "your-newrelic-key"
  upsunstg integration:add --project bmc-web-portal --type datadog --api-key "your-datadog-key"
  # ... repeat for all projects
  ```

## Phase 13: Backup Configuration

### 13.1 Database Backups
- [ ] Set up automated backups for each project
  ```bash
  upsunstg backup:create --project bmc-core-platform --environment production
  upsunstg backup:create --project bmc-data-warehouse --environment production
  # ... repeat for all projects with databases
  ```

## Phase 14: Documentation & Verification

### 14.1 System Verification
- [ ] Verify all organizations are created
  ```bash
  upsunstg organization:list
  ```
- [ ] Verify all teams are created
  ```bash
  upsunstg team:list
  ```
- [ ] Verify all projects are created
  ```bash
  upsunstg project:list
  ```
- [ ] Verify all users are created
  ```bash
  upsunstg user:list
  ```

### 14.2 Environment Verification
- [ ] Verify all environments are active
  ```bash
  upsunstg environment:list
  ```
- [ ] Verify all domains are configured
  ```bash
  upsunstg domain:list
  ```
- [ ] Verify all certificates are installed
  ```bash
  upsunstg certificate:list
  ```

## Phase 15: Demo Data Population

### 15.1 Sample Applications
- [ ] Deploy sample applications to each project
- [ ] Create sample data for analytics projects
- [ ] Set up sample mobile app builds

### 15.2 Demo Scenarios
- [ ] Create demo scenarios for different user roles
- [ ] Set up demo workflows for each team
- [ ] Prepare demo data for presentations

## Phase 16: Demo Ecosystem Cleanup

### 16.1 Delete All Projects
- [ ] Delete BMC Corporate Website project
  ```bash
  upsunstg project:delete --project bmc-corporate-website
  ```
- [ ] Delete BMC E-commerce Store project
  ```bash
  upsunstg project:delete --project bmc-ecommerce-store
  ```
- [ ] Delete BMC CMS Platform project
  ```bash
  upsunstg project:delete --project bmc-cms-platform
  ```
- [ ] Delete BMC API Services project
  ```bash
  upsunstg project:delete --project bmc-api-services
  ```
- [ ] Delete Client Project Alpha
  ```bash
  upsunstg project:delete --project client-project-alpha
  ```
- [ ] Delete Client Project Beta
  ```bash
  upsunstg project:delete --project client-project-beta
  ```
- [ ] Delete BMC Analytics Dashboard project
  ```bash
  upsunstg project:delete --project bmc-analytics-dashboard
  ```

### 16.2 Delete All Teams
- [ ] Delete Full-Stack Development team
  ```bash
  upsunstg team:delete --team fullstack-dev
  ```
- [ ] Delete Executive & Management team
  ```bash
  upsunstg team:delete --team executive-mgmt
  ```
- [ ] Delete Finance & Billing team
  ```bash
  upsunstg team:delete --team finance-billing
  ```

### 16.3 Delete All Users
- [ ] Delete CEO user
  ```bash
  upsunstg user:delete --user sarah.johnson@bmcglobalgroup.com
  ```
- [ ] Delete CTO user
  ```bash
  upsunstg user:delete --user michael.chen@bmcglobalgroup.com
  ```
- [ ] Delete Lead Developer
  ```bash
  upsunstg user:delete --user alex.thompson@bmcglobalgroup.com
  ```
- [ ] Delete Senior Developer
  ```bash
  upsunstg user:delete --user david.kim@bmcglobalgroup.com
  ```
- [ ] Delete Full-Stack Developer
  ```bash
  upsunstg user:delete --user jennifer.martinez@bmcglobalgroup.com
  ```
- [ ] Delete Junior Developer
  ```bash
  upsunstg user:delete --user robert.wilson@bmcglobalgroup.com
  ```
- [ ] Delete Finance Manager
  ```bash
  upsunstg user:delete --user amanda.davis@bmcglobalgroup.com
  ```
- [ ] Delete Operations Manager
  ```bash
  upsunstg user:delete --user kevin.lee@bmcglobalgroup.com
  ```

### 16.4 Delete All Organizations
- [ ] Delete BMC Global Group Inc. (Fixed)
  ```bash
  upsunstg organization:delete --organization bmc-global-group
  ```
- [ ] Delete BMC E-commerce Platform (Fixed)
  ```bash
  upsunstg organization:delete --organization bmc-ecommerce-platform
  ```
- [ ] Delete BMC Content Management (Fixed)
  ```bash
  upsunstg organization:delete --organization bmc-content-management
  ```
- [ ] Delete BMC Development Labs (Flex)
  ```bash
  upsunstg organization:delete --organization bmc-development-labs
  ```
- [ ] Delete BMC Client Projects (Flex)
  ```bash
  upsunstg organization:delete --organization bmc-client-projects
  ```

### 16.5 Cleanup Verification
- [ ] Verify all projects are deleted
  ```bash
  upsunstg project:list
  ```
- [ ] Verify all teams are deleted
  ```bash
  upsunstg team:list
  ```
- [ ] Verify all users are deleted
  ```bash
  upsunstg user:list
  ```
- [ ] Verify all organizations are deleted
  ```bash
  upsunstg organization:list
  ```

### 16.6 Optional: Clean Up SSH Keys
- [ ] List SSH keys to identify demo keys
  ```bash
  upsunstg ssh-key:list
  ```
- [ ] Delete any demo SSH keys if needed
  ```bash
  upsunstg ssh-key:delete --key-id <key-id>
  ```

## Success Criteria

- [ ] All 5 organizations created and configured (3 Fixed for monolithic apps, 2 Flex for microservices)
- [ ] All 3 teams created with proper user assignments (no DevOps team needed)
- [ ] All 7 projects created with proper team assignments
- [ ] All 8 users created with appropriate roles
- [ ] All environments (production, staging, development) configured
- [ ] All domains and SSL certificates configured
- [ ] All integrations and monitoring set up
- [ ] All backup strategies implemented
- [ ] Demo data populated and ready for presentation

## Estimated Timeline
- **Phase 1-2**: 45 minutes (Authentication & Organizations)
- **Phase 3-4**: 20 minutes (Teams & Users)
- **Phase 5-6**: 30 minutes (Projects & Assignments)
- **Phase 7-8**: 1 hour (Environments & Domains)
- **Phase 9-10**: 30 minutes (Certificates & Variables)
- **Phase 11-12**: 20 minutes (Resources & Integrations)
- **Phase 13-15**: 20 minutes (Backups & Demo Data)
- **Phase 16**: 15 minutes (Demo Ecosystem Cleanup)

**Total Estimated Time**: 3.75 hours (including cleanup)

## Notes
- Use `--yes` flag for non-interactive execution
- Use `--verbose` flag for detailed output
- Test each phase before proceeding to the next
- Keep backup of all configuration commands for easy recreation
- Document any custom configurations or deviations from the plan
