# automation/refresh_tableau.py
"""
Automates Tableau dashboard refresh using Tableau Server / Tableau Public API.
Update placeholders with your credentials and project details.
"""

import os
import pandas as pd
from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils.querying import get_projects_dataframe

# ==============================
# STEP 1: Update these variables
# ==============================
# Allow overrides via environment variables for safer automation (recommended)
TABLEAU_SERVER_URL = os.getenv('TABLEAU_SERVER_URL', "https://prod-apnortheast-a.online.tableau.com")
# Common env names supported
SITE_NAME = os.getenv('TABLEAU_SITE_NAME', os.getenv('SITE_NAME', "your_site_name"))  # Tableau site name
TABLEAU_USERNAME = os.getenv('TABLEAU_USERNAME', "your_email@example.com")  # Tableau login email
TABLEAU_PASSWORD = os.getenv('TABLEAU_PASSWORD', "your_password_or_token")  # Tableau password or API token
PROJECT_NAME = os.getenv('TABLEAU_PROJECT_NAME', os.getenv('PROJECT_NAME', "Banking Insights Dashboard"))  # Tableau project folder name
DATA_SOURCE_NAME = os.getenv('TABLEAU_DATA_SOURCE_NAME', os.getenv('DATA_SOURCE_NAME', "merged_dataset"))  # Published data source name

# ==============================
# STEP 2: Authenticate
# ==============================

# Basic credential checks to fail fast with a clear message
missing = []
for var_name, var_value in [
    ('TABLEAU_SERVER_URL', TABLEAU_SERVER_URL),
    ('TABLEAU_USERNAME', TABLEAU_USERNAME),
    ('TABLEAU_PASSWORD', TABLEAU_PASSWORD),
    ('SITE_NAME', SITE_NAME),
    ('PROJECT_NAME', PROJECT_NAME),
    ('DATA_SOURCE_NAME', DATA_SOURCE_NAME)
]:
    if not var_value or 'your_' in str(var_value) or 'example' in str(var_value):
        missing.append(var_name)

if missing:
    raise SystemExit(f"Missing or placeholder Tableau configuration variables: {missing}. Please update the top of the script with real credentials and names.")

connection = TableauServerConnection(
    {
        "tableau_prod": {
            "server": TABLEAU_SERVER_URL,
            "api_version": "3.26",
            "username": TABLEAU_USERNAME,
            "password": TABLEAU_PASSWORD,
            "site_name": SITE_NAME,
            "site_url": SITE_NAME
        }
    },
    env="tableau_prod"
)

connection.sign_in()
print("✅ Connected to Tableau Server successfully!")

# If environment variables were used, log which ones are set (avoid printing secrets)
env_set = [k for k in ['TABLEAU_SERVER_URL', 'TABLEAU_SITE_NAME', 'TABLEAU_USERNAME', 'TABLEAU_PROJECT_NAME', 'TABLEAU_DATA_SOURCE_NAME'] if os.getenv(k)]
if env_set:
    print(f"Using environment variables for: {env_set}")

# ==============================
# STEP 3: Refresh the published data source
# ==============================
from tableau_api_lib.exceptions.tableau_server_exceptions import PaginationError

try:
    all_projects = get_projects_dataframe(connection)
except PaginationError:
    # Some server responses are non-paginated; fall back to direct query_projects() and build a DataFrame
    resp = connection.query_projects()

    # Try JSON first, then fallback to XML parsing (Tableau may return XML)
    projects = None
    try:
        data = resp.json()
        if isinstance(data, dict):
            if 'projects' in data and isinstance(data['projects'], dict) and 'project' in data['projects']:
                projects = data['projects']['project']
            elif 'projects' in data and isinstance(data['projects'], list):
                projects = data['projects']
            elif 'project' in data:
                projects = data['project']
    except Exception:
        # Not JSON; attempt XML parsing
        try:
            import xml.etree.ElementTree as ET
            text = getattr(resp, 'text', str(resp))
            root = ET.fromstring(text)
            projects = []
            for elem in root.iter():
                tag = elem.tag
                if tag.lower().endswith('project'):
                    attrib = elem.attrib
                    proj = {}
                    if 'id' in attrib:
                        proj['id'] = attrib.get('id')
                    if 'name' in attrib:
                        proj['name'] = attrib.get('name')
                    # sometimes name is a child element
                    for child in elem:
                        if child.tag.lower().endswith('name') and child.text:
                            proj['name'] = child.text
                    projects.append(proj)
            if not projects:
                projects = None
        except Exception:
            projects = None

    if projects is None:
        # Provide more debugging info to help the user
        resp_text = getattr(resp, 'text', None)
        snippet = resp_text[:1000] if isinstance(resp_text, str) else str(resp)
        raise RuntimeError(f'Could not parse projects from Tableau response; check connection and permissions. Response snippet:\n{snippet}')

    all_projects = pd.DataFrame(projects)

# Safely lookup project id
matching = all_projects[all_projects.get('name') == PROJECT_NAME]
if matching.empty:
    raise ValueError(f"Project named '{PROJECT_NAME}' not found on the server. Available projects: {all_projects.get('name').tolist()}")

project_id = matching.iloc[0].get('id')

# Trigger data source refresh
try:
    connection.refresh_data_source(data_source_name=DATA_SOURCE_NAME, project_id=project_id)
    print(f"🔁 Tableau Data Source '{DATA_SOURCE_NAME}' refreshed successfully!")
except Exception as e:
    # Provide a helpful error message including any response snippet
    detail_text = ''
    try:
        resp = getattr(e, 'response', None)
        if resp is None:
            # tableau_api_lib sometimes raises exceptions without a .response attribute
            detail_text = str(e)
        else:
            try:
                detail_text = resp.text
            except Exception:
                detail_text = str(resp)
    except Exception:
        detail_text = str(e)
    raise RuntimeError(f"Failed to refresh data source: {detail_text}") from e

# ==============================
# STEP 4: Sign out
# ==============================
connection.sign_out()
print("👋 Signed out from Tableau API")
