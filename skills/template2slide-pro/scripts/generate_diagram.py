#!/usr/bin/env python3
"""
Generate architecture diagram from proposal template
Streamlined workflow: Read .md → Generate Mermaid → Render to PNG

Usage:
    python3 generate_diagram.py <template.md> <output.png>

Example:
    python3 generate_diagram.py Leda_Inio_Safety_Analytics_template.md architecture_diagram.png
"""

import sys
import re
import subprocess
from pathlib import Path


def extract_deployment_info(content: str) -> dict:
    """
    Extract deployment information from template markdown

    Returns:
        dict with keys: deployment_method, cameras, ai_workstations, components
    """
    info = {
        'deployment_method': 'on-premise',  # default
        'cameras': 0,
        'has_cloud': False,
        'has_local_storage': False,
        'components': []
    }

    # Extract deployment method
    deploy_match = re.search(r'##\s*Deployment\s*Method.*?\n(.*?)(?=\n##|\Z)', content, re.IGNORECASE | re.DOTALL)
    if deploy_match:
        deploy_text = deploy_match.group(1).lower()
        if 'cloud' in deploy_text:
            info['deployment_method'] = 'cloud'
            info['has_cloud'] = True
        elif 'hybrid' in deploy_text:
            info['deployment_method'] = 'hybrid'
            info['has_cloud'] = True
            info['has_local_storage'] = True
        else:
            info['deployment_method'] = 'on-premise'
            info['has_local_storage'] = True

    # Extract number of cameras
    camera_matches = re.findall(r'(\d+)\s*cameras?', content, re.IGNORECASE)
    if camera_matches:
        info['cameras'] = int(camera_matches[0])

    # Extract AI workstations
    if 'AI workstation' in content or 'workstation' in content:
        info['components'].append('AI Workstation')

    if 'Dashboard' in content or 'Monitoring' in content:
        info['components'].append('Dashboard')

    if 'Alert' in content or 'Notification' in content:
        info['components'].append('Alert System')

    return info


def generate_mermaid_code(info: dict, project_name: str) -> str:
    """
    Generate Mermaid diagram code based on deployment information

    Args:
        info: Deployment information dict
        project_name: Name of the project

    Returns:
        Mermaid diagram code as string
    """
    deployment = info['deployment_method']
    cameras = info['cameras']

    if deployment == 'cloud':
        mermaid = f"""graph LR
    subgraph OnSite["On-Site (Customer)"]
        Cameras["{cameras} IP Cameras<br/>RTSP Streaming"]
    end

    subgraph Cloud["Cloud (viAct Infrastructure)"]
        direction TB
        AI["AI Processing<br/>Scalable Cloud"]
        Storage["Cloud Storage<br/>Data Retention"]
        API["API Gateway<br/>Management"]
    end

    Dashboard["Web Dashboard<br/>Browser Access"]
    Alert["Alert/Notification<br/>Email & Telegram"]

    Cameras ==>|Internet| AI
    AI --> Storage
    AI --> API
    API --> Dashboard
    API --> Alert

    classDef default fill:#00AEEF,stroke:#000,stroke-width:2px,color:#fff
    classDef cloud fill:#4A90E2,stroke:#000,stroke-width:2px,color:#fff
    class Cameras,Dashboard,Alert default
    class AI,Storage,API cloud
"""
    elif deployment == 'hybrid':
        mermaid = f"""graph LR
    subgraph OnSite["On-Site Infrastructure"]
        direction TB
        Cameras["{cameras} IP Cameras<br/>RTSP Streaming"]
        LocalAI["Local AI Inference<br/>Real-time Processing"]
        LocalStorage["Local Storage<br/>Buffer & Backup"]
    end

    subgraph Cloud["Cloud Services"]
        direction TB
        CloudAI["Cloud AI Training<br/>Model Updates"]
        CloudStorage["Cloud Storage<br/>Long-term Archive"]
        Management["Management Portal<br/>Remote Access"]
    end

    Dashboard["Local Dashboard<br/>On-site Monitoring"]
    Alert["Alert System<br/>Multi-channel"]

    Cameras --> LocalAI
    LocalAI --> LocalStorage
    LocalAI --> Dashboard
    LocalAI --> Alert

    LocalStorage <-->|Sync| CloudStorage
    LocalAI <-->|Model Updates| CloudAI
    Dashboard <-->|Remote Access| Management

    classDef default fill:#00AEEF,stroke:#000,stroke-width:2px,color:#fff
    classDef cloud fill:#4A90E2,stroke:#000,stroke-width:2px,color:#fff
    class Cameras,LocalAI,LocalStorage,Dashboard,Alert default
    class CloudAI,CloudStorage,Management cloud
"""
    else:  # on-premise
        mermaid = f"""graph LR
    subgraph OnSite["On-Site Infrastructure"]
        direction TB
        Cameras["{cameras} IP Cameras<br/>RTSP Streaming"]

        subgraph Network["Local Area Network (LAN)"]
            direction LR
            AIInference["AI Inference Workstation<br/>NVIDIA GPU"]
            AITraining["AI Training Workstation<br/>Model Updates"]
            Dashboard["Dashboard Workstation<br/>Local Monitoring"]
        end

        LocalStorage["Local Storage Server<br/>Video Retention"]
    end

    Internet["Internet Connection<br/>(Updates & Support Only)"]
    Alert["Alert/Notification<br/>Email & Telegram"]

    Cameras --> AIInference
    AIInference --> Dashboard
    AIInference --> LocalStorage
    AITraining -.->|Model Updates| AIInference

    Dashboard --> Alert
    Internet -.->|Support| AITraining

    classDef default fill:#00AEEF,stroke:#000,stroke-width:2px,color:#fff
    classDef storage fill:#7B68EE,stroke:#000,stroke-width:2px,color:#fff
    class Cameras,AIInference,AITraining,Dashboard,Alert,Internet default
    class LocalStorage storage
"""

    return mermaid


def render_mermaid_to_png(mermaid_code: str, output_path: str) -> bool:
    """
    Render Mermaid code to PNG using mermaid-cli

    Args:
        mermaid_code: Mermaid diagram code
        output_path: Output PNG file path

    Returns:
        True if successful, False otherwise
    """
    try:
        # Write mermaid code to temporary file
        temp_mmd = Path('/tmp/temp_diagram.mmd')
        temp_mmd.write_text(mermaid_code)

        # Run mermaid-cli with puppeteer args for Linux
        result = subprocess.run(
            ['npx', '@mermaid-js/mermaid-cli',
             '-i', str(temp_mmd),
             '-o', output_path,
             '-t', 'dark',
             '-b', 'transparent',
             '-p', 'puppeteerLaunchArgs.executablePath=/usr/bin/chromium-browser'],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Clean up temp file
        temp_mmd.unlink()

        if result.returncode == 0:
            return True
        else:
            print(f"Mermaid rendering error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("Error: Mermaid rendering timed out")
        return False
    except Exception as e:
        print(f"Error rendering Mermaid diagram: {e}")
        return False


def main(template_path: str, output_path: str = None):
    """
    Main function to generate architecture diagram from template

    Args:
        template_path: Path to template markdown file
        output_path: Path to output PNG file (optional)
    """
    template_file = Path(template_path)

    if not template_file.exists():
        print(f"Error: Template file not found: {template_path}")
        return 1

    # Read template
    content = template_file.read_text()

    # Extract deployment information
    info = extract_deployment_info(content)
    project_name = template_file.stem.replace('_template', '').replace('_template', '')

    # Generate Mermaid code
    mermaid_code = generate_mermaid_code(info, project_name)

    # Save Mermaid code for reference
    mermaid_file = template_file.parent / f"{project_name}_architecture_diagram.md"
    mermaid_file.write_text(mermaid_code)
    print(f"✅ Mermaid code saved to: {mermaid_file}")

    # Determine output path
    if output_path is None:
        output_path = template_file.parent / f"{project_name}_architecture_diagram.png"
    else:
        output_path = Path(output_path)

    # Render to PNG
    print("🎨 Rendering diagram to PNG...")
    success = render_mermaid_to_png(mermaid_code, str(output_path))

    if success:
        print(f"✅ Diagram saved to: {output_path}")
        return 0
    else:
        print("❌ Failed to render diagram")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_diagram.py <template.md> [output.png]")
        sys.exit(1)

    template_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    sys.exit(main(template_path, output_path))
