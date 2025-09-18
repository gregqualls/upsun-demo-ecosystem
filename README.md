# 🚢 Upsun Yacht Industry Demo Ecosystem

A powerful, configuration-driven system for creating complete demo ecosystems in Upsun. Perfect for sales demos, training sessions, and showcasing Upsun's capabilities with realistic yacht industry scenarios.

## ⚡ Quick Start (30 seconds)

```bash
# Clone and run the yacht demo
git clone https://github.com/gregqualls/upsun-demo-ecosystem.git
cd upsun-demo-ecosystem
./setup-demo.sh

# Clean up when done
./cleanup-demo.sh
```

**That's it!** The script will create:
- 🏢 **6 Organizations** (3 Fixed + 3 Flex)
- 🚀 **16 Projects** (created in parallel for speed)
- 👥 **User invitations** to all organizations and projects
- 🌍 **Yacht industry scenarios** (marketing, commerce, blogs, IoT, logistics)

## 🎯 What You Get

### Organizations Created
- **BMC Marketing** (Fixed) - Marketing websites and campaigns
- **BMC Commerce** (Fixed) - E-commerce and retail platforms  
- **BMC Blogs** (Fixed) - Content management and blogs
- **BMC Europe** (Flex) - EMEA region services
- **BMC USA** (Flex) - North American operations
- **BMC Singapore** (Flex) - Asia-Pacific services

### Projects Created (16 total)
- **Marketing Sites**: Blatavaria Yachts, Vandercon Shipyard, Yght.CO, Camperson & Nichols, SVBB Marketing
- **E-commerce**: SVB Magento Store, Sailing Franceman Merch
- **Blogs**: Camperson & Nichols Blog, SVBB Blog, Sailing Franceman Blog
- **IoT Services**: EMEA Yacht IoT Services, EMEA Logistics Management
- **Management Systems**: USA Order Management, USA Fleet Tracking, Singapore Booking, Singapore Maintenance

## 🚀 Features

### ⚡ **Parallel Project Creation**
- All 16 projects create simultaneously (not one-by-one)
- **3-5x faster** than sequential creation
- Process tracking with unique IDs for each project

### 🎭 **Hilarious Cleanup Experience**
- 10 escalating verification prompts
- From "Are you sure?" to "BURN IT DOWN!"
- Safety-first approach with humor

### 🔧 **Production & Staging Support**
- Toggle between `upsun` (production) and `upsunstg` (staging)
- Single configuration controls the entire environment
- No code changes needed to switch environments

### 🛡️ **Idempotent & Safe**
- Run multiple times without creating duplicates
- Checks for existing organizations and projects
- Graceful error handling and recovery

## 📋 Prerequisites

The setup script checks these automatically:
- ✅ Python 3.6+
- ✅ Upsun CLI installed (`upsunstg` for staging, `upsun` for production)
- ✅ Authenticated with Upsun
- ✅ Git (for GitHub repository projects)

## ⚙️ Configuration

### Environment Selection
```json
{
  "settings": {
    "use_production": false,  // true = upsun, false = upsunstg
    "region": "plc.recreation.plat.farm",
    "organization_prefix": "bmc-",
    "organization_prefix_replacement": "BMC "
  }
}
```

### User Management
```json
{
  "users": [
    {
      "email": "kemi.ojogbede@platform.sh",
      "name": "Kemi O",
      "role": "developer"
    }
  ]
}
```

## 🎮 Usage Examples

### Basic Yacht Demo
```bash
# Run the complete yacht industry demo
./setup-demo.sh

# Check what was created
upsunstg organization:list
upsunstg project:list

# Clean up when done
./cleanup-demo.sh
```

### Custom Configuration
```bash
# Use your own configuration
python3 demo-setup.py --config my-demo.json
chmod +x setup-demo-ecosystem.sh
./setup-demo-ecosystem.sh
```

### Production Environment
```bash
# Switch to production in demo-config.json
# "use_production": true

# Run with production CLI
./setup-demo.sh
```

## 🔧 Advanced Features

### Parallel Project Creation
The script creates all projects simultaneously using background processes:
- Each project runs in its own process
- Process IDs are tracked and displayed
- All processes complete before continuing
- Much faster than sequential creation

### Smart Organization Handling
- **Fixed Organizations**: Created via API with `a:curl`
- **Flex Organizations**: Created via standard CLI
- **Unique Names**: Timestamp-based names prevent conflicts
- **Rate Limiting**: Built-in delays to avoid API limits

### User Invitation System
- Invites users to all organizations
- Invites users to all projects
- Handles errors gracefully
- Works with both staging and production

## 🎯 Demo Scenarios

### Sales Demos
- **Multi-tenant Architecture**: Show different organization types
- **Scalability**: Demonstrate parallel project creation
- **User Management**: Invite team members to collaborate
- **Real-world Examples**: Yacht industry use cases

### Training Sessions
- **Configuration-driven**: Show how to customize demos
- **Environment Management**: Switch between staging/production
- **Cleanup Procedures**: Safe environment teardown
- **Best Practices**: Idempotent, safe, and maintainable

## 🛠️ Troubleshooting

### Common Issues

**Authentication Required**
```bash
upsunstg auth:browser-login
```

**Projects Not Creating**
- Check organization status: `upsunstg organization:list`
- Verify region setting in config
- Check for rate limiting (script handles this automatically)

**Cleanup Issues**
- Run cleanup script multiple times if needed
- Check for any remaining projects: `upsunstg project:list`
- Manual cleanup: `upsunstg project:delete --project PROJECT_ID`

### Debug Commands
```bash
# Check authentication
upsunstg auth:info

# List organizations
upsunstg organization:list

# List projects
upsunstg project:list

# Check specific project
upsunstg project:info --project PROJECT_ID
```

## 📁 File Structure

```
upsun-demo-ecosystem/
├── setup-demo.sh              # 🚀 One-command setup
├── cleanup-demo.sh            # 🧹 Hilarious cleanup
├── demo-setup.py              # 🐍 Main Python script
├── demo-config.json           # ⚙️ Yacht industry configuration
├── example-config.json        # 📝 Example configuration
└── README.md                  # 📖 This file
```

## 🎉 Benefits

- ⚡ **Fast**: Parallel project creation (3-5x faster)
- 🎭 **Fun**: Hilarious cleanup verification prompts
- 🔧 **Flexible**: Works with staging and production
- 🛡️ **Safe**: Idempotent and error-resistant
- 🎯 **Realistic**: Complete yacht industry demo
- 👥 **Team-ready**: User invitation system
- 📝 **Configurable**: Everything driven by JSON config
- 🧹 **Clean**: Complete cleanup procedures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both staging and production
5. Submit a pull request

## 📞 Support

For issues or questions:
1. Check the generated shell scripts for errors
2. Verify your Upsun CLI authentication
3. Test with a small configuration first
4. Check the troubleshooting section above

---

**Ready to demo? Run `./setup-demo.sh` and watch the magic happen! 🚀**