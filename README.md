# AI-Terraform-Code

An intelligent Terraform code generator that uses OpenAI GPT-4 to create, validate, and automatically fix Azure infrastructure configurations. This project demonstrates the integration of AI-powered infrastructure-as-code generation with automated validation and error correction.

## 🌟 Features

- **AI-Powered Code Generation**: Uses OpenAI GPT-4 to generate production-ready Terraform code
- **Automatic Error Detection & Fixing**: Self-healing infrastructure code with intelligent retry mechanisms
- **Multi-Environment Support**: Pre-configured for SIT, UAT, and Production environments
- **Security Best Practices**: Built-in security configurations including private endpoints, NSGs, and Key Vault integration
- **Azure Resource Compliance**: Follows Azure naming conventions and governance standards
- **CI/CD Integration**: GitHub Actions workflow for automated deployment
- **Prompt Engineering**: Sophisticated prompt templates for consistent, high-quality code generation

## 🏗️ Architecture

```
ai-terraform-poc/
├── agent/                      
│   ├── prompt_terraform.py     
│   └── validate_fix.py         
├── environments/               
│   ├── sit/terraform.tfvars    
│   ├── urt/terraform.tfvars    
│   └── prod/terraform.tfvars   
├── modules/                    
│   └── main.tf                 
├── prompts/                    
│   ├── config.json             
│   ├── system_prompt.txt       
│   ├── user_prompt.txt         
│   ├── user_prompt_template.txt 
│   └── fix_prompt.txt          
├── .github/workflows/          
│   └── ci-cd.yml              
└── requirements.txt            
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Terraform 1.0+
- Azure CLI (authenticated)
- OpenAI API Key

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd ai-terraform-poc
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export ARM_CLIENT_ID="your-azure-client-id"
   export ARM_CLIENT_SECRET="your-azure-client-secret"
   export ARM_SUBSCRIPTION_ID="your-azure-subscription-id"
   export ARM_TENANT_ID="your-azure-tenant-id"
   ```

### Usage

1. **Generate Infrastructure Code**:
   ```bash
   cd ai-terraform-poc
   python agent/prompt_terraform.py
   ```

2. **Deploy to Specific Environment**:
   ```bash
   cd modules
   terraform init
   terraform plan -var-file=../environments/sit/terraform.tfvars
   terraform apply -var-file=../environments/sit/terraform.tfvars
   ```

## 🤖 AI Agent Capabilities

### Code Generation
- Interprets natural language infrastructure requirements
- Generates production-ready Terraform code following Azure best practices
- Implements security controls and governance standards automatically

### Auto-Fixing
- Detects Terraform validation errors
- Automatically generates fixes using AI
- Supports up to 3 retry attempts with progressive improvements
- Creates diagnostic reports for persistent issues

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 access | Yes |
| `ARM_CLIENT_ID` | Azure Service Principal Client ID | Yes |
| `ARM_CLIENT_SECRET` | Azure Service Principal Secret | Yes |
| `ARM_SUBSCRIPTION_ID` | Azure Subscription ID | Yes |
| `ARM_TENANT_ID` | Azure Tenant ID | Yes |

### Prompt Customization

Edit `prompts/user_prompt.txt` to modify infrastructure requirements:

```
PROJECT DETAILS:
- Project Name: Your Project
- Environment: Development/Production
- Business Unit: Your Unit
- Owner: Your Team
- Cost Center: Your Cost Center

RESOURCE REQUIREMENTS:
- Describe your infrastructure needs...

NAMING & GOVERNANCE:
- Naming Prefix: your-prefix
- Tags: Your tagging strategy
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`ci-cd.yml`) provides:

- **Automated Code Generation**: Runs AI agent on code changes
- **Terraform Validation**: Validates generated code
- **Multi-Environment Deployment**: Supports SIT → UAT → Production flow
- **Security Scanning**: Built-in security checks

### Required Secrets
Configure these secrets in your GitHub repository:
- `OPENAI_API_KEY`
- `ARM_CLIENT_ID`
- `ARM_CLIENT_SECRET`
- `ARM_SUBSCRIPTION_ID`
- `ARM_TENANT_ID`

## 🛡️ Security Features

- **Private Endpoints**: Secure access to Azure services
- **Network Security Groups**: Controlled network access
- **Azure Key Vault Integration**: Secure secrets management
- **Managed Identity Support**: Enhanced security for Azure resources
- **Resource Tagging**: Compliance and governance tracking

1. **OpenAI API Errors**:
   - Verify `OPENAI_API_KEY` is set correctly
   - Check API quota and billing status

2. **Terraform Validation Errors**:
   - Review `modules/diagnostic_report.txt` for detailed error analysis
   - Check Azure provider version compatibility

3. **Authentication Issues**:
   - Ensure Azure Service Principal has appropriate permissions
   - Verify all ARM environment variables are set

## 📄 License

This project is licensed under the MIT License

## 🔮 Future Enhancements

- [ ] Support for additional cloud providers (AWS, GCP)
- [ ] Integration with Terraform Cloud/Enterprise
- [ ] Advanced cost optimization suggestions
- [ ] Infrastructure drift detection and correction
- [ ] Multi-region deployment strategies
- [ ] Enhanced security scanning and recommendations

## 📞 Support

For issues and questions:
1. Check existing GitHub Issues
2. Create a new issue with detailed description

## 🏷️ Tags

`#terraform` `#azure` `#ai` `#infrastructure-as-code` `#automation` `#devops` `#gpt4` `#openai`

-----------------------------------
**Made with ❤️ by the DevOps Team**
- Suthakar Paramathma
