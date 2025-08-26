# Yada Autonomous Creator

## Overview
Yada Autonomous Creator is an ethical and autonomous AI application designed to assist users in creating workflows, web applications, and more. It leverages advanced AI capabilities to generate code and automate tasks while adhering to ethical principles.

## Features
- Generates n8n workflows and web applications.
- Deploys applications to n8n and Vercel.
- Runs code in a secure Docker sandbox.
- Ensures ethical compliance through predefined principles.

## System Requirements
- Operating System: Windows, macOS, or Linux
- Hardware: Minimum 2 CPU cores, 4 GB RAM (8 GB recommended), 10 GB disk space
- Python: Version 3.12 or higher
- Docker: Installed and running

## Installation Instructions

1. **Clone the Repository**
   ```
   git clone <repository-url>
   cd yada-autonomous-creator
   ```

2. **Set Up a Virtual Environment**
   ```
   python -m venv yada_env
   source yada_env/bin/activate  # On Windows use: yada_env\Scripts\activate
   ```

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Configure API Keys**
   - Obtain API keys for OpenAI, n8n, and Vercel.
   - Set environment variables for the keys:
     - Linux/macOS: Add to `~/.bashrc`
     - Windows: Use PowerShell to set environment variables.

5. **Run the Application**
   ```
   python src/yada_creator.py
   ```

## Usage
- Access the web interface at `http://localhost:5000`.
- Describe your task in the provided form and execute it to see results.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.