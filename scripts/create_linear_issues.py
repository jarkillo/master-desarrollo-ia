"""
Script to create all Linear issues from LINEAR_ISSUES_MASTER_PLAN.md

This script reads the master plan and creates all 42 issues in Linear using GraphQL API.

Usage:
    1. Copy .env.template to .env
    2. Add your Linear API key
    3. Run: python create_linear_issues.py
"""

import os
import re
import time
from dataclasses import dataclass
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")
LINEAR_API_URL = "https://api.linear.app/graphql"
TEAM_KEY = os.getenv("LINEAR_TEAM_KEY", "JAR")  # Team key (JAR for JAR-XXX issues)
TEAM_ID = "d6e60bff-96b3-4393-8894-d9eb72899539"  # Team Jarko ID
PROJECT_ID = "3237de8a-8c51-425a-9af7-b4f219cca458"  # Master desarrollo con IA project
PROJECT_NAME = "Master desarrollo con IA"

@dataclass
class Issue:
    """Represents a Linear issue to create."""
    title: str
    description: str
    labels: list[str]
    priority: str  # P0, P1, P2, P3
    estimate: str  # 1-2h, 3-4h, etc.
    module: str
    agent_workflow: str = ""  # Recommended agent workflow

class LinearAPI:
    """Linear GraphQL API client."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }

    def execute_query(self, query: str, variables: dict | None = None) -> dict:
        """Execute a GraphQL query against Linear API."""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = requests.post(
            LINEAR_API_URL,
            headers=self.headers,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"Query failed: {response.status_code} - {response.text}")

        data = response.json()
        if "errors" in data:
            raise Exception(f"GraphQL errors: {data['errors']}")

        return data["data"]

    def get_team_id(self, team_key: str) -> str:
        """Get team ID by team key."""
        query = """
        query GetTeam($key: String!) {
            team(key: $key) {
                id
                name
            }
        }
        """
        result = self.execute_query(query, {"key": team_key})
        return result["team"]["id"]

    def get_or_create_project(self, team_id: str, project_name: str) -> str:
        """Get existing project or create new one."""
        # First try to find existing project
        query = """
        query GetProjects($teamId: String!) {
            projects(filter: { team: { id: { eq: $teamId } } }) {
                nodes {
                    id
                    name
                }
            }
        }
        """
        result = self.execute_query(query, {"teamId": team_id})

        for project in result["projects"]["nodes"]:
            if project["name"] == project_name:
                print(f"✅ Found existing project: {project_name} ({project['id']})")
                return project["id"]

        # Create new project
        mutation = """
        mutation CreateProject($teamId: String!, $name: String!) {
            projectCreate(input: { teamId: $teamId, name: $name }) {
                project {
                    id
                    name
                }
            }
        }
        """
        result = self.execute_query(mutation, {"teamId": team_id, "name": project_name})
        project_id = result["projectCreate"]["project"]["id"]
        print(f"✅ Created new project: {project_name} ({project_id})")
        return project_id

    def get_or_create_label(self, team_id: str, name: str, color: str = "#5E6AD2") -> str:
        """Get existing label or create new one."""
        # Try to find existing label
        query = """
        query GetLabels($teamId: String!) {
            issueLabels(filter: { team: { id: { eq: $teamId } } }) {
                nodes {
                    id
                    name
                }
            }
        }
        """
        result = self.execute_query(query, {"teamId": team_id})

        for label in result["issueLabels"]["nodes"]:
            if label["name"] == name:
                return label["id"]

        # Create new label
        mutation = """
        mutation CreateLabel($teamId: String!, $name: String!, $color: String!) {
            issueLabelCreate(input: { teamId: $teamId, name: $name, color: $color }) {
                issueLabel {
                    id
                    name
                }
            }
        }
        """
        result = self.execute_query(mutation, {
            "teamId": team_id,
            "name": name,
            "color": color
        })
        label_id = result["issueLabelCreate"]["issueLabel"]["id"]
        print(f"  ✅ Created label: {name}")
        return label_id

    def create_issue(
        self,
        team_id: str,
        project_id: str,
        title: str,
        description: str,
        label_ids: list[str],
        priority: int
    ) -> str:
        """Create a new issue in Linear."""
        mutation = """
        mutation CreateIssue(
            $teamId: String!,
            $projectId: String!,
            $title: String!,
            $description: String,
            $labelIds: [String!],
            $priority: Int
        ) {
            issueCreate(input: {
                teamId: $teamId,
                projectId: $projectId,
                title: $title,
                description: $description,
                labelIds: $labelIds,
                priority: $priority
            }) {
                issue {
                    id
                    identifier
                    title
                }
            }
        }
        """

        result = self.execute_query(mutation, {
            "teamId": team_id,
            "projectId": project_id,
            "title": title,
            "description": description,
            "labelIds": label_ids,
            "priority": priority
        })

        issue = result["issueCreate"]["issue"]
        return issue["id"], issue["identifier"]


def parse_master_plan(file_path: str) -> list[Issue]:
    """Parse LINEAR_ISSUES_MASTER_PLAN.md and extract issues."""
    with open(file_path, encoding='utf-8') as f:
        content = f.read()

    issues = []

    # Find all issue sections (headers with M1-1, M2-1, etc.)
    pattern = r'### (M\d+-\d+|GAME-\d+|FIX-\d+): (.+?)\n\*\*Prioridad\*\*: (P\d+).+?\n\*\*Labels\*\*: (.+?)\n\*\*Estimación\*\*: (.+?)\n(.+?)(?=\n### |\n## |$)'

    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        issue_id = match.group(1)
        title = f"{issue_id}: {match.group(2)}"
        priority_str = match.group(3)
        labels_str = match.group(4)
        estimate = match.group(5)
        body = match.group(6).strip()

        # Extract module from issue_id
        if issue_id.startswith('M'):
            module_num = issue_id[1]
            module = f"module-{module_num}"
        elif issue_id.startswith('GAME'):
            module = "game"
        elif issue_id.startswith('FIX'):
            module = "fixes"
        else:
            module = "other"

        # Parse labels
        labels = [label.strip().strip('`') for label in labels_str.split(',')]

        # Determine recommended agent workflow
        agent_workflow = determine_agent_workflow(title, labels, body)

        # Append agent workflow to description
        full_description = body + agent_workflow

        issues.append(Issue(
            title=title,
            description=full_description,
            labels=labels,
            priority=priority_str,
            estimate=estimate,
            module=module,
            agent_workflow=agent_workflow
        ))

    return issues


def determine_agent_workflow(title: str, labels: list[str], description: str) -> str:
    """Determine recommended agent workflow based on issue type and content."""

    agents = []
    workflow_description = ""

    # Detectar tipo de issue basado en labels y contenido
    is_ai_integration = "ai-integration" in labels
    is_content_creation = "content-creation" in labels
    is_bug_fix = "bug-fix" in labels
    is_game = "game" in labels

    # Detectar tecnología basada en título y descripción
    has_fastapi = "FastAPI" in title or "CRUD" in title or "API" in title or "endpoint" in title.lower()
    has_database = "Database" in title or "SQLAlchemy" in title or "Alembic" in title or "ORM" in title
    has_docker = "Docker" in title or "contenedor" in title.lower() or "Dockerfile" in description
    has_react = "React" in title or "Frontend" in title or "UI" in title
    has_testing = "Test" in title or "Testing" in title or "Pytest" in title
    has_security = "Security" in title or "JWT" in title or "Auth" in title
    has_performance = "Performance" in title or "Optimization" in title or "Cache" in title

    # Module-specific patterns
    module_num = None
    for label in labels:
        if label.startswith("module-"):
            module_num = label.split("-")[1]
            break

    # Build agent workflow based on context

    # 1. Core agents for Python code quality (almost always needed)
    if is_ai_integration or is_content_creation:
        agents.append("python-best-practices-coach")

    # 2. Technology-specific agents
    if has_fastapi:
        agents.append("fastapi-design-coach")
        agents.append("api-design-reviewer")

    if has_database:
        agents.append("database-orm-specialist")

    if has_docker:
        agents.append("docker-infrastructure-guide")

    if has_react:
        agents.append("react-integration-coach")

    if has_testing:
        workflow_description = "Use Test Coverage Strategist for test design, "

    if has_security:
        workflow_description += "Security Hardening Mentor for validation, "

    if has_performance:
        agents.append("performance-optimizer")

    # 3. Module-specific workflows
    if module_num == "1":
        # Module 1: Fundamentals + AI Assistant
        if "Clase 1" in title:
            agents.extend(["python-best-practices-coach"])
        elif "Clase 2" in title:
            workflow_description = "Test Coverage Strategist for test generation, "

    elif module_num == "2":
        # Module 2: Architecture + Clean Code
        workflow_description += "Clean Architecture Enforcer for layering, "
        if not has_fastapi:
            agents.append("fastapi-design-coach")

    elif module_num == "3":
        # Module 3: Security
        workflow_description += "Security Hardening Mentor for security review, "
        if has_fastapi:
            agents.append("api-design-reviewer")

    elif module_num == "4":
        # Module 4: Infrastructure
        if "Clase 3" in title or "Clase 4" in title:
            agents.extend(["database-orm-specialist", "performance-optimizer"])
        elif "Clase 2" in title or has_docker:
            agents.append("docker-infrastructure-guide")

    elif module_num == "5":
        # Module 5: Full-Stack
        agents.extend(["react-integration-coach", "api-design-reviewer", "performance-optimizer"])

    # 4. Game issues
    if is_game:
        agents.extend(["react-integration-coach", "api-design-reviewer", "fastapi-design-coach"])

    # 5. Bug fixes
    if is_bug_fix:
        agents.append("python-best-practices-coach")
        workflow_description += "Debug with profiling tools, "

    # Remove duplicates while preserving order
    seen = set()
    unique_agents = []
    for agent in agents:
        if agent not in seen:
            seen.add(agent)
            unique_agents.append(agent)

    # Build markdown workflow section
    if not unique_agents and not workflow_description:
        return ""

    workflow_md = "\n\n---\n\n## 🤖 Recommended Agent Workflow\n\n"

    if workflow_description:
        workflow_md += f"**Workflow**: {workflow_description.rstrip(', ')}\n\n"

    if unique_agents:
        workflow_md += "**Agents to use** (in order):\n\n"
        for i, agent in enumerate(unique_agents, 1):
            agent_name = agent.replace("-", " ").title()
            workflow_md += f"{i}. **{agent_name}** (`.claude/agents/educational/{agent}.md`)\n"

        workflow_md += "\n**How to use**:\n"
        workflow_md += "1. Review existing code/content with each agent\n"
        workflow_md += "2. Address feedback and anti-patterns identified\n"
        workflow_md += "3. Iterate until agents approve (no critical issues)\n"
        workflow_md += "4. Document learnings in commit message\n"

    return workflow_md


def priority_to_number(priority_str: str) -> int:
    """Convert priority string (P0, P1, etc.) to Linear priority number."""
    mapping = {
        "P0": 0,  # Urgent
        "P1": 1,  # High
        "P2": 2,  # Medium
        "P3": 3   # Low
    }
    return mapping.get(priority_str, 3)


def setup_labels(api: LinearAPI, team_id: str) -> dict[str, str]:
    """Create all necessary labels and return mapping of name -> ID."""
    print("\n📋 Setting up labels...")

    # Use pre-existing label IDs provided by user
    label_map = {
        # Modules
        "module-1": "3e781400-6c0e-4797-a399-fdbdb8ff3699",
        "module-2": "01def120-73a8-4e2b-ab09-496f747118db",
        "module-3": "3d653956-9d0c-4d9b-b909-03c72654543d",
        "module-4": "d8b71ba9-d9ea-4615-9858-fa9c81641434",
        "module-5": "ab5b4c45-e01b-4670-94e5-4a490c82b60a",

        # Types
        "content-creation": "e726e4c4-8ab3-4c27-abde-5fdf35d8211f",
        "ai-integration": "c3b87c19-deb6-4976-a86e-8310680c15bc",
        "bug-fix": "5a1d9058-6453-49fb-871f-defe3e5d45bd",
        "documentation": "e5fb6f1b-d60c-4b2b-8f83-dc8c5681bdb6",
        "game": "44124dd8-677b-4998-bcd4-7226c502cb02",

        # Priorities
        "P0-critical": "23379306-9a94-4f05-9c14-8b89362db644",
        "P1-high": "d4df4574-568a-47ac-852a-fb30f60369b8",
        "P2-medium": "2619d671-acb8-42c0-ae59-4f1fba9800c0",
        "P3-low": "cde37e07-5d16-484e-9baf-defadee3dab7",
    }

    print(f"✅ Labels ready: {len(label_map)} pre-existing labels")
    return label_map


def main():
    """Main function to create all Linear issues."""
    print("🚀 Linear Issues Creator")
    print("=" * 60)

    # Validate environment
    if not LINEAR_API_KEY:
        print("❌ ERROR: LINEAR_API_KEY not found in environment")
        print("   Create a .env file with your Linear API key")
        print("   Get your key from: https://linear.app/settings/api")
        return

    # Initialize API client
    api = LinearAPI(LINEAR_API_KEY)

    # Issues already created (to skip)
    ALREADY_CREATED = [
        "M2-1",  # JAR-201
        "M3-2",  # JAR-202
        "M4-3",  # JAR-203
        "M4-4",  # JAR-204
        "M5-5",  # JAR-205
        "M5-6",  # JAR-206
        "M1-1",  # JAR-207
        "M1-2",  # JAR-208
    ]

    try:
        # Use pre-configured IDs
        print(f"\n✅ Using Team: {TEAM_KEY} (ID: {TEAM_ID})")
        print(f"✅ Using Project: {PROJECT_NAME} (ID: {PROJECT_ID})")

        # Setup labels
        label_map = setup_labels(api, TEAM_ID)

        # Parse issues from master plan
        # Get absolute path to master plan
        script_dir = Path(__file__).parent
        plan_file = script_dir.parent / "docs" / "LINEAR_ISSUES_MASTER_PLAN.md"

        print(f"\n📖 Parsing master plan: {plan_file}")
        all_issues = parse_master_plan(str(plan_file))

        # Filter out already created issues
        issues = []
        skipped = []
        for issue in all_issues:
            issue_id = issue.title.split(":")[0]
            if issue_id in ALREADY_CREATED:
                skipped.append(issue_id)
            else:
                issues.append(issue)

        print(f"✅ Found {len(all_issues)} total issues")
        print(f"⏭️  Skipped {len(skipped)} already created: {', '.join(skipped)}")
        print(f"🎯 Creating {len(issues)} remaining issues")

        # Sort issues by priority (P0 first, then P1, P2, P3)
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        issues.sort(key=lambda x: priority_order.get(x.priority, 4))
        print("✅ Issues sorted by priority (P0 → P1 → P2 → P3)")

        # Create issues in batches
        print("\n🎯 Creating issues in priority order...")
        print("=" * 60)

        created_count = 0
        failed_count = 0

        for idx, issue in enumerate(issues, 1):
            try:
                # Map label names to IDs
                label_ids = []
                for label_name in issue.labels:
                    if label_name in label_map:
                        label_ids.append(label_map[label_name])
                    else:
                        # Try to create label on the fly
                        label_id = api.get_or_create_label(TEAM_ID, label_name)
                        label_map[label_name] = label_id
                        label_ids.append(label_id)

                # Add priority label
                priority_label = f"{issue.priority}-{'critical' if issue.priority == 'P0' else 'high' if issue.priority == 'P1' else 'medium' if issue.priority == 'P2' else 'low'}"
                if priority_label in label_map:
                    label_ids.append(label_map[priority_label])

                # Convert priority to number
                priority_num = priority_to_number(issue.priority)

                # Create issue
                issue_id, identifier = api.create_issue(
                    team_id=TEAM_ID,
                    project_id=PROJECT_ID,
                    title=issue.title,
                    description=issue.description,
                    label_ids=label_ids,
                    priority=priority_num
                )

                created_count += 1
                print(f"✅ [{idx}/{len(issues)}] Created: {identifier} - {issue.title[:50]}...")

                # Rate limiting: sleep between requests
                time.sleep(0.5)

                # Report progress every 5 issues
                if idx % 5 == 0:
                    print(f"\n📊 Progress: {created_count}/{len(issues)} issues created")
                    print("-" * 60)

            except Exception as e:
                failed_count += 1
                print(f"❌ [{idx}/{len(issues)}] Failed: {issue.title[:50]}...")
                print(f"   Error: {str(e)}")

        # Final summary
        print("\n" + "=" * 60)
        print("🎉 SUMMARY")
        print("=" * 60)
        print(f"✅ Successfully created: {created_count}/{len(issues)} issues")
        if failed_count > 0:
            print(f"❌ Failed: {failed_count} issues")
        print(f"\n🔗 View project: https://linear.app/team/{TEAM_KEY}/project/{PROJECT_NAME.lower().replace(' ', '-')}")

    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
