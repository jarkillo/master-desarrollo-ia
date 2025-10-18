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
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")
LINEAR_API_URL = "https://api.linear.app/graphql"
TEAM_KEY = os.getenv("LINEAR_TEAM_KEY", "TEAM")  # Your team key (e.g., "ENG")
PROJECT_NAME = "Master desarrollo con IA"

@dataclass
class Issue:
    """Represents a Linear issue to create."""
    title: str
    description: str
    labels: List[str]
    priority: str  # P0, P1, P2, P3
    estimate: str  # 1-2h, 3-4h, etc.
    module: str

class LinearAPI:
    """Linear GraphQL API client."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }

    def execute_query(self, query: str, variables: Optional[Dict] = None) -> Dict:
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
        label_ids: List[str],
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


def parse_master_plan(file_path: str) -> List[Issue]:
    """Parse LINEAR_ISSUES_MASTER_PLAN.md and extract issues."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    current_module = None

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
        labels = [l.strip().strip('`') for l in labels_str.split(',')]

        issues.append(Issue(
            title=title,
            description=body,
            labels=labels,
            priority=priority_str,
            estimate=estimate,
            module=module
        ))

    return issues


def priority_to_number(priority_str: str) -> int:
    """Convert priority string (P0, P1, etc.) to Linear priority number."""
    mapping = {
        "P0": 0,  # Urgent
        "P1": 1,  # High
        "P2": 2,  # Medium
        "P3": 3   # Low
    }
    return mapping.get(priority_str, 3)


def setup_labels(api: LinearAPI, team_id: str) -> Dict[str, str]:
    """Create all necessary labels and return mapping of name -> ID."""
    print("\n📋 Setting up labels...")

    label_colors = {
        # Modules
        "module-0": "#00FF00",  # Green
        "module-1": "#0000FF",  # Blue
        "module-2": "#8B00FF",  # Violet
        "module-3": "#FFA500",  # Orange
        "module-4": "#FF0000",  # Red
        "module-5": "#FF69B4",  # Pink

        # Types
        "content-creation": "#FFFF00",  # Yellow
        "ai-integration": "#00FFFF",    # Cyan
        "bug-fix": "#FF0000",           # Red
        "documentation": "#808080",     # Gray
        "game": "#800080",              # Purple
        "security": "#DC143C",          # Crimson

        # Priorities
        "P0-critical": "#8B0000",  # Dark Red
        "P1-high": "#FFA500",      # Orange
        "P2-medium": "#FFFF00",    # Yellow
        "P3-low": "#00FF00",       # Green
    }

    label_map = {}
    for label_name, color in label_colors.items():
        label_id = api.get_or_create_label(team_id, label_name, color)
        label_map[label_name] = label_id

    print(f"✅ Labels ready: {len(label_map)} labels")
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

    try:
        # Get team ID
        print(f"\n🔍 Finding team: {TEAM_KEY}")
        team_id = api.get_team_id(TEAM_KEY)
        print(f"✅ Team found: {team_id}")

        # Get or create project
        print(f"\n🔍 Finding/creating project: {PROJECT_NAME}")
        project_id = api.get_or_create_project(team_id, PROJECT_NAME)

        # Setup labels
        label_map = setup_labels(api, team_id)

        # Parse issues from master plan
        plan_file = "../docs/LINEAR_ISSUES_MASTER_PLAN.md"
        print(f"\n📖 Parsing master plan: {plan_file}")
        issues = parse_master_plan(plan_file)
        print(f"✅ Found {len(issues)} issues to create")

        # Create issues in batches
        print(f"\n🎯 Creating issues...")
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
                        label_id = api.get_or_create_label(team_id, label_name)
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
                    team_id=team_id,
                    project_id=project_id,
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
