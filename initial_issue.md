# Setup Issues and Solutions - RevTickets Project
## Overview
This document outlines the issues encountered during initial Docker setup and their solutions. These issues primarily affected Windows users and were related to Docker/Windows compatibility, package version conflicts, and configuration requirements.
---
## Issue 1: Backend Container Failing to Start - start.sh Not Found
### Symptoms
- Backend container stuck in restart loop
- Error: exec ./start.sh: no such file or directory
- Container exits with code 255
### Root Cause
Windows line endings (CRLF) vs Unix line endings (LF). The start.sh script had Windows line endings, which caused the shebang (#!/bin/bash) to fail in the Linux Docker container.
### Solution
*File:* backend/Dockerfile
Added line ending conversion and explicit bash invocation:
dockerfile
# Make start script executable and fix line endings (Windows compatibility)
RUN chmod +x start.sh && \
    sed -i 's/\r$//' start.sh || true

# Set the entrypoint - explicitly use bash to handle Windows line endings
CMD ["/bin/bash", "./start.sh"]
### Prevention
- Use .gitattributes to enforce LF line endings for shell scripts
- Or configure Git to handle line endings automatically: git config core.autocrlf input
- Or use a .editorconfig file to standardize line endings
---
## Issue 2: Seed Data Script Failing - bcrypt Password Hashing Error
### Symptoms
- Seed data script crashes during user creation
- Error: ValueError: password cannot be longer than 72 bytes
- Error: AttributeError: module 'bcrypt' has no attribute '__about__'
- No users created, login fails with credentials from README
### Root Cause
Version incompatibility between bcrypt 5.0.0 and passlib 1.7.4. The newer bcrypt version has API changes that passlib 1.7.4 doesn't fully support.
### Solution
*File:* backend/requirements.txt
Pinned bcrypt to compatible version:
txt
passlib[bcrypt]
bcrypt==4.1.2
*Note:* The password "password123" is only 12 characters, so the error message was misleading. The real issue was the version incompatibility causing bcrypt initialization to fail.
### Prevention
- Pin all dependency versions in requirements.txt (not just major versions)
- Test seed scripts during Docker build process
- Consider using requirements.in with pip-compile for better dependency management
---
## Issue 3: Backend Startup Blocked by Missing GOOGLE_API_KEY
### Symptoms
- Backend fails to start if GOOGLE_API_KEY environment variable is not set
- Error during LangChain initialization
- Blocks development/testing when AI features aren't needed
### Root Cause
GOOGLE_API_KEY was marked as required in the settings, and LangChain tried to initialize the Google API client at import time, even when AI features weren't being used.
### Solution
*Files Modified:*
- backend/src/core/config.py - Made google_api_key optional with default empty string
- backend/src/langchain_app/config/model_config.py - Implemented lazy loading of LLM
- backend/src/langchain_app/chains/summarize_ticket_data.py - Added error handling for missing API key
- backend/src/langchain_app/chains/generate_closing_comments.py - Added error handling for missing API key
*Changes:*
1. Made API key optional: google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")
2. Lazy-loaded LLM: Only initialize when API key is present
3. Return 503 error when AI endpoints are called without API key configured
### Prevention
- Make optional dependencies truly optional
- Use lazy initialization for external service clients
- Provide clear error messages when optional features require configuration
- Document which features require which environment variables
---
## Issue 4: TypeScript Linter Error - date-fns Module Not Found
### Symptoms
- IDE shows error: Cannot find module 'date-fns' or its corresponding type declarations
- This appears in VS Code/TypeScript but doesn't affect runtime
### Root Cause
TypeScript language server in the IDE can't resolve the module, likely because:
- Node modules aren't installed locally (only in Docker container)
- TypeScript configuration needs adjustment
- IDE needs to be pointed to the correct node_modules location
### Solution
This is a *false positive* - the package is installed in the Docker container and works at runtime. To fix the IDE error:
1. Install dependencies locally: cd frontend && npm install
2. Or configure TypeScript to ignore this error (if only developing in Docker)
3. Or use a dev container setup that shares node_modules
### Prevention
- Document that local npm install may be needed for IDE support
- Consider using VS Code Dev Containers extension for better IDE integration
- Add note in README about IDE setup requirements
