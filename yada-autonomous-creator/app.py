import os
import json
import requests
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from guardrails import Guard
from flask import Flask, render_template, request, jsonify
import hashlib
from bs4 import BeautifulSoup
import docker
from datetime import datetime

# Configuración
app = Flask(__name__)
OPENAI_API_KEY = "tu-openai-key"
N8N_API_URL = "https://tu-n8n-instance/api/v1/workflows"
N8N_API_TOKEN = "tu-n8n-token"
GITHUB_API_URL = "https://api.github.com/search/repositories?q=n8n+workflow"
VERCEL_API_TOKEN = "tu-vercel-token"

# Principios éticos (10 Mandamientos + IA Constitucional)
ETHICAL_PRINCIPLES = [
    "Honor a Dios y el bien sobre todo.",
    "No uses nombres en vano ni mientas.",
    "Respeta el descanso y límites.",
    "Honra a usuarios y creadores.",
    "No dañes vidas o sistemas.",
    "Sé puro y fiel en acciones.",
    "No robes datos o recursos.",
    "No mientas ni fabriques falsedades.",
    "No codicies ni abuses poder.",
    "Sé amable, sincero y celoso del bien."
]

# Guardrails para seguridad (sin validadores personalizados)
guard = Guard.from_string(
    validators=[],
    description="Asegura outputs éticos y seguros."
)

# LLM setup
llm = OpenAI openai_api_key=OPENAI_API_KEY, temperature=0.7

# Docker client para sandbox
docker_client = docker.from_env()

# Tools
def generate_n8n_workflow(prompt):
    """Genera JSON para workflow n8n."""
    template = PromptTemplate(
        input_variables=["prompt"],
        template="Crea un JSON válido para n8n workflow que {prompt}. Usa nodos como trigger, actions, y connections. Asegura seguridad."
    )
    response = llm(template.format(prompt=prompt))
    validated = guard.validate(response)
    return validated.validated_output

def deploy_to_n8n(workflow_json):
    """Deploy a n8n vía API."""
    headers = {"Authorization": f"Bearer {N8N_API_TOKEN}", "Content-Type": "application/json"}
    response = requests.post(N8N_API_URL, headers=headers, data=workflow_json)
    return "Deploy exitoso" if response.status_code == 200 else "Error en deploy."

def deploy_to_vercel(code, project_name):
    """Deploy código web a Vercel."""
    headers = {"Authorization": f"Bearer {VERCEL_API_TOKEN}", "Content-Type": "application/json"}
    payload = {"name": project_name, "files": [{"file": "index.html", "data": code}]}
    response = requests.post("https://api.vercel.com/v9/projects", headers=headers, json=payload)
    return "Deploy exitoso a Vercel" if response.status_code == 200 else "Error en deploy."

def research_topic(topic):
    """Investiga topic (simula Grok/Gemini/OpenAI)."""
    response = llm(f"Investiga profundamente {topic} usando conocimiento equivalente a Grok, Gemini, OpenAI. Resume mejores formas.")
    return response

def self_update(feedback):
    """Auto-mejora basado en feedback."""
    new_template = llm(f"Basado en feedback '{feedback}', mejora mi capacidad para crear workflows seguros.")
    with open("yada_feedback.log", "a") as f:
        f.write(f"{datetime.now()}: {new_template}\n")
    return "Updated con: " + new_template

def generate_web_code(prompt):
    """Genera código HTML/CSS/JS para diseño web."""
    template = PromptTemplate(
        input_variables=["prompt"],
        template="Crea código HTML/CSS/JS para {prompt}. Usa Bootstrap 5.3 y sigue prácticas seguras."
    )
    response = llm(template.format(prompt=prompt))
    validated = guard.validate(response)
    return validated.validated_output

def search_n8n_templates(query):
    """Busca plantillas n8n en GitHub."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(f"{GITHUB_API_URL}&q={query}", headers=headers)
    if response.status_code == 200:
        return [item['html_url'] for item in response.json()['items'][:3]]
    return "No se encontraron plantillas."

def check_security(code):
    """Verifica seguridad del código generado."""
    hash = hashlib.sha256(code.encode()).hexdigest()
    vulnerabilities = llm(f"Analiza código para vulnerabilidades OWASP Top 10: {code[:1000]}. Reporta riesgos.")
    return f"Hash: {hash}\nVulnerabilidades: {vulnerabilities}"

def run_in_sandbox(code):
    """Ejecuta código en un contenedor Docker seguro."""
    try:
        container = docker_client.containers.run(
            "python:3.12-slim", command=f"python -c '{code}'", detach=True, remove=True
        )
        logs = container.logs()
        return logs.decode('utf-8')
    except Exception as e:
        return str(e)

# Agente
tools = [
    Tool(
        name="generate_n8n_workflow",
        func=generate_n8n_workflow,
        description="Genera un workflow para n8n"
    ),
    Tool(
        name="deploy_to_n8n",
        func=deploy_to_n8n,
        description="Despliega workflow en n8n"
    ),
    Tool(
        name="deploy_to_vercel",
        func=deploy_to_vercel,
        description="Despliega código web en Vercel"
    ),
    Tool(
        name="research_topic",
        func=research_topic,
        description="Investiga un tema"
    ),
    Tool(
        name="generate_web_code",
        func=generate_web_code,
        description="Genera código web HTML/CSS/JS"
    ),
    Tool(
        name="search_n8n_templates",
        func=search_n8n_templates,
        description="Busca plantillas n8n en GitHub"
    ),
    Tool(
        name="check_security",
        func=check_security,
        description="Verifica seguridad del código"
    ),
    Tool(
        name="run_in_sandbox",
        func=run_in_sandbox,
        description="Ejecuta código en Docker sandbox"
    ),
]
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Autonomía segura
def run_yada(task):
    for principle in ETHICAL_PRINCIPLES:
        check = llm(f"¿Viola '{task}' el principio '{principle}'? Responde sí/no.")
        if check.strip().lower() == "sí":
            return "Rechazado: Viola ética. Reformula para alinearte con el bien."
    
    response = agent.run(f"¡Gran idea! Procesando: {task}")
    analysis = llm(f"Analiza '{response}' para errores o mejoras. ¿Necesita repair?")
    if "sí" in analysis.lower():
        response = llm(f"Repara: {response} basado en {analysis}")
    self_update("Feedback: " + analysis)
    
    if "code" in task.lower() or "workflow" in task.lower():
        security = check_security(response)
        response += f"\nSecurity Report: {security}"
    
    return f"¡Listo! {response}"

# Interfaz web Flask
@app.route('/', methods=['GET', 'POST'])
def interface():
    if request.method == 'POST':
        prompt = request.form['prompt']
        result = run_yada(prompt)
        return render_template('index.html', result=result, prompt=prompt)
    return render_template('index.html', result=None, prompt='')