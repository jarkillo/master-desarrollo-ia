import re, sys, os

TEMPLATE_PATH = os.path.join("infra", ".env.template")
ENV_PATH = ".env"

missing = []
if not os.path.exists(TEMPLATE_PATH):
    print("❌ No se encontró infra/.env.template")
    sys.exit(1)

if not os.path.exists(ENV_PATH):
    print("⚠️  No hay archivo .env, créalo a partir del template.")
    sys.exit(1)

with open(TEMPLATE_PATH, "r") as f:
    variables = re.findall(r"^([A-Z_]+)=", f.read(), re.MULTILINE)

with open(ENV_PATH, "r") as f:
    contenido_env = f.read()

for var in variables:
    if var not in contenido_env:
        missing.append(var)

if missing:
    print("❌ Faltan variables en .env:", ", ".join(missing))
    sys.exit(1)

print("✅ Variables sincronizadas correctamente")
