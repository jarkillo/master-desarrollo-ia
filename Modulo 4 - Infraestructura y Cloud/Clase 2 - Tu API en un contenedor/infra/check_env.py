# infra/check_env.py
import re, sys, os

TEMPLATE_PATH = os.path.join("infra", ".env.template")
ENV_PATH = ".env"
EN_CI = os.getenv("GITHUB_ACTIONS") == "true"

if not os.path.exists(TEMPLATE_PATH):
    print("❌ No se encontró infra/.env.template")
    sys.exit(1)

if not os.path.exists(ENV_PATH):
    if EN_CI:
        print(
            "ℹ️  CI: no hay .env; se omite la validación de valores (solo se valida en local)."
        )
        sys.exit(0)
    else:
        print("⚠️  No hay archivo .env, créalo a partir del template.")
        sys.exit(1)

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    variables = re.findall(r"^([A-Z_]+)=", f.read(), re.MULTILINE)

with open(ENV_PATH, "r", encoding="utf-8") as f:
    contenido_env = f.read()

missing = [var for var in variables if var not in contenido_env]

if missing:
    print("❌ Faltan variables en .env:", ", ".join(missing))
    sys.exit(1)

print("✅ Variables sincronizadas correctamente")
