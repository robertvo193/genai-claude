---
name: train-model
description: Train computer vision models using natural language. Auto-detects dataset, selects model, trains end-to-end. Use cases: PPE detection, danger zone, safety monitoring.
version: 1.0.0
author: Claude Code
requirements:
  - ultralytics>=8.0.0
  - pyyaml>=6.0
  - pillow>=10.0.0
  - torch>=2.0.0
---

# Train Model Skill Implementation

## Quick Start

```bash
# Install dependencies
pip install ultralytics pyyaml pillow torch

# Train a model
/train-model i want to train a model for PPE detection

# With explicit dataset
/train-model i want to train a model for danger zone detection with dataset ./linde-mexico-data
```

## Implementation Structure

```
~/.claude/skills/train-model/
├── skill.md          # This file
├── intent_parser.py  # Parse natural language requests
├── survey_agent.py   # Dataset analysis
├── design_agent.py   # Model selection
├── planning_agent.py # Execution planning
├── execution_agent.py# Training execution
├── evaluation_agent.py# Performance evaluation
└── orchestrator.py   # Main coordinator
```

## Core Components

### 1. Intent Parser

Extracts use case, dataset path, and requirements from natural language.

```python
class IntentParser:
    def parse(self, user_input: str) -> dict:
        return {
            'use_case': self._extract_use_case(user_input),
            'dataset_path': self._extract_dataset(user_input),
            'priority': self._extract_priority(user_input),
            'output_path': self._extract_output(user_input)
        }
```

### 2. Survey Agent

Analyzes dataset characteristics.

```python
class SurveyAgent:
    def survey(self, dataset_path: str) -> dict:
        return {
            'format': self._detect_format(dataset_path),
            'num_images': self._count_images(dataset_path),
            'classes': self._extract_classes(dataset_path),
            'distribution': self._analyze_distribution(dataset_path)
        }
```

### 3. Design Agent

Selects optimal model and hyperparameters.

```python
class DesignAgent:
    def design(self, survey_results: dict, requirements: dict) -> dict:
        return {
            'model': self._select_model(survey_results, requirements),
            'hyperparams': self._configure_hyperparams(survey_results)
        }
```

### 4. Planning Agent

Creates execution plan with time and resource estimates.

```python
class PlanningAgent:
    def plan(self, design: dict) -> dict:
        return {
            'steps': self._breakdown_steps(design),
            'time_estimate': self._estimate_time(design),
            'resources': self._check_resources(design)
        }
```

### 5. Execution Agent

Executes model training with progress monitoring.

```python
class ExecutionAgent:
    def execute(self, plan: dict) -> dict:
        from ultralytics import YOLO

        # Create data.yaml
        self._create_data_yaml(plan)

        # Initialize and train model
        model = YOLO(plan['model'])
        results = model.train(**plan['hyperparams'])

        return {'model_path': results.save_dir}
```

### 6. Evaluation Agent

Evaluates model performance and generates report.

```python
class EvaluationAgent:
    def evaluate(self, model_path: str, dataset_path: str) -> dict:
        from ultralytics import YOLO

        model = YOLO(model_path)
        metrics = model.val()

        return {
            'mAP50': metrics.box.map50,
            'mAP50_95': metrics.box.map,
            'precision': metrics.box.mp,
            'recall': metrics.box.mr
        }
```

### 7. Orchestrator

Coordinates all agents.

```python
class TrainingOrchestrator:
    def run(self, user_request: str) -> dict:
        # Phase 1: Parse intent
        intent = self.intent_parser.parse(user_request)

        # Phase 2: Survey dataset
        survey = self.survey_agent.survey(intent['dataset_path'])

        # Phase 3: Design pipeline
        design = self.design_agent.design(survey, intent)

        # Phase 4: Create plan
        plan = self.planning_agent.plan(design)

        # Phase 5: Execute training
        results = self.execution_agent.execute(plan)

        # Phase 6: Evaluate
        evaluation = self.evaluation_agent.evaluate(results['model_path'])

        return evaluation
```

## Usage Examples

See `/train-model` command documentation for complete examples.
