# CodeQL Configuration for Educational Repository

## Current Situation

This repository contains **intentionally vulnerable code examples** in:
- `**/ejemplos_vulnerables/**` - Security training examples (Module 3)
- `**/tareas_bugs*.py` - Debugging exercise examples

CodeQL detects these as real vulnerabilities, but they are **educational material** by design.

## CodeQL Configuration

The `.github/codeql-config.yml` file contains exclusion rules for these intentional examples.

### To Enable This Configuration

**GitHub CodeQL Default Setup is currently active** and doesn't automatically use custom config files. To use our configuration:

1. Go to: **Settings** → **Code security and analysis**
2. Under **CodeQL analysis**, click **Configure** (or **Edit configuration**)
3. Select **Advanced** setup
4. In the workflow file, add:
   ```yaml
   - name: Initialize CodeQL
     uses: github/codeql-action/init@v3
     with:
       config-file: ./.github/codeql-config.yml
   ```

### Alternative: Accept False Positives

Since these are **teaching examples**, you can also choose to accept the CodeQL warnings as expected false positives. Every flagged file is intentional for security education.

## Files Excluded in Config

```yaml
paths-ignore:
  - '**/ejemplos_vulnerables/**'      # Module 3 security examples
  - '**/tareas_bugs*.py'              # Debugging exercises
  - '**/tests/fixtures/vulnerable_*'  # Test fixtures
  - '**/.venv/**'                     # Virtual environments
  - '**/node_modules/**'              # Dependencies
```

## Example: Code Injection in ejemplos_vulnerables

```python
# Modulo 3 – Calidad y Seguridad/Clase 2/ejemplos_vulnerables/a03_injection.py

# ❌ VULNERABILIDAD CRÍTICA INTENCIONAL - Para enseñanza
resultado = eval(expresion)  # CodeQL correctamente detecta esto
```

This is **intentional** for teaching OWASP A03:2021 Injection vulnerabilities.
