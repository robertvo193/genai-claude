# Claude Code Global Workflow - Complete Guide

## Overview

Your `.claude` global directory contains a sophisticated custom workflow system built on top of Claude Code. This system provides structured workflows, skills, commands, and protocols for enhanced development productivity.

**Location**: `~/.claude/`

**Last Updated**: 2025-01-27

---

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [Core Components](#core-components)
3. [Workflow System](#workflow-system)
4. [Commands](#commands)
5. [Skills](#skills)
6. [CLI Tools Integration](#cli-tools-integration)
7. [Protocols](#protocols)
8. [Configuration](#configuration)

---

## Directory Structure

```
~/.claude/
├── CLAUDE.md                              # Main global instructions
├── settings.json                          # Environment & hooks config
├── version.json                           # Version tracking
│
├── workflows/                             # Core workflow definitions
│   ├── workflow-architecture.md           # Complete workflow system design
│   ├── cli-tools-usage.md                 # CLI execution specification
│   ├── coding-philosophy.md               # Development principles
│   ├── context-tools.md                   # Tool usage priorities
│   ├── file-modification.md               # File editing workflow
│   └── cli-templates/                     # 19 templates for CLI commands
│       ├── protocols/                     # Analysis & Write protocols
│       ├── planning-roles/                # Role-based templates
│       ├── tech-stacks/                   # Technology stack guides
│       └── memory/                        # Memory context templates
│
├── commands/                              # 108 slash commands
│   ├── ccw.md                            # Main orchestrator
│   ├── ccw-coordinator.md                # CLI coordinator
│   ├── spec-*.md                         # Spec commands (create, execute, list)
│   ├── bug-*.md                          # Bug commands (analyze, create, fix, verify)
│   ├── template.md                       # Template generation
│   ├── quotation.md                      # Quotation generation
│   └── workflow/                         # Workflow commands (30+ files)
│       ├── plan.md
│       ├── lite-plan.md
│       ├── execute.md
│       ├── debug.md
│       ├── review.md
│       ├── tdd-plan.md
│       ├── test-gen.md
│       ├── brainstorm/                   # Brainstorming workflows
│       ├── session/                      # Session management
│       ├── ui-design/                    # UI design workflows
│       └── tools/                        # Tool-specific workflows
│
├── skills/                                # 36 skills
│   ├── template/                         # Template generation skill
│   ├── quotation_skill/                  # Quotation generation skill
│   ├── dealtransfer2template/            # Excel → Template conversion
│   ├── pptx/                             # PowerPoint manipulation
│   ├── pdf/                              # PDF manipulation
│   ├── docx/                             # Word document manipulation
│   ├── xlsx/                             # Excel manipulation
│   ├── media-processing/                 # FFmpeg & ImageMagick
│   ├── annotate/                         # Image annotation workflows
│   ├── sam3-detect/                      # SAM3 object detection
│   ├── project-analyze/                  # Multi-phase project analysis
│   ├── review-code/                      # Code review workflows
│   ├── issue-manage/                     # Interactive issue management
│   ├── mcp-builder/                      # MCP server creation
│   ├── skill-creator/                    # Skill creation
│   ├── skill-generator/                  # Meta-skill for skills
│   ├── skill-tuning/                     # Skill optimization
│   ├── copyright-docs/                   # Copyright documentation
│   ├── software-manual/                  # TiddlyWiki manual generation
│   ├── text-formatter/                   # Text formatting
│   ├── ccw-loop/                         # Development loop workflow
│   ├── ccw-help/                         # Command help system
│   ├── google-drive/                     # Google Drive API
│   ├── prompt-enhancer/                  # Prompt transformation
│   └── _shared/                          # Shared skill utilities
│
├── agents/                                # Agent configurations
├── bugs/                                  # Bug tracking
├── config/                                # Configuration files
├── debug/                                 # Debug logs
├── ide/                                   # IDE integrations
├── plugins/                               # Plugin system
├── projects/                              # Project-specific data
├── scripts/                               # Shell scripts
│   └── safety-check.sh                   # Pre-tool-use safety validation
├── session-env/                           # Session environments
├── specs/                                 # Specifications storage
├── steering/                              # Steering configurations
├── templates/                             # Template storage
│   └── .quotation/                        # Quotation templates
│   └── .template/                         # Generation templates
└── todos/                                 # Todo storage
```

---

## Core Components

### 1. CLAUDE.md - Global Instructions

**Location**: `~/.claude/CLAUDE.md`

**Purpose**: Main instruction file that Claude reads on startup

**Key Sections**:

```markdown
- **Coding Philosophy**: References workflow/coding-philosophy.md
- **CLI Endpoints**: References cli-tools.json configuration
- **Tool Execution**:
  - Agent Calls: Use run_in_background: false
  - CLI Tool Calls: Use run_in_background: true
  - CLI Analysis: Wait for completion before actions
  - Auto-Invoke Triggers: Self-repair, ambiguity, architecture decisions
- **Code Diagnostics**: Prefer mcp__ide__getDiagnostics
```

**Critical Rules**:
- Strictly follow cli-tools.json configuration
- Always use TodoWrite for task tracking
- Wait for CLI analysis completion
- Value every CLI call (aggregate results)

### 2. Settings Configuration

**Location**: `~/.claude/settings.json`

**Current Configuration**:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "d4a39a8e8b464ed0adb774b04fd2b2d3.8eqcR4PopFJsaKQH",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": 1
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/scripts/safety-check.sh"
          }
        ]
      }
    ]
  }
}
```

**Features**:
- Custom API endpoint configuration
- Extended timeout (50 minutes)
- Safety check hook before Bash tool execution
- Non-essential traffic disabled

---

## Workflow System

### Architecture Overview

**Location**: `~/.claude/workflows/workflow-architecture.md`

**Key Design Principles**:

1. **JSON-Only Data Model**
   - Task state stored in JSON files (`.task/IMPL-*.json`)
   - Markdown documents are read-only generated views
   - Single source of truth eliminates sync complexity

2. **Marker-Based Session Management**
   - Active sessions: `.workflow/active/WFS-[topic]/`
   - Archived sessions: `.workflow/archives/WFS-[topic]/`
   - Simple directory-based tracking

3. **Unified File Structure**
   - Same structure for all workflows
   - On-demand file creation
   - Maximum 2-level task hierarchy (IMPL-N, IMPL-N.M)

4. **Dynamic Task Decomposition**
   - Subtasks created as needed
   - Flow control with dependencies
   - Agent-agnostic task definitions

### Session Structure

```
.workflow/
├── active/
│   └── WFS-[topic-slug]/
│       ├── workflow-session.json          # Session metadata (REQUIRED)
│       ├── IMPL_PLAN.md                   # Planning document (REQUIRED)
│       ├── TODO_LIST.md                   # Progress tracking (REQUIRED)
│       ├── .task/                         # Task definitions (REQUIRED)
│       │   ├── IMPL-1.json
│       │   └── IMPL-1.1.json
│       ├── .brainstorming/                # Optional brainstorming
│       ├── .chat/                         # CLI sessions
│       ├── .process/                      # Analysis results
│       ├── .summaries/                    # Task summaries
│       └── .review/                       # Code review results
└── archives/
    └── WFS-[completed]/
```

### Task JSON Schema

**Location**: `.workflow/active/WFS-[topic]/.task/IMPL-*.json`

**Structure**:

```json
{
  "id": "IMPL-1.2",
  "title": "Implement feature",
  "status": "pending|active|completed|blocked|container",
  "context_package_path": ".workflow/WFS-session/.process/context-package.json",

  "meta": {
    "type": "feature|bugfix|refactor|test-gen|docs",
    "agent": "@code-developer|@action-planning-agent|@test-fix-agent"
  },

  "context": {
    "requirements": ["requirement1", "requirement2"],
    "focus_paths": ["src/auth", "tests/auth"],
    "acceptance": ["criteria1", "criteria2"],
    "parent": "IMPL-1",
    "depends_on": ["IMPL-1.1"],
    "shared_context": {
      "key": "value"
    }
  },

  "flow_control": {
    "pre_analysis": [
      {
        "step": "load_context",
        "action": "Load context",
        "command": "Read(file.md)",
        "output_to": "context"
      }
    ],
    "implementation_approach": [
      {
        "step": 1,
        "title": "Implementation step",
        "description": "What to do",
        "modification_points": ["file:line"],
        "logic_flow": ["step1", "step2"],
        "depends_on": [],
        "output": "result"
      }
    ],
    "target_files": [
      "src/file.ts:function:100-150"
    ]
  }
}
```

**Key Fields**:
- **status**: Task state
- **meta.type**: Task category
- **meta.agent**: Which agent handles it
- **context.focus_paths**: Concrete project paths
- **flow_control**: Execution instructions with dependencies

### Flow Control System

**Two Formats**:

1. **Inline Format** (Brainstorm workflows)
   - Used by: conceptual-planning-agent
   - Location: In prompt (markdown list)
   - Purpose: Temporary context preparation

2. **JSON Format** (Implementation tasks)
   - Used by: code-developer, test-fix-agent
   - Location: In task JSON file
   - Purpose: Persistent task execution

**Command Types Supported**:
- Bash: `bash(command)`
- Tools: `Read()`, `Glob()`, `Grep()`
- MCP: `mcp__exa__search()`
- CLI: `gemini`, `qwen`, `codex`

**Variable References**: `[variable_name]` for cross-step data flow

---

## Commands

### Command Categories

**Total**: 108 commands

**Location**: `~/.claude/commands/`

### Main Commands

#### 1. `/ccw` - Main Workflow Orchestrator

**File**: `commands/ccw.md`

**Purpose**: Intent analysis → workflow selection → command chain execution

**Features**:
- 5-phase workflow (Analyze → Clarify → Select → Confirm → Execute)
- Minimum execution units (atomic command groups)
- Synchronous execution via SlashCommand
- Task type detection (bugfix, feature, tdd, review, etc.)

**Example**:
```
/ccw "Implement JWT authentication"
```

#### 2. Spec Commands

**Files**:
- `spec-create.md` - Create specification
- `spec-execute.md` - Execute specification tasks
- `spec-list.md` - List all specs
- `spec-status.md` - Check spec status
- `spec-steering-setup.md` - Configure steering

**Usage**:
```
/spec create "User authentication system"
/spec execute
/spec list
```

#### 3. Bug Commands

**Files**:
- `bug-analyze.md` - Analyze bug
- `bug-create.md` - Create bug report
- `bug-fix.md` - Fix bug
- `bug-status.md` - Check bug status
- `bug-verify.md` - Verify bug fix

**Usage**:
```
/bug create "Login fails after 30 minutes"
/bug fix
```

#### 4. Template & Quotation Commands

**Files**:
- `template.md` - Generate proposal templates from Excel
- `template-quickref.md` - Quick reference
- `quotation.md` - Generate PowerPoint + PDF
- `quotation-quickref.md` - Quick reference

**Usage**:
```
/template dealA.xlsx
/quotation slide ./output/dealA_template.md
```

#### 5. Workflow Commands

**Location**: `commands/workflow/`

**Categories**:

**Planning**:
- `plan.md` - Full planning workflow
- `lite-plan.md` - Lightweight planning
- `replan.md` - Re-plan existing session

**Execution**:
- `execute.md` - Execute implementation
- `lite-execute.md` - Lightweight execution
- `lite-lite-lite.md` - Ultra-lightweight

**Debugging**:
- `debug.md` - Debug workflow
- `debug-with-file.md` - Debug with file context

**Testing**:
- `tdd-plan.md` - TDD planning
- `tdd-verify.md` - TDD verification
- `test-gen.md` - Test generation
- `test-fix-gen.md` - Test fix generation
- `test-cycle-execute.md` - Test cycle execution

**Review**:
- `review.md` - Basic review
- `review-module-cycle.md` - Module review cycle
- `review-session-cycle.md` - Session review cycle
- `review-fix.md` - Review and fix

**Brainstorming** (`brainstorm/`):
- `auto-parallel.md` - Auto parallel brainstorming
- Role-specific: `product-owner.md`, `scrum-master.md`, `system-architect.md`, etc.

**Session** (`session/`):
- `start.md` - Start session
- `resume.md` - Resume session
- `complete.md` - Complete session
- `list.md` - List sessions

**UI Design** (`ui-design/`):
- `generate.md` - Generate UI design
- `imitate-auto.md` - Imitate design
- `codify-style.md` - Codify style
- `import-from-code.md` - Import from code

**Tools** (`tools/`):
- Tool-specific workflows

**Specialized**:
- `quotation/generate.md` - Generate quotation
- `quotation/generate-slide.md` - Generate slides
- `template/generate.md` - Generate template

---

## Skills

### Skill Overview

**Total**: 36 skills

**Location**: `~/.claude/skills/`

### Structure

Each skill directory contains:
- `skill.md` - Main definition (required)
- `skill-implementation.md` - Implementation details
- Supporting files as needed

### Key Skills

#### 1. Business Workflow Skills

**template/** - Template Generation
- **Purpose**: Generate proposal templates from Excel files
- **Command**: `/template <excel_file.xlsx>`
- **Input**: Excel with Commercial (S1) and Technical (S2) sheets
- **Output**: Template, reasoning, checklist files
- **Features**:
  - Automatic pain point → AI module mapping
  - 12-section template generation
  - Placeholder tracking

**quotation_skill/** - Quotation Generation
- **Purpose**: Generate PowerPoint + PDF from verified templates
- **Command**: `/quotation slide <template.md>`
- **Features**:
  - Two-phase pipeline (slide agent + reviewer agent)
  - Direct MD → HTML → PPTX/PDF conversion
  - Intelligent slide type selection

**dealtransfer2template/** - Excel to Template
- **Purpose**: Convert Deal Transfer Excel + Knowledge base to technical proposals
- **Trigger**: User provides Deal Transfer document
- **Output**: Template, reasoning, checklist files

#### 2. Document Manipulation Skills

**docx/** - Word Documents
- **Create**: New .docx files
- **Edit**: Modify content with tracked changes
- **Analyze**: Extract text, handle comments
- **Format**: Preserve formatting

**pptx/** - PowerPoint
- **Create**: New presentations
- **Edit**: Modify layouts, add content
- **Format**: Style management

**pdf/** - PDF Manipulation
- **Extract**: Text and tables
- **Create**: New PDFs
- **Merge/Split**: Document manipulation
- **Forms**: Fill PDF forms

**xlsx/** - Excel Spreadsheets
- **Create**: New spreadsheets
- **Edit**: Modify with formulas, formatting
- **Analyze**: Data analysis and visualization

#### 3. Media Processing Skills

**media-processing/** - FFmpeg & ImageMagick
- **Video**: Conversion, encoding, streaming
- **Audio**: Extraction, conversion
- **Images**: Manipulation, format conversion
- **Filters**: Effects and composition
- **Hardware**: NVENC, QSV acceleration

**annotate/** - Image Annotation
- **Purpose**: Complete image annotation workflows
- **Workflow**: SAM3 detection → YOLO conversion
- **Features**:
  - Batch processing
  - Screen session management
  - Multi-class detection

**sam3-detect/** - SAM3 Detection
- **Purpose**: Core SAM3 object detection
- **Features**:
  - Natural language prompts
  - JSON coordinates output
  - Basic visualization

**sam3-to-yolo/** - SAM3 to YOLO
- **Purpose**: Convert SAM3 to YOLO format
- **Features**:
  - Multi-class support
  - Color-coded visualizations
  - Ultralytics dataset structure

#### 4. Development Skills

**project-analyze/** - Project Analysis
- **Purpose**: Multi-phase project analysis
- **Output**: Architecture, design, method analysis reports
- **Features**: Mermaid diagrams

**review-code/** - Code Review
- **Purpose**: Multi-dimensional code review
- **Dimensions**: Correctness, readability, performance, security, testing
- **Output**: Structured reports

**issue-manage/** - Issue Management
- **Purpose**: Interactive issue management
- **Features**:
  - Menu-driven CRUD operations
  - Bulk operations
  - Issue history

#### 5. Meta Skills

**skill-creator/** - Create Skills
- **Purpose**: Guide for creating new skills
- **Usage**: When building new Claude Code capabilities

**skill-generator/** - Meta-Skill Generator
- **Purpose**: Create skills with configurable execution modes
- **Modes**: Sequential (fixed order) or autonomous (stateless)

**skill-tuning/** - Skill Optimization
- **Purpose**: Diagnose and fix skill execution issues
- **Detection**: Context explosion, long-tail forgetting, data flow disruption

#### 6. Documentation Skills

**software-manual/** - Software Manual Generation
- **Output**: TiddlyWiki-style HTML manuals
- **Features**:
  - Screenshots
  - API docs
  - Multi-level code examples

**copyright-docs/** - Copyright Documentation
- **Purpose**: Generate CPCC-compliant design specs
- **Output**: Mermaid diagrams, design documents

**text-formatter/** - Text Formatting
- **Output**: BBCode + Markdown hybrid
- **Use**: Forum-optimized formatting

#### 7. Workflow Skills

**ccw-loop/** - Development Loop
- **Purpose**: Stateless iterative development workflow
- **Phases**: Develop, debug, validate
- **Features**: File-based state tracking

**ccw-help/** - Command Help
- **Purpose**: Command search, browse, recommend
- **Triggers**: ccw-help, ccw-issue

#### 8. Utility Skills

**google-drive/** - Google Drive Integration
- **Purpose**: Interact with Google Drive API
- **Features**: Upload, download, search, manage files
- **Auth**: Pre-configured at ~/.gdrivelm/

**prompt-enhancer/** - Prompt Enhancement
- **Trigger**: -e or --enhance flag
- **Features**: Session memory, intent analysis

**mcp-builder/** - MCP Server Builder
- **Purpose**: Create MCP servers
- **Languages**: Python (FastMCP), Node/TypeScript (MCP SDK)

---

## CLI Tools Integration

### Configuration File

**Expected Location**: `~/.claude/cli-tools.json`

**Note**: This file was not found in your setup. The system references it in CLAUDE.md but it's currently missing.

**Purpose**: Define CLI endpoints configuration

**Expected Structure**:
```json
{
  "tools": {
    "gemini": {
      "enabled": true,
      "primaryModel": "model-name",
      "tags": ["analysis", "implementation"]
    },
    "codex": {
      "enabled": true,
      "tags": ["review"]
    }
  }
}
```

### CLI Tools Usage Specification

**Location**: `~/.claude/workflows/cli-tools-usage.md`

**Key Concepts**:

1. **Tag-Based Routing**
   - Tools selected by capability tags
   - Examples: `analysis`, `implementation`, `documentation`, `testing`

2. **Prompt Template**
   ```bash
   ccw cli -p "PURPOSE: [...] TASK: [...] MODE: analysis CONTEXT: @**/* EXPECTED: [...] CONSTRAINTS: [...]" --tool <tool-id>
   ```

3. **Mode Protocol**
   - **analysis**: Read-only, safe for auto-execution
   - **write**: Create/Modify/Delete files
   - **review**: Git-aware code review (codex only)

4. **Auto-Invoke Triggers**
   - Self-repair fails
   - Ambiguous requirements
   - Architecture decisions
   - Pattern uncertainty
   - Critical code paths

5. **Agent Execution**
   - Agent calls: `run_in_background: false`
   - CLI calls: `run_in_background: true`
   - Wait for analysis results

---

## Protocols

### Protocol Templates

**Location**: `~/.claude/workflows/cli-templates/protocols/`

**Total**: 2 protocols

#### 1. Analysis Protocol

**File**: `protocols/analysis-protocol.md`

**Mode**: READ-ONLY

**Purpose**: Code analysis without file modifications

**Allowed Operations**:
- ✅ READ all CONTEXT files
- ✅ ANALYZE patterns, architecture, dependencies
- ✅ GENERATE text output and insights
- ✅ DOCUMENT in output response

**Forbidden Operations**:
- ❌ NO file creation
- ❌ NO file modification
- ❌ NO file deletion
- ❌ NO directory operations

**Execution Flow**:
1. Parse 6 fields (PURPOSE, TASK, MODE, CONTEXT, EXPECTED, RULES)
2. Read and analyze CONTEXT files
3. Identify patterns and issues
4. Generate insights
5. Output structured analysis

**Output Format**:
```markdown
# Analysis: [Title]

## Related Files
- `file1.ext` - description
- `file2.ext` - description

## Summary
[2-3 sentence overview]

## Key Findings
1. Finding - file:123
2. Finding - file:456

## Detailed Analysis
[Evidence-based analysis]

## Recommendations
1. Actionable recommendation
2. Actionable recommendation
```

#### 2. Write Protocol

**File**: `protocols/write-protocol.md`

**Mode**: Create/Modify/Delete

**Purpose**: Implementation with full file operations

**Allowed Operations**:
- ✅ READ all CONTEXT files
- ✅ CREATE new files
- ✅ MODIFY existing files
- ✅ DELETE files when required

**Restrictions**:
- Follow project conventions
- Cannot break existing functionality
- Must test every change

**Execution Flow**:
1. Parse 6 fields
2. Read CONTEXT files, find 3+ similar patterns
3. Plan implementation
4. Execute file operations
5. Validate changes
6. Report modifications

**Three-Attempt Rule**:
- On 3rd failure, stop and report:
  - What was attempted
  - What failed
  - Root cause

**Output Format**:
```markdown
# Implementation: [Title]

## Changes
- Created: `file1.ext` (X lines)
- Modified: `file2.ext` (+Y/-Z lines)
- Deleted: `file3.ext`

## Summary
[2-3 sentence overview]

## Key Decisions
1. Decision - rationale
2. Decision - file:line

## Implementation Details
[Evidence-based description]

## Testing
- Tests written: X
- Tests passing: Y/Z

## Validation
✅ Tests: X passing
✅ Build: Success
```

---

## Configuration

### Environment Variables

**Location**: `~/.claude/settings.json` → `env` field

**Current Settings**:
- `ANTHROPIC_AUTH_TOKEN`: API authentication
- `ANTHROPIC_BASE_URL`: Custom API endpoint (https://api.z.ai)
- `API_TIMEOUT_MS`: 3000000 (50 minutes)
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`: 1 (enabled)

### Hooks

**Location**: `~/.claude/settings.json` → `hooks` field

**Current Hook**:
- **PreToolUse**: Safety check before Bash execution
- **Script**: `~/.claude/scripts/safety-check.sh`

### Coding Philosophy

**Location**: `~/.claude/workflows/coding-philosophy.md`

**Core Beliefs**:
1. Pursue good taste
2. Embrace extreme simplicity
3. Be pragmatic
4. Data structures first
5. Never break backward compatibility
6. Incremental progress over big bangs
7. Learn from existing code
8. Clear intent over clever code
9. Follow existing code style
10. Minimize changes

**Simplicity Means**:
- Single responsibility per function/class
- Avoid premature abstractions
- No clever tricks
- If you need to explain it, it's too complex

**Fix, Don't Hide**:
- Solve problems, don't silence symptoms
- NEVER use suppression mechanisms without fixing root cause
- Always plan before implementation
- Stop after 3 failed attempts and reassess

---

## Context Tools Priority

**Location**: `~/.claude/workflows/context-tools.md`

**Priority Order**:

1. **mcp__ace-tool__search_context** (HIGHEST)
   - Semantic search with real-time codebase index
   - Use for: finding implementations, understanding architecture

2. **smart_search** (Fallback)
   - Use for: keyword/regex search, file discovery
   - Modes: auto, hybrid, exact, ripgrep

3. **read_file** (Batch Read)
   - Read multiple files in parallel
   - Supports glob patterns

4. **Shell Commands** (LAST RESORT)
   - Use only when MCP tools unavailable

**File Modification Priority**:
1. Built-in Edit tool (FIRST)
2. edit_file (MCP) (if Edit fails)
3. write_file (MCP) (last resort)

---

## Template System

**Location**: `~/.claude/workflows/cli-templates/`

**Total**: 19 templates

**Categories**:

### Planning Roles (12 templates)
- `data-architect.md`
- `product-manager.md`
- `product-owner.md`
- `scrum-master.md`
- `subject-matter-expert.md`
- `synthesis-role.md`
- `system-architect.md`
- `test-strategist.md`
- `ui-designer.md`
- `ux-expert.md`
- `api-designer.md`

### Tech Stacks (6 templates)
- `go-dev.md`
- `java-dev.md`
- `javascript-dev.md`
- `python-dev.md`
- `react-dev.md`
- `typescript-dev.md`

### Memory Templates
- `skill-md-template.md`

### Schema Templates
- `fix-plan-template.json`
- `fix-progress-template.json`

---

## Quick Reference

### Common Workflows

#### Generate Proposal from Excel
```bash
/template dealA.xlsx
# Output: ./output/dealA_[timestamp]/
#   - dealA_template.md
#   - dealA_reasoning.md
#   - dealA_checklist.md
```

#### Generate Slides from Template
```bash
/quotation slide ./output/dealA_[timestamp]/dealA_template.md
# Output: PowerPoint + PDF
```

#### Create and Execute Spec
```bash
/spec create "User authentication"
/spec execute
```

#### Bug Workflow
```bash
/bug create "Login fails"
/bug fix
/bug verify
```

#### Planning Workflow
```bash
/workflow:plan "Implement JWT authentication"
/workflow:execute
```

#### Code Review
```bash
/workflow:review-session-cycle
```

### Skill Invocations

Skills are invoked via `/skill-name`:

```bash
/annotate "Label this folder"
/ccw-loop "Develop feature"
/project-analyze
/review-code
```

---

## Summary

Your `.claude` global directory contains:

- **108 commands** for workflow automation
- **36 skills** for specialized tasks
- **19 CLI templates** for consistent execution
- **2 protocols** (analysis, write)
- **Complete workflow system** with JSON-based task management
- **Custom API configuration** with extended timeout
- **Safety hooks** for tool execution

**Key Features**:
1. Structured workflow system with session management
2. Business workflow automation (proposals, quotations)
3. Document manipulation (Word, PowerPoint, PDF, Excel)
4. Media processing (video, audio, images)
5. Development tools (project analysis, code review, issue management)
6. Meta skills for creating and optimizing other skills
7. CLI tools integration with tag-based routing
8. Protocol-driven execution (analysis vs write modes)

**Design Philosophy**:
- JSON as single source of truth
- On-demand file creation
- Maximum 2-level task hierarchy
- Flow control with dependencies
- Agent-agnostic task definitions
- Simplicity and pragmatism over cleverness

This is a sophisticated, production-grade workflow system built on top of Claude Code, designed for enterprise software development with extensive automation capabilities.
