# Demo Examples

This folder contains working Upsun application examples that can be used for demos without requiring external GitHub repository access.

## Available Examples

### 1. Flask Yacht IoT Services (`flask-yacht-iot/`)
- **Type**: Python Flask application
- **Description**: IoT monitoring and management for yachts
- **Features**: 
  - REST API endpoints
  - Database integration (PostgreSQL)
  - Health check endpoints
  - Modern web interface
- **Files**:
  - `app.py` - Main Flask application
  - `requirements.txt` - Python dependencies
  - `templates/index.html` - Web interface
  - `.upsun/config.yaml` - Upsun configuration
  - `.environment` - Environment variables

### 2. Demo Decouple Frontend (`demo-decouple-frontend/`)
- **Type**: Multi-application (PHP Symfony + Node.js Next.js)
- **Description**: Decoupled frontend/backend architecture
- **Features**:
  - Symfony backend API
  - Next.js frontend
  - Database integration
  - Modern development workflow
- **Files**:
  - `backend/` - Symfony PHP application
  - `frontend/` - Next.js React application
  - `.upsun/config.yaml` - Upsun configuration

### 3. WordPress Blog (`wordpress-blog/`)
- **Type**: PHP WordPress application
- **Description**: Content management system for blogs
- **Features**:
  - WordPress CMS
  - Database integration
  - Content management
  - Plugin support
- **Files**:
  - `wordpress/` - WordPress core files
  - `wp-cli.yml` - WP-CLI configuration
  - `.upsun/config.yaml` - Upsun configuration
  - `.environment` - Environment variables

## Usage

These examples are automatically used by the demo setup script when projects are configured with `"type": "local"` in the `demo-config.json` file.

### Local Development

You can also use these examples for local development:

1. **Flask Application**:
   ```bash
   cd examples/flask-yacht-iot
   pip install -r requirements.txt
   python app.py
   ```

2. **Demo Decouple Frontend**:
   ```bash
   cd examples/demo-decouple-frontend/backend
   composer install
   php bin/console server:run
   
   # In another terminal:
   cd examples/demo-decouple-frontend/frontend
   npm install
   npm run dev
   ```

3. **WordPress Blog**:
   ```bash
   cd examples/wordpress-blog
   # Follow WordPress setup instructions
   ```

## Adding New Examples

To add a new example:

1. Create a new directory in `examples/`
2. Include all necessary application files
3. Add a `.upsun/config.yaml` configuration file
4. Add any required environment files (`.environment`, etc.)
5. Update this README with the new example details
6. Update `demo-config.json` to reference the new example

## Configuration

Each example includes a properly configured `.upsun/config.yaml` file that defines:
- Application runtime and dependencies
- Database relationships
- Build and deployment hooks
- Web server configuration
- Environment variables

These configurations are tested and ready for deployment on Upsun.
