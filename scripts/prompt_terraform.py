import openai
import os
import subprocess

# Configure API key (OpenAI or local Ollama)
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_terraform(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-4o" / "ollama" if running locally
        messages=[
            {"role": "system", "content": "You are a DevOps expert. Generate valid Terraform code for Azure."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response['choices'][0]['message']['content']

def save_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def run_terraform():
    cmds = ["terraform init", "terraform plan", "terraform apply -auto-approve"]
    for cmd in cmds:
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(process.stdout)
        if process.returncode != 0:
            print("Error:", process.stderr)
            return process.stderr
    return None

if __name__ == "__main__":
    user_prompt = "Create Terraform code to provision an Azure Virtual Machine and a Storage Account in East US with tags for dev environment."
    tf_code = generate_terraform(user_prompt)
    save_file("main.tf", tf_code)

    print("Terraform code generated and saved to main.tf")

    error = run_terraform()
    if error:
        print("Sending error back to AI for debugging...")
        fix_prompt = f"The following Terraform error occurred:\n{error}\nFix the code."
        fix_code = generate_terraform(fix_prompt)
        save_file("main.tf", fix_code)
        run_terraform()
