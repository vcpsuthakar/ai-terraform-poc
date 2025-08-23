from openai import OpenAI
import os
import subprocess
import re

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- Load Prompts from Files ----------
def load_prompt(filename: str) -> str:
    """Read prompt text from a file inside 'prompts' folder."""
    with open(os.path.join("prompts", filename), "r") as f:
        return f.read().strip()

SYSTEM_PROMPT = load_prompt("system_prompt.txt")
USER_PROMPT = load_prompt("user_prompt.txt")
FIX_PROMPT_TEMPLATE = load_prompt("fix_prompt.txt")

# ---------- OpenAI Call ----------
def generate_terraform(prompt: str, system_prompt: str = SYSTEM_PROMPT) -> str:
    """Generate Terraform code using OpenAI Chat API."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content

# ---------- File Handling ----------
def save_file(filename: str, content: str):
    """Save generated Terraform code to a file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # ensure 'modules/' exists
    with open(filename, "w") as f:
        f.write(content)

def clean_code(content: str) -> str:
    """Remove markdown fences and ensure only HCL remains."""
    if "```" in content:
        content = content.split("```")[1]  # take part between first fences
        if content.strip().startswith("hcl"):
            content = content.split("\n", 1)[1]
    return content.strip()

def enforce_best_practices(code: str) -> str:
    """Auto-replace deprecated/unsafe patterns before saving."""
    code = code.replace("azurerm_app_service_plan", "azurerm_service_plan")

    if "filebase64" in code:
        print("⚠️ Found filebase64 usage for certs. Replacing with Key Vault secret reference placeholder.")
        code = re.sub(
            r'data\s*=\s*filebase64\([^\)]*\)',
            'key_vault_secret_id = azurerm_key_vault_secret.ssl_cert.id',
            code
        )
    return code

# ---------- Terraform Runner ----------
def run_terraform() -> str | None:
    """Run Terraform init, validate, plan, apply inside 'modules/'."""
    cmds = ["terraform init", "terraform validate", "terraform plan"]
    for cmd in cmds:
        process = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd="modules"
        )
        print(process.stdout)
        if process.returncode != 0:
            print("❌ Error:", process.stderr)
            return process.stderr
    return None

# ---------- Main ----------
if __name__ == "__main__":
    # Step 1: Generate initial Terraform code
    tf_code = generate_terraform(USER_PROMPT)
    tf_code = clean_code(tf_code)
    tf_code = enforce_best_practices(tf_code)
    save_file("modules/main.tf", tf_code)
    print("✅ Terraform code generated and saved to modules/main.tf")

    # Step 2: Run Terraform
    error = run_terraform()

    # Step 3: Multi-Retry Auto-Fix if errors occur
    retries = 0
    max_retries = 3
    while error and retries < max_retries:
        retries += 1
        print(f"⚠️ Attempt {retries}: Terraform error occurred. Sending back to AI for debugging...")

        fix_prompt = FIX_PROMPT_TEMPLATE.format(
            error_message=error,
            original_code=tf_code
        )

        fixed_code = generate_terraform(
            fix_prompt,
            system_prompt=(
                SYSTEM_PROMPT
                + "\nIMPORTANT: Do not use deprecated resources. "
                + "Use azurerm_service_plan instead of azurerm_app_service_plan. "
                + "Use Key Vault for certs/secrets instead of filebase64."
            )
        )
        fixed_code = clean_code(fixed_code)
        fixed_code = enforce_best_practices(fixed_code)

        save_file("modules/main.tf", fixed_code)
        tf_code = fixed_code

        print("🔄 Retrying Terraform with fixed code...")
        error = run_terraform()

    # Step 4: Diagnostic if still fails
    if error:
        diag_path = "modules/diagnostic_report.txt"
        os.makedirs(os.path.dirname(diag_path), exist_ok=True)
        with open(diag_path, "w") as f:
            f.write("Terraform failed after retries.\n\n")
            f.write("Last error:\n")
            f.write(error + "\n\n")
            f.write("Last generated Terraform code:\n")
            f.write(tf_code)
        print(f"🚨 Failed after 3 retries. Diagnostic report saved to {diag_path}")
