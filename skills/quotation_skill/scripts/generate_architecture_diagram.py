#!/usr/bin/env python3
"""
Simplified Mermaid Diagram Generator for quotation_skill
High-level guide: template.md -> Mermaid code -> .png diagram

NO JSON, NO REGEX - Simple, readable Python
"""

class SimpleArchitectureGenerator:
    """Generate Mermaid architecture diagrams from template.md data"""

    def __init__(self, deployment_method, num_cameras, ai_modules, deployment_details=None):
        """
        Initialize with data from template.md

        Args:
            deployment_method: 'on-prem', 'cloud', or 'hybrid'
            num_cameras: Number of cameras (int)
            ai_modules: List of AI module names
            deployment_details: Dict with optional details (alert_methods, include_nvr, etc.)
        """
        self.deployment_method = deployment_method.lower()
        self.num_cameras = num_cameras
        self.ai_modules = ai_modules
        self.details = deployment_details or {}

        # Set defaults
        self.alert_methods = self.details.get('alert_methods', ['Email', 'Dashboard'])
        self.include_nvr = self.details.get('include_nvr', False)
        self.compact_mode = self.details.get('compact_mode', True)

    def _format_ai_modules_inline(self):
        """Format AI modules as inline list (compact display)"""
        if not self.ai_modules:
            return ""

        # Remove common suffixes and shorten
        short_modules = []
        for module in self.ai_modules:
            # Remove parenthetical text
            import re
            short_name = re.sub(r'\s*\([^)]*\)\s*$', '', module.strip())
            # Truncate if too long
            if len(short_name) > 40:
                short_name = short_name[:37] + "..."
            short_modules.append(short_name)

        return "<br/>".join(short_modules)

    def generate_on_premise(self):
        """Generate On-Premise Architecture Diagram"""

        # Build camera node
        camera_node = f'Cameras["Up to {self.num_cameras} Cameras<br/>IP-based Camera"]'

        # Build NVR node (optional)
        nvr_node = ''
        nvr_connection = ''
        if self.include_nvr:
            nvr_node = 'NVR["Network Video Recorder<br/>(NVR)*"]'
            nvr_connection = 'Cameras -->|RTSP Links| NVR\n    NVR -->|RTSP Links| AI_Inference'
        else:
            nvr_connection = 'Cameras -->|RTSP Links| AI_Inference'

        # Build AI Inference node
        if self.compact_mode and self.ai_modules:
            ai_modules_text = self._format_ai_modules_inline()
            ai_inference = f'AI_Inference["AI Inference<br/>(On-Premise Processing)<br/>{ai_modules_text}"]'
        else:
            ai_inference = 'AI_Inference["AI Inference<br/>(On-Premise Processing)"]'

        # Build other nodes
        ai_training = 'AI_Training["AI Training<br/>(On-Premise)"]'
        dashboard = 'Dashboard["Local Dashboard"]'
        alert_list = ' & '.join(self.alert_methods)
        alert_system = f'Alert["Alert/Notification<br/>({alert_list})"]'

        # Generate Mermaid code
        mermaid = f"""graph TB
    subgraph "On-Premise Infrastructure"
        {camera_node}
        {nvr_node}
        {ai_training}
        {ai_inference}
        {dashboard}
        {alert_system}
    end

    {nvr_connection}
    AI_Training -->|Trained Models| AI_Inference
    AI_Inference -->|Detection Results| Dashboard
    AI_Inference -->|Alerts| Alert

    style AI_Training fill:#e1f5ff,stroke:#01579b,stroke-width:2px,color:#000000
    style AI_Inference fill:#81d4fa,stroke:#0277bd,stroke-width:2px,color:#000000
    style Dashboard fill:#fff4e1,stroke:#e65100,stroke-width:2px,color:#000000
    style Alert fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#000000
    style Cameras fill:#ffffff,stroke:#424242,stroke-width:2px,color:#000000"""

        return mermaid

    def generate_cloud(self):
        """Generate Cloud Architecture Diagram"""

        # On-site components
        camera_node = f'Cameras["Up to {self.num_cameras} Cameras<br/>IP-based Camera"]'

        # Internet connection
        internet = 'Internet["Internet Connection<br/>(Provided by Client)"]'

        # NVR (optional)
        nvr_node = ''
        nvr_connection = ''
        if self.include_nvr:
            nvr_node = 'NVR["NVR"]'
            nvr_connection = 'Cameras --> NVR\n    NVR -->|RTSP Links| Internet'
        else:
            nvr_connection = 'Cameras -->|RTSP Links| Internet'

        # Cloud components
        if self.compact_mode and self.ai_modules:
            ai_modules_text = self._format_ai_modules_inline()
            cloud_inference = f'Cloud_Inference["On-cloud in AWS<br/>(viAct\'s CMP)<br/>{ai_modules_text}"]'
        else:
            cloud_inference = 'Cloud_Inference["On-cloud in AWS<br/>(viAct\'s CMP)"]'

        dashboard = 'Dashboard["Centralized Dashboard"]'
        alert_list = ' & '.join(self.alert_methods)
        alert_system = f'Alert["Alert/Notification<br/>({alert_list})"]'
        hse_manager = 'HSE_Manager["HSE Manager"]'

        # Generate Mermaid code
        mermaid = f"""graph LR
    subgraph "On-Site Infrastructure"
        direction TB
        {camera_node}
        {nvr_node}
        {internet}
    end

    subgraph "On-Cloud"
        direction LR
        subgraph "Cloud Infrastructure"
            direction TB
            {cloud_inference}
        end

        subgraph "Output Services"
            direction TB
            {dashboard}
            {alert_system}
        end
    end

    {hse_manager}

{nvr_connection}
    Internet --> Cloud_Inference
    Cloud_Inference --> Dashboard
    HSE_Manager --> Dashboard

    style Cloud_Inference fill:#81d4fa,stroke:#0277bd,stroke-width:3px,color:#000000
    style Dashboard fill:#fff4e1,stroke:#e65100,stroke-width:2px,color:#000000
    style Alert fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#000000
    style HSE_Manager fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#000000
    style Internet fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000000
    style Cameras fill:#ffffff,stroke:#424242,stroke-width:2px,color:#000000"""

        return mermaid

    def generate(self):
        """Generate Mermaid code based on deployment method"""

        if self.deployment_method in ['on-prem', 'on-premise']:
            return self.generate_on_premise()
        elif self.deployment_method == 'cloud':
            return self.generate_cloud()
        else:
            # Default to on-premise for hybrid
            return self.generate_on_premise()


# ============================================================================
# HIGH-LEVEL GUIDE: How to Use This Generator
# ============================================================================

"""
STEP 1: Extract data from template.md
--------------------------------------
From the "SYSTEM ARCHITECTURE" section:

Example for Leda Inio:
- Deployment Method: "On-Premise"
- Camera Number: 9 cameras
- AI Modules: ["Helmet Detection", "Safety Mask Detection", "Hi-vis vest detection",
              "Fire & Smoke Detection", "Human Down Detection"]

STEP 2: Create generator instance
----------------------------------
generator = SimpleArchitectureGenerator(
    deployment_method='on-prem',
    num_cameras=9,
    ai_modules=['Helmet Detection', 'Safety Mask Detection', 'Hi-vis vest detection',
                'Fire & Smoke Detection', 'Human Down Detection'],
    deployment_details={
        'alert_methods': ['Dashboard', 'Email', 'Telegram'],
        'include_nvr': False,
        'compact_mode': True
    }
)

STEP 3: Generate Mermaid code
-------------------------------
mermaid_code = generator.generate()

STEP 4: Save to .mmd file
----------------------------
with open('architecture.mmd', 'w') as f:
    f.write(mermaid_code)

STEP 5: Convert to PNG using mmdc
----------------------------------
Run command:
    mmdc -i architecture.mmd -o architecture.png -b transparent -t dark

This will create architecture.png that can be inserted into HTML slide!
"""


if __name__ == "__main__":
    # Example: Generate diagram for Leda Inio
    generator = SimpleArchitectureGenerator(
        deployment_method='on-prem',
        num_cameras=9,
        ai_modules=[
            'Helmet Detection',
            'Safety Mask Detection',
            'Hi-vis vest detection',
            'Fire & Smoke Detection',
            'Human Down Detection'
        ],
        deployment_details={
            'alert_methods': ['Dashboard', 'Email', 'Telegram'],
            'include_nvr': False,
            'compact_mode': True
        }
    )

    mermaid_code = generator.generate()

    print("=" * 80)
    print("GENERATED MERMAID CODE")
    print("=" * 80)
    print(mermaid_code)
    print("=" * 80)
    print("\nTo convert to PNG:")
    print("  mmdc -i architecture.mmd -o architecture.png -b transparent -t dark")
