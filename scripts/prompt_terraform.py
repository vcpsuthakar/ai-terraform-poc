from openai import OpenAI
import os
import subprocess

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_terraform(prompt: str) -> str:
    """Generate Terraform code using OpenAI Chat API."""
    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4.1", "gpt-4o-mini"
        messages=[
            {"role": "system", "content": "You are a DevOps expert. Generate ONLY valid Terraform code for Azure. Always include a terraform { required_providers { azurerm } } block with source and version, and a provider azurerm { features {} }. Do not include explanations or markdown formatting."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content

def save_file(filename: str, content: str):
    """Save generated Terraform code to a file."""
    with open(filename, "w") as f:
        f.write(content)

def run_terraform() -> str | None:
    """Run Terraform commands (init, plan, apply)."""
    cmds = ["terraform init", "terraform plan", "terraform apply -auto-approve"]
    for cmd in cmds:
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(process.stdout)
        if process.returncode != 0:
            print("Error:", process.stderr)
            return process.stderr
    return None

if __name__ == "__main__":
    user_prompt = (
        "Create Terraform code to provision an Azure Resource Group in East US with tags for dev environment"
    )

    def clean_code(content: str) -> str:
        """Remove markdown fences and extra text from AI output."""
        if "```" in content:
            content = content.split("```")[1]  # take the part after first ```
            if content.strip().startswith("hcl"):
                content = content.split("\n", 1)[1]  # remove 'hcl' tag
        return content.strip()

    # Step 1: Generate Terraform code
    tf_code = generate_terraform(user_prompt)
    tf_code = clean_code(tf_code)
    save_file("main.tf", tf_code)
    print("✅ Terraform code generated and saved to main.tf")

    # Step 2: Run Terraform
    error = run_terraform()

    # Step 3: Auto-fix if errors occur
    if error:
        print("⚠️ Terraform error occurred. Sending back to AI for debugging...")
        fix_prompt = f"The following Terraform error occurred:\n{error}\nFix the code."
        fix_code = generate_terraform(fix_prompt)
        save_file("main.tf", fix_code)
        print("🔄 Retrying Terraform with fixed code...")
        run_terraform()
