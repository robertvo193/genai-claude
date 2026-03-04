# Detailed Guide to Skills, Commands, and Workflows

## Overview

This document provides detailed information about all 36 skills, 108 commands, and the workflow system in your global `.claude` directory.

---

## Part 1: Skills (36 Total)

### Business Workflow Skills

#### 1. **template** - Template Generation
**Location**: `~/.claude/skills/template/`
**Purpose**: Generate technical proposal templates from Deal Transfer Excel files
**Command**: `/template <excel_file.xlsx>`
**Trigger**: User provides Excel file or asks for template generation

**Workflow** (5 steps):
1. Validate Excel file format
2. Extract data from Commercial (S1) and Technical (S2) sheets
3. Map pain points to AI modules automatically
4. Generate 3 files:
   - `{project}_template.md` - Proposal template
   - `{project}_reasoning.md` - Audit trail
   - `{project}_checklist.md` - Placeholders
5. Output to `./output/{project}_{timestamp}/`

**AI Module Mapping** (automatic):
| Pain Points | AI Module |
|-------------|-----------|
| helmet, safety | Safety Helmet Detection |
| vest | Safety Vest Detection |
| mask | Safety Mask Detection |
| fire, smoke | Fire & Smoke Detection |
| intrusion | Intrusion Detection |
| vehicle | Vehicle Detection |

**Input Requirements**:
- Excel file in `.xlsx` format
- Sheets named "Commercial" (or S1) and "Technical" (or S2)
- Row-based format (Question/Answer pairs)

**Output Structure**:
```
./output/
└── {project}_{timestamp}/
    ├── {project}_template.md       # 12 sections
    ├── {project}_reasoning.md      # Complete audit trail
    └── {project}_checklist.md      # Placeholders to fill
```

#### 2. **quotation_skill** - Quotation Generation
**Location**: `~/.claude/skills/quotation_skill/`
**Purpose**: Generate PowerPoint and PDF from verified proposal templates
**Command**: `/quotation slide <template.md>`
**Trigger**: User asks to generate slides/quotation

**Workflow** (4 steps):
1. Validate verified template (no placeholders)
2. Generate HTML slides with proper formatting
3. Convert HTML to PowerPoint (.pptx)
4. Convert PowerPoint to PDF

**Input Requirements**:
- Verified template markdown file
- No `[PLACEHOLDER_XXX]` markers remaining
- Proper markdown structure

**Output**:
- `{project}.pptx` - PowerPoint presentation
- `{project}.pdf` - PDF document

#### 3. **dealtransfer2template** - Excel to Technical Proposal
**Location**: `~/.claude/skills/dealtransfer2template/`
**Purpose**: Convert Deal Transfer Excel + Knowledge base to technical proposals
**Trigger**: User provides Deal Transfer document

**Workflow**:
1. Extract data from Commercial and Technical sheets
2. Query knowledge base for relevant information
3. Map pain points to AI modules
4. Generate proposal template with reasoning and checklist

**Output**: Same 3-file structure as template skill

#### 4. **quotation-generate-slide** - Slide Generation Wrapper
**Location**: `~/.claude/skills/quotation-generate-slide/`
**Purpose**: Wrapper for quotation_skill with enhanced command syntax
**Command**: `/quotation generate slide <template.md>`

---

### Document Manipulation Skills

#### 5. **docx** - Word Documents
**Location**: `~/.claude/skills/docx/`
**Purpose**: Create, edit, and analyze Word documents (.docx files)

**Capabilities**:
- **Create**: New .docx files with formatted content
- **Modify**: Edit content while preserving tracked changes and comments
- **Extract**: Text and structured data
- **Analyze**: Read comments, tracked changes, formatting
- **Format**: Preserve existing formatting and styles

**Use When**:
- Creating documentation
- Modifying existing Word documents
- Working with tracked changes
- Adding comments to documents
- Any Word document task

**Key Features**:
- Tracked changes support
- Comment handling
- Formatting preservation
- Text extraction
- Style management

#### 6. **pptx** - PowerPoint Presentations
**Location**: `~/.claude/skills/pptx/`
**Purpose**: Create, edit, and analyze PowerPoint presentations (.pptx files)

**Capabilities**:
- **Create**: New presentations from scratch or templates
- **Edit**: Modify slides, layouts, content
- **Analyze**: Extract text, layouts, design elements
- **Format**: Style management, themes

**Reading Methods**:

1. **Text Extraction** (simple):
```bash
python -m markitdown file.pptx
```

2. **Raw XML Access** (advanced features):
```bash
python ooxml/scripts/unpack.py <file.pptx> <output_dir>
```

**Key XML Structures**:
- `ppt/presentation.xml` - Main metadata
- `ppt/slides/slide{N}.xml` - Slide contents
- `ppt/notesSlides/notesSlide{N}.xml` - Speaker notes
- `ppt/comments/modernComment_*.xml` - Comments
- `ppt/slideLayouts/` - Layout templates
- `ppt/theme/` - Themes and styling
- `ppt/media/` - Images and media

**Creating Presentations**:
- Use **html2pptx** workflow for HTML to PowerPoint conversion
- Analyze typography and colors from examples first
- Check `ppt/theme/theme1.xml` for colors and fonts
- Sample `ppt/slides/slide1.xml` for actual usage

**Use When**:
- Creating new presentations
- Modifying existing presentations
- Working with layouts
- Adding comments or speaker notes
- Any presentation task

#### 7. **pdf** - PDF Manipulation
**Location**: `~/.claude/skills/pdf/`
**Purpose**: Manipulate PDF documents (extract, create, merge, split, forms)

**Capabilities**:
- **Extract**: Text and tables from PDFs
- **Create**: New PDF documents
- **Merge**: Combine multiple PDFs
- **Split**: Separate PDF pages
- **Forms**: Fill PDF forms programmatically

**Use When**:
- Processing PDF files
- Extracting data from PDFs
- Filling PDF forms
- Generating PDF reports
- Any PDF manipulation task

#### 8. **xlsx** - Excel Spreadsheets
**Location**: `~/.claude/skills/xlsx/`
**Purpose**: Create, edit, and analyze Excel spreadsheets (.xlsx, .xlsm, .csv)

**Capabilities**:
- **Create**: New spreadsheets with formulas and formatting
- **Edit**: Modify existing sheets while preserving formulas
- **Analyze**: Data analysis and visualization
- **Recalculate**: Update formulas

**Use When**:
- Working with spreadsheets
- Data analysis and visualization
- Creating reports with charts
- Processing CSV/Excel data
- Any spreadsheet task

---

### Media Processing Skills

#### 9. **media-processing** - FFmpeg & ImageMagick
**Location**: `~/.claude/skills/media-processing/`
**Purpose**: Process multimedia files with FFmpeg (video/audio) and ImageMagick (images)

**Video Capabilities** (FFmpeg):
- Encoding/conversion (H.264, H.265, VP9)
- Streaming (HLS/DASH manifests)
- Filtering and effects
- Hardware acceleration (NVENC, QSV)
- Audio extraction
- Format conversion

**Image Capabilities** (ImageMagick):
- Format conversion
- Batch processing
- Effects and composition
- Resizing/cropping
- Thumbnail generation

**Use When**:
- Converting media formats
- Encoding videos with specific codecs
- Resizing/cropping images
- Extracting audio from video
- Applying filters and effects
- Optimizing file sizes
- Creating streaming manifests
- Generating thumbnails
- Batch processing images
- Any media processing task

**Supported Formats**: 100+ formats

#### 10. **annotate** - Image Annotation Workflow
**Location**: `~/.claude/skills/annotate/`
**Purpose**: Complete image annotation workflows with SAM3 detection and YOLO conversion

**Workflow**:
1. SAM3 object detection (natural language prompts)
2. YOLO format conversion (multi-class support)
3. Dataset generation (Ultralytics-compatible)

**Features**:
- "label this folder" workflow support
- Automatic batch processing
- Screen session management for large jobs
- Multi-class detection
- Color-coded visualizations

**Use When**:
- Annotating images for computer vision
- Preparing datasets for training
- Object detection tasks
- Complete dataset preparation workflows

#### 11. **sam3-detect** - SAM3 Object Detection
**Location**: `~/.claude/skills/sam3-detect/`
**Purpose**: Core SAM3 object detection and segmentation with natural language prompts

**Features**:
- Natural language prompts
- JSON coordinates output
- Basic visualization
- Auto-activates SAM3 environment (conda 'sam3' or .venv)

**Use For**: Single image or simple batch processing

**Use When**:
- Single image detection/segmentation
- Simple batch processing
- Getting JSON coordinates
- Basic visualization needs

#### 12. **sam3-to-yolo** - SAM3 to YOLO Converter
**Location**: `~/.claude/skills/sam3-to-yolo/`
**Purpose**: Convert SAM3 JSON outputs to YOLO format

**Features**:
- Multi-class support
- Text prompt as class names
- Merging multiple classes for same image
- Color-coded visualizations
- Ultralytics dataset structure

**Use When**:
- Converting SAM3 detections to YOLO format
- Preparing YOLO training datasets
- Multi-class object detection workflows

---

### Development Skills

#### 13. **project-analyze** - Project Analysis
**Location**: `~/.claude/skills/project-analyze/`
**Purpose**: Multi-phase iterative project analysis with Mermaid diagrams

**Triggers**:
- "analyze project"
- "architecture report"
- "design analysis"
- "code structure"
- "system overview"

**Architecture**:
```
Phase 1: Requirements → analysis-config.json
Phase 2: Exploration → 初步探索，确定范围
Phase 3: Parallel Agents → sections/section-*.md
Phase 3.5: Consolidation → consolidation-summary.md
Phase 4: Assembly → 合并MD + 质量附录
Phase 5: Refinement → 最终报告
```

**Output Reports**:
- Architecture reports
- Design reports
- Method analysis reports

**Use When**:
- Analyzing codebases
- Understanding project structure
- Reviewing architecture
- Exploring design patterns
- Documenting system components

#### 14. **review-code** - Code Review
**Location**: `~/.claude/skills/review-code/`
**Purpose**: Multi-dimensional code review with structured reports

**Triggers**:
- "review code"
- "code review"
- "审查代码"
- "代码审查"

**Review Dimensions** (6 total):
1. **Correctness**: Logic errors, edge cases
2. **Readability**: Code clarity, naming conventions
3. **Performance**: Efficiency, optimization opportunities
4. **Security**: OWASP Top 10, vulnerabilities
5. **Testing**: Test coverage, quality
6. **Architecture**: Design patterns, structure

**Architecture**:
```
Phase 0: Study specs (强制前置)
  ↓
Orchestrator (状态驱动决策)
  ↓
├─ Collect Context
├─ Quick Scan
├─ Deep Review
├─ Report Generate
└─ Complete
```

**Use When**:
- Reviewing code changes
- Analyzing code quality
- Security audits
- Performance analysis
- Any code review task

#### 15. **issue-manage** - Issue Management
**Location**: `~/.claude/skills/issue-manage/`
**Purpose**: Interactive issue management with menu-driven CRUD operations

**Triggers**:
- "manage issue"
- "list issues"
- "edit issue"
- "delete issue"
- "bulk update"
- "issue dashboard"
- "issue history"
- "completed issues"

**Features**:
- Menu-driven interface
- Create, Read, Update, Delete operations
- Bulk operations
- Issue history tracking
- Dashboard view

**Use When**:
- Managing project issues
- Tracking bug reports
- Bulk issue updates
- Viewing issue status/history

---

### Meta Skills

#### 16. **skill-creator** - Create Skills
**Location**: `~/.claude/skills/skill-creator/`
**Purpose**: Guide for creating new Claude Code skills

**Use When**:
- Building new skills
- Extending Claude's capabilities
- Creating specialized workflows

#### 17. **skill-generator** - Meta-Skill Generator
**Location**: `~/.claude/skills/skill-generator/`
**Purpose**: Create new Claude Code skills with configurable execution modes

**Triggers**:
- "create skill"
- "new skill"
- "skill generator"
- "生成技能"
- "创建技能"

**Execution Modes**:
- **Sequential**: Fixed order execution
- **Autonomous**: Stateless phase patterns

**Use When**:
- Skill scaffolding
- Creating new workflows
- Building skills with specific execution patterns

#### 18. **skill-tuning** - Skill Optimization
**Location**: `~/.claude/skills/skill-tuning/`
**Purpose**: Diagnose and fix skill execution issues

**Triggers**:
- "skill tuning"
- "tune skill"
- "skill diagnosis"
- "optimize skill"
- "skill debug"

**Detection Capabilities**:
- Context explosion
- Long-tail forgetting
- Data flow disruption
- Agent coordination failures

**Supports**: Gemini CLI for deep analysis

**Use When**:
- Skill not working correctly
- Performance issues
- Debugging skill execution
- Optimizing skill performance

---

### Documentation Skills

#### 19. **software-manual** - Software Manual Generation
**Location**: `~/.claude/skills/software-manual/`
**Purpose**: Generate interactive TiddlyWiki-style HTML software manuals

**Triggers**:
- "software manual"
- "user guide"
- "generate manual"
- "create docs"

**Features**:
- Screenshots
- API documentation
- Multi-level code examples
- Interactive navigation
- Single HTML file output

**Use When**:
- Creating user guides
- Generating software documentation
- Creating API references
- Building interactive manuals

#### 20. **copyright-docs** - Copyright Documentation
**Location**: `~/.claude/skills/copyright-docs/`
**Purpose**: Generate CPCC-compliant software copyright design specifications

**Triggers**:
- "软件著作权"
- "设计说明书"
- "版权登记"
- "CPCC"
- "软著申请"

**Output**:
- Complete design documents
- Mermaid diagrams
- CPCC-compliant format

**Use When**:
- Software copyright registration
- Generating design specifications
- Creating CPCC-compliant documents
- Documenting software for IP protection

#### 21. **text-formatter** - Text Formatting
**Location**: `~/.claude/skills/text-formatter/`
**Purpose**: Transform and optimize text content with intelligent formatting

**Triggers**:
- "format text"
- "text formatter"
- "排版"
- "格式化文本"
- "BBCode"

**Output**: BBCode + Markdown hybrid format

**Use For**: Forum-optimized formatting

---

### Workflow Skills

#### 22. **ccw-loop** - Development Loop
**Location**: `~/.claude/skills/ccw-loop/`
**Purpose**: Stateless iterative development loop workflow with documented progress

**Triggers**:
- "ccw-loop"
- "dev loop"
- "development loop"
- "开发循环"
- "迭代开发"

**Phases**:
1. **Develop**: Implementation phase
2. **Debug**: Debugging phase
3. **Validate**: Validation phase

**Features**:
- File-based state tracking
- Independent phase files
- Auto-cycle mode support
- Progress documentation

**Arguments**:
- `task`: Task description (new loop)
- `--loop-id`: Continue existing loop
- `--auto`: Auto-cycle through all phases

**Use When**:
- Iterative development
- Debugging with documentation
- Validating implementations
- Tracking development progress

#### 23. **ccw-help** - Command Help System
**Location**: `~/.claude/skills/ccw-help/`
**Purpose**: Command search, browse, and recommendation

**Triggers**:
- "ccw-help"
- "ccw-issue"

**Use When**:
- Finding available commands
- Browsing command documentation
- Getting command recommendations

#### 24. **workflow-loader** - Workflow Executor
**Location**: `~/.claude/skills/workflow-loader/`
**Purpose**: Execute CCW workflows from `~/.claude/commands/workflow/` directory

**Features**:
- TodoWrite progress tracking
- Auto-continue execution

**Use When**:
- Running workflow commands
- Executing predefined workflows
- Automated task sequences

---

### Utility Skills

#### 25. **google-drive** - Google Drive Integration
**Location**: `~/.claude/skills/google-drive/`
**Purpose**: Interact with Google Drive API using PyDrive2

**Authentication**: Pre-configured at `~/.gdrivelm/`

**Capabilities**:
- Upload files
- Download files
- Search files/folders
- Manage files (delete, move, copy)
- Folder management
- Batch operations
- Sharing settings

**Use When**:
- Working with Google Drive
- File transfers to/from Drive
- Searching Drive content
- Managing Drive files/folders
- Any Google Drive operation

#### 26. **prompt-enhancer** - Prompt Enhancement
**Location**: `~/.claude/skills/prompt-enhancer/`
**Purpose**: Transform vague prompts into actionable specs

**Trigger**: `-e` or `--enhance` flag

**Features**:
- Session memory
- Intent analysis
- Intelligent transformation

**Use When**:
- Improving vague prompts
- Adding context to requests
- Transforming user input

---

### Builder Skills

#### 27. **mcp-builder** - MCP Server Builder
**Location**: `~/.claude/skills/mcp-builder/`
**Purpose**: Create high-quality MCP (Model Context Protocol) servers

**Languages**:
- Python (FastMCP)
- Node/TypeScript (MCP SDK)

**Use When**:
- Building MCP servers
- Integrating external APIs
- Creating LLM tools
- Service integration

**Workflow** (4 phases):
1. **Deep Research and Planning**:
   - Understand modern MCP design
   - API coverage vs workflow tools
   - Tool naming and discoverability

2. **Server Implementation**:
   - Language-specific setup
   - Tool design patterns
   - Error handling

3. **Testing and Validation**:
   - Tool testing
   - Integration testing
   - Documentation

4. **Packaging and Publishing**:
   - Package setup
   - Publishing guide
   - Maintenance

**Key Design Principles**:
- Balance API coverage with workflow tools
- Clear, descriptive tool names
- Consistent naming conventions
- Comprehensive input validation
- Clear error messages
- Good documentation

---

### Other Skills

#### 28. **alert-generator** - Alert Generation
**Location**: `~/.claude/skills/alert-generator/`
**Purpose**: Generate alerts (specific to your use case)

#### 29. **my-skill** - Custom Skill
**Location**: `~/.claude/skills/my-skill/`
**Purpose**: Template/custom skill for personal use

#### 30. **yolo-finetune** - YOLO Fine-tuning
**Location**: `~/.claude/skills/yolo-finetune/`
**Purpose**: Fine-tune YOLO models for custom object detection

#### 31-36. Additional Skills
- `template2slide/` - Template to slide conversion
- `template2slide-pro/` - Pro version
- `template2slide-pro-backup/` - Backup
- `template_skill/` - Template skill variant
- `_shared/` - Shared utilities

---

## Part 2: Commands (108 Total)

### Top-Level Commands

#### 1. **ccw** - Main Workflow Orchestrator
**File**: `commands/ccw.md`
**Purpose**: Intent analysis → workflow selection → command chain execution

**5-Phase Workflow**:
1. **Analyze Intent**:
   - Extract goal, scope, constraints
   - Detect task type (bugfix, feature, tdd, review, etc.)
   - Assess complexity (low, medium, high)
   - Calculate clarity score (0-3)

2. **Clarify Requirements** (if clarity < 2):
   - Generate clarification questions
   - Ask user for answers
   - Update analysis

3. **Select Workflow**:
   - Match task type to workflow
   - Consider complexity level
   - Choose appropriate command chain

4. **Confirm & Execute**:
   - Show selected workflow
   - User confirms
   - Execute command chain

5. **Track Progress**:
   - TodoWrite tracking
   - Update completion status

**Task Types**:
- `bugfix-hotfix`: Urgent/production + fix/bug
- `bugfix`: fix, bug, error, crash, fail, debug
- `issue-batch`: issues + fix/resolve
- `exploration`: uncertain, explore, research
- `multi-perspective`: compare, cross-verify
- `quick-task`: quick/simple + feature
- `ui-design`: ui, design, component, style
- `tdd`: tdd, test-driven, test first
- `test-fix`: test fail, fix test
- `review`: review, code review
- `documentation`: docs, documentation, readme

**Minimum Execution Units**:
- Planning + Execution: `lite-plan` → `lite-execute`
- Testing: `test-fix-gen` → `test-cycle-execute`
- Review: `review-session-cycle` → `review-fix`

**Use**: `/ccw "task description"`

#### 2. **ccw-coordinator** - CLI Coordinator
**File**: `commands/ccw-coordinator.md`
**Purpose**: External CLI execution with background tasks and hook callbacks

**Difference from ccw**:
- `ccw`: SlashCommand in main process (blocking)
- `ccw-coordinator`: External CLI with background execution

**Use**: `/ccw-coordinator "task"`

---

### Spec Commands

#### 3. **spec-create** - Create Specification
**File**: `commands/spec-create.md`
**Purpose**: Create new feature specification through complete workflow

**Workflow Sequence** (must follow in order):
1. **Requirements Phase**:
   - Create `requirements.md`
   - Get user approval
   - Proceed to design

2. **Design Phase**:
   - Create `design.md`
   - Get user approval
   - Proceed to tasks

3. **Tasks Phase**:
   - Create `tasks.md`
   - Get user approval
   - Ask if task commands needed

4. **Task Commands Generation** (optional):
   - Run `claude-code-spec-workflow generate-task-commands`
   - Generate executable commands

5. **Implementation Phase**:
   - Execute generated commands
   - Or execute tasks individually

**Directory Structure**:
```
.claude/specs/{feature-name}/
├── requirements.md
├── design.md
├── tasks.md
└── task-commands/ (optional)
```

**Use**: `/spec create <feature-name> [description]`

#### 4. **spec-execute** - Execute Specification Tasks
**File**: `commands/spec-execute.md`
**Purpose**: Execute specific tasks from approved task list

**Use**: `/spec execute <task-id>`

#### 5. **spec-list** - List Specifications
**File**: `commands/spec-list.md`
**Purpose**: List all specs in current project

**Use**: `/spec list`

#### 6. **spec-status** - Specification Status
**File**: `commands/spec-status.md`
**Purpose**: Show status of all specs or specific spec

**Use**: `/spec status [spec-name]`

#### 7. **spec-steering-setup** - Configure Steering
**File**: `commands/spec-steering-setup.md`
**Purpose**: Create/update steering documents for persistent project context

**Use**: `/spec steering-setup`

---

### Bug Commands

#### 8. **bug-analyze** - Analyze Bug
**File**: `commands/bug-analyze.md`
**Purpose**: Investigate and analyze root cause of reported bug

**Use**: `/bug analyze <bug-description>`

#### 9. **bug-create** - Create Bug Report
**File**: `commands/bug-create.md`
**Purpose**: Initialize new bug fix workflow

**Use**: `/bug create <bug-description>`

#### 10. **bug-fix** - Fix Bug
**File**: `commands/bug-fix.md`
**Purpose**: Implement the fix for analyzed bug

**Use**: `/bug fix`

#### 11. **bug-status** - Bug Status
**File**: `commands/bug-status.md`
**Purpose**: Show status of all bugs or specific bug

**Use**: `/bug status [bug-id]`

#### 12. **bug-verify** - Verify Bug Fix
**File**: `commands/bug-verify.md`
**Purpose**: Verify bug fix works correctly, no regressions

**Use**: `/bug verify`

---

### Template & Quotation Commands

#### 13. **template** - Generate Templates
**File**: `commands/template.md`
**Purpose**: Generate technical proposal templates from Excel files

**Subcommands**:
- `template generate deal <excel.xlsx>`: Generate from Excel
- `template status`: Show generation status
- `template list`: List available templates

**Use**: `/template generate deal <excel.xlsx>`

#### 14. **template-quickref** - Template Quick Reference
**File**: `commands/template-quickref.md`
**Purpose**: Quick reference for template command

#### 15. **quotation** - Generate Quotations
**File**: `commands/quotation.md`
**Purpose**: Generate PowerPoint and PDF from templates

**Subcommands**:
- `quotation generate slide <template.md>`: Generate slides
- `quotation status`: Show generation status
- `quotation list`: List available quotations

**Use**: `/quotation generate slide <template.md>`

#### 16. **quotation-quickref** - Quotation Quick Reference
**File**: `commands/quotation-quickref.md`
**Purpose**: Quick reference for quotation command

---

### Utility Commands

#### 17. **version** - Version Information
**File**: `commands/version.md`
**Purpose**: Display Claude Code version and check for updates

**Use**: `/version`

#### 18. **enhance-prompt** - Enhance Prompt
**File**: `commands/enhance-prompt.md`
**Purpose**: Transform vague prompts using session memory and intent analysis

**Trigger**: `-e` or `--enhance` flag

---

### Workflow Commands (30+ Files)

**Location**: `commands/workflow/`

#### Planning Workflows

##### 19. **plan** - Full Planning Workflow
**File**: `workflow/plan.md`
**Purpose**: 5-phase planning workflow with task generation

**Phases**:
1. **Session Discovery** → Session ID
2. **Context Gathering** → Context package + conflict risk
3. **Conflict Resolution** (optional) → Modified artifacts
4. **Task Generation** → IMPL_PLAN.md, task JSONs, TODO_LIST.md
5. **Return** → Summary with next steps

**Use**: `/workflow:plan [-y|--yes] "task description"`

**Auto Mode**: With `--yes` or `-y`, auto-continue all phases

##### 20. **lite-plan** - Lightweight Planning
**File**: `workflow/lite-plan.md`
**Purpose**: Quick planning for simpler tasks

**Use**: `/workflow:lite-plan "task"`

##### 21. **replan** - Re-plan Session
**File**: `workflow/replan.md`
**Purpose**: Re-plan existing workflow session

**Use**: `/workflow:replan`

---

#### Execution Workflows

##### 22. **execute** - Execute Workflow
**File**: `workflow/execute.md`
**Purpose**: Coordinate agent execution with automatic session discovery

**Phases**:
1. **Session Discovery**: Find active sessions
2. **Execution Strategy**: Parse IMPL_PLAN.md
3. **TodoWrite Tracking**: Real-time progress
4. **Agent Orchestration**: Execute tasks with context
5. **Status Sync**: Update JSON state
6. **Autonomous Completion**: Continue until all tasks done

**Lazy Loading**: Task JSONs loaded on-demand

**Use**: `/workflow:execute [-y|--yes] [--resume-session="session-id"]`

**Auto Mode**: Select first session, auto-complete on finish

##### 23. **lite-execute** - Lightweight Execution
**File**: `workflow/lite-execute.md`
**Purpose**: Quick execution for simple tasks

**Use**: `/workflow:lite-execute`

##### 24. **lite-lite-lite** - Ultra-Lightweight
**File**: `workflow/lite-lite-lite.md`
**Purpose**: Minimal execution for tiny tasks

**Use**: `/workflow:lite-lite-lite`

---

#### Debugging Workflows

##### 25. **debug** - Debug Workflow
**File**: `workflow/debug.md`
**Purpose**: Debug issues with guided analysis

**Use**: `/workflow:debug`

##### 26. **debug-with-file** - Debug with File Context
**File**: `workflow/debug-with-file.md`
**Purpose**: Debug with specific file context

**Use**: `/workflow:debug-with-file <file>`

---

#### Testing Workflows

##### 27. **tdd-plan** - TDD Planning
**File**: `workflow/tdd-plan.md`
**Purpose**: Test-driven development planning

**Use**: `/workflow:tdd-plan`

##### 28. **tdd-verify** - TDD Verification
**File**: `workflow/tdd-verify.md`
**Purpose**: Verify TDD implementation

**Use**: `/workflow:tdd-verify`

##### 29. **test-gen** - Test Generation
**File**: `workflow/test-gen.md`
**Purpose**: Generate tests for code

**Use**: `/workflow:test-gen`

##### 30. **test-fix-gen** - Test Fix Generation
**File**: `workflow/test-fix-gen.md`
**Purpose**: Generate fixes for failing tests

**Use**: `/workflow:test-fix-gen`

##### 31. **test-cycle-execute** - Test Cycle Execution
**File**: `workflow/test-cycle-execute.md`
**Purpose**: Execute full test cycle (gen + exec + fix)

**Use**: `/workflow:test-cycle-execute`

---

#### Review Workflows

##### 32. **review** - Basic Review
**File**: `workflow/review.md`
**Purpose**: Basic code review

**Use**: `/workflow:review`

##### 33. **review-module-cycle** - Module Review Cycle
**File**: `workflow/review-module-cycle.md`
**Purpose**: Comprehensive module review with fix cycle

**Use**: `/workflow:review-module-cycle`

##### 34. **review-session-cycle** - Session Review Cycle
**File**: `workflow/review-session-cycle.md`
**Purpose**: Review entire workflow session

**Use**: `/workflow:review-session-cycle`

##### 35. **review-fix** - Review and Fix
**File**: `workflow/review-fix.md`
**Purpose**: Review code and implement fixes

**Use**: `/workflow:review-fix`

---

#### Session Management

**Location**: `workflow/session/`

##### 36. **session:start** - Start Session
**File**: `workflow/session/start.md`
**Purpose**: Start new workflow session

**Use**: `/workflow:session:start "description"`

##### 37. **session:resume** - Resume Session
**File**: `workflow/session/resume.md`
**Purpose**: Resume existing workflow session

**Use**: `/workflow:session:resume [session-id]`

##### 38. **session:complete** - Complete Session
**File**: `workflow/session/complete.md`
**Purpose**: Complete workflow session

**Use**: `/workflow:session:complete`

##### 39. **session:list** - List Sessions
**File**: `workflow/session/list.md`
**Purpose**: List all workflow sessions

**Use**: `/workflow:session:list`

##### 40. **session:solidify** - Solidify Session
**File**: `workflow/session/solidify.md`
**Purpose**: Solidify session (save state)

**Use**: `/workflow:session:solidify`

---

#### Brainstorming Workflows

**Location**: `workflow/brainstorm/`

##### 41. **auto-parallel** - Auto Parallel Brainstorm
**File**: `workflow/brainstorm/auto-parallel.md`
**Purpose**: Automatic parallel brainstorming with multiple roles

**Use**: `/workflow:brainstorm:auto-parallel`

##### 42. **product-owner** - Product Owner Role
**File**: `workflow/brainstorm/product-owner.md`
**Purpose**: Brainstorm from product owner perspective

**Use**: `/workflow:brainstorm:product-owner`

##### 43. **scrum-master** - Scrum Master Role
**File**: `workflow/brainstorm/scrum-master.md`
**Purpose**: Brainstorm from scrum master perspective

**Use**: `/workflow:brainstorm:scrum-master`

##### 44. **system-architect** - System Architect Role
**File**: `workflow/brainstorm/system-architect.md`
**Purpose**: Brainstorm from system architect perspective

**Use**: `/workflow:brainstorm:system-architect`

##### 45. **subject-matter-expert** - Subject Matter Expert
**File**: `workflow/brainstorm/subject-matter-expert.md`
**Purpose**: Brainstorm from domain expert perspective

**Use**: `/workflow:brainstorm:subject-matter-expert`

##### 46. **ux-expert** - UX Expert Role
**File**: `workflow/brainstorm/ux-expert.md`
**Purpose**: Brainstorm from UX expert perspective

**Use**: `/workflow:brainstorm:ux-expert`

##### 47. **ui-designer** - UI Designer Role
**File**: `workflow/brainstorm/ui-designer.md`
**Purpose**: Brainstorm from UI designer perspective

**Use**: `/workflow:brainstorm:ui-designer`

##### 48. **data-architect** - Data Architect Role
**File**: `workflow/brainstorm/data-architect.md`
**Purpose**: Brainstorm from data architect perspective

**Use**: `/workflow:brainstorm:data-architect`

##### 49. **api-designer** - API Designer Role
**File**: `workflow/brainstorm/api-designer.md`
**Purpose**: Brainstorm from API designer perspective

**Use**: `/workflow:brainstorm:api-designer`

##### 50. **product-manager** - Product Manager Role
**File**: `workflow/brainstorm/product-manager.md`
**Purpose**: Brainstorm from product manager perspective

**Use**: `/workflow:brainstorm:product-manager`

##### 51. **synthesis** - Synthesis Role
**File**: `workflow/brainstorm/synthesis.md`
**Purpose**: Synthesize all brainstorming inputs

**Use**: `/workflow:brainstorm:synthesis`

##### 52. **artifacts** - Artifacts Generation
**File**: `workflow/brainstorm/artifacts.md`
**Purpose**: Generate brainstorming artifacts

**Use**: `/workflow:brainstorm:artifacts`

---

#### UI Design Workflows

**Location**: `workflow/ui-design/`

##### 53. **generate** - Generate UI Design
**File**: `workflow/ui-design/generate.md`
**Purpose**: Generate complete UI design

**Use**: `/workflow:ui-design:generate`

##### 54. **imitate-auto** - Imitate Design
**File**: `workflow/ui-design/imitate-auto.md`
**Purpose**: Imitate existing design automatically

**Use**: `/workflow:ui-design:imitate-auto`

##### 55. **codify-style** - Codify Style
**File**: `workflow/ui-design/codify-style.md`
**Purpose**: Extract and codify design style

**Use**: `/workflow:ui-design:codify-style`

##### 56. **import-from-code** - Import from Code
**File**: `workflow/ui-design/import-from-code.md`
**Purpose**: Import UI design from existing code

**Use**: `/workflow:ui-design:import-from-code`

##### 57. **style-extract** - Extract Style
**File**: `workflow/ui-design/style-extract.md`
**Purpose**: Extract style information

**Use**: `/workflow:ui-design:style-extract`

##### 58. **layout-extract** - Extract Layout
**File**: `workflow/ui-design/layout-extract.md`
**Purpose**: Extract layout information

**Use**: `/workflow:ui-design:layout-extract`

##### 59. **animation-extract** - Extract Animation
**File**: `workflow/ui-design/animation-extract.md`
**Purpose**: Extract animation information

**Use**: `/workflow:ui-design:animation-extract`

##### 60. **reference-page-generator** - Reference Page Generator
**File**: `workflow/ui-design/reference-page-generator.md`
**Purpose**: Generate reference pages

**Use**: `/workflow:ui-design:reference-page-generator`

##### 61. **design-sync** - Design Sync
**File**: `workflow/ui-design/design-sync.md`
**Purpose**: Sync design with code

**Use**: `/workflow:ui-design:design-sync`

---

#### Specialized Workflows

##### 62. **action-plan-verify** - Verify Action Plan
**File**: `workflow/action-plan-verify.md`
**Purpose**: Verify action plan quality

**Use**: `/workflow:action-plan-verify`

##### 63. **clean** - Clean Workflow
**File**: `workflow/clean.md`
**Purpose**: Clean up workflow artifacts

**Use**: `/workflow:clean`

##### 64. **develop-with-file** - Develop with File
**File**: `workflow/develop-with-file.md`
**Purpose**: Development with file context

**Use**: `/workflow:develop-with-file <file>`

##### 65. **init** - Initialize Workflow
**File**: `workflow/init.md`
**Purpose**: Initialize new workflow

**Use**: `/workflow:init`

##### 66. **multi-cli-plan** - Multi-CLI Planning
**File**: `workflow/multi-cli-plan.md`
**Purpose**: Plan with multiple CLI tools

**Use**: `/workflow:multi-cli-plan`

##### 67. **plan-verify** - Verify Plan
**File**: `workflow/plan-verify.md`
**Purpose**: Verify implementation plan

**Use**: `/workflow:plan-verify`

---

#### Quotation Workflows

**Location**: `workflow/quotation/`

##### 68. **generate** - Generate Quotation
**File**: `workflow/quotation/generate.md`
**Purpose**: Generate quotation document

**Use**: `/workflow:quotation:generate`

##### 69. **generate-slide** - Generate Quotation Slides
**File**: `workflow/quotation/generate-slide.md`
**Purpose**: Generate quotation PowerPoint slides

**Use**: `/workflow:quotation:generate-slide`

---

#### Template Workflows

**Location**: `workflow/template/`

##### 70. **generate** - Generate Template
**File**: `workflow/template/generate.md`
**Purpose**: Generate template from Excel

**Use**: `/workflow:template:generate <excel>`

---

#### Tools Workflows

**Location**: `workflow/tools/`

Additional tool-specific workflows for context gathering, conflict resolution, task generation, etc.

---

## Part 3: Workflow System Architecture

### Core Concepts

#### 1. **JSON-Only Data Model**
- **Task State**: Stored in `.task/IMPL-*.json` files
- **Documents**: Read-only generated views
- **Single Source of Truth**: JSON files are authoritative
- **No Synchronization**: Eliminates bidirectional sync complexity

#### 2. **Session Management**

**Active Sessions**:
```
.workflow/active/
└── WFS-[topic-slug]/          # WFS = Workflow Session
    ├── workflow-session.json  # Session metadata (REQUIRED)
    ├── IMPL_PLAN.md           # Planning document (REQUIRED)
    ├── TODO_LIST.md           # Progress tracking (REQUIRED)
    ├── .task/                 # Task definitions (REQUIRED)
    │   ├── IMPL-1.json
    │   ├── IMPL-1.1.json
    │   └── IMPL-2.json
    ├── .brainstorming/        # Optional brainstorming
    ├── .chat/                 # CLI sessions
    ├── .process/              # Analysis results
    ├── .summaries/            # Task summaries
    └── .review/               # Code reviews
```

**Archived Sessions**:
```
.workflow/archives/
└── WFS-[completed-topic]/
```

**Session ID Format**: `WFS-[topic-slug]`
- `WFS` = Workflow Session prefix
- Topic converted to lowercase with hyphens
- Example: "User Auth System" → `WFS-user-auth-system`

#### 3. **Task Hierarchy**

**Maximum 2 Levels**:
```
IMPL-1          # Main task (container)
├── IMPL-1.1    # Subtask (executable)
└── IMPL-1.2    # Subtask (executable)

IMPL-2          # Simple task (executable)
```

**Status Rules**:
- **Container tasks**: Have subtasks (cannot execute directly)
- **Leaf tasks**: Only these can execute
- **Status inheritance**: Parent derived from children

#### 4. **Task JSON Schema**

```json
{
  "id": "IMPL-1.2",
  "title": "Implement JWT authentication",
  "status": "pending|active|completed|blocked|container",
  "context_package_path": ".workflow/WFS-session/.process/context-package.json",

  "meta": {
    "type": "feature|bugfix|refactor|test-gen|test-fix|docs",
    "agent": "@code-developer|@action-planning-agent|@test-fix-agent"
  },

  "context": {
    "requirements": ["JWT authentication", "OAuth2 support"],
    "focus_paths": ["src/auth", "tests/auth"],
    "acceptance": ["JWT validation works", "OAuth flow complete"],
    "parent": "IMPL-1",
    "depends_on": ["IMPL-1.1"],
    "shared_context": {
      "auth_strategy": "JWT with refresh tokens"
    }
  },

  "flow_control": {
    "pre_analysis": [
      {
        "step": "load_context",
        "action": "Load project context",
        "command": "Read(CLAUDE.md)",
        "output_to": "context"
      }
    ],
    "implementation_approach": [
      {
        "step": 1,
        "title": "Setup infrastructure",
        "description": "Install JWT library",
        "modification_points": ["Add to package.json"],
        "logic_flow": ["Install via npm", "Configure"],
        "depends_on": [],
        "output": "jwt_setup"
      }
    ],
    "target_files": [
      "src/auth/login.ts:handleLogin:75-120"
    ]
  }
}
```

**Key Fields**:
- **status**: Task state
- **meta.type**: Task category
- **meta.agent**: Which agent executes it
- **context.focus_paths**: Concrete project paths (no wildcards)
- **context.shared_context**: Data shared across tasks
- **flow_control**: Execution instructions

#### 5. **Flow Control System**

**Two Formats**:

**Inline Format** (Brainstorm):
- Used by: `conceptual-planning-agent`
- Location: In prompt (markdown list)
- Purpose: Temporary context preparation
- 3-5 simple loading steps

**JSON Format** (Implementation):
- Used by: `code-developer`, `test-fix-agent`
- Location: In task JSON file
- Purpose: Persistent task execution
- Complex 10+ step workflows

**Command Types**:
- Bash: `bash(command)`
- Tools: `Read()`, `Glob()`, `Grep()`
- MCP: `mcp__exa__search()`
- CLI: `gemini`, `qwen`, `codex`

**Variable References**: `[variable_name]` for cross-step data flow

---

## Part 4: Usage Patterns

### Common Workflows

#### 1. Generate Proposal from Excel
```bash
# Step 1: Generate template
/template generate deal dealA.xlsx

# Step 2: Review checklist
cat ./output/dealA_*/dealA_checklist.md

# Step 3: Fill placeholders
vim ./output/dealA_*/dealA_template.md

# Step 4: Generate slides
/quotation generate slide ./output/dealA_*/dealA_template.md
```

#### 2. Create and Execute Spec
```bash
# Create specification
/spec create "User authentication system"

# Execute tasks
/spec execute

# Check status
/spec status
```

#### 3. Bug Workflow
```bash
# Create bug report
/bug create "Login fails after 30 minutes"

# Fix bug
/bug fix

# Verify fix
/bug verify
```

#### 4. Full Development Workflow
```bash
# Plan
/workflow:plan "Implement JWT authentication"

# Execute
/workflow:execute

# Review
/workflow:review-session-cycle
```

#### 5. Quick Development
```bash
# Quick plan
/workflow:lite-plan "Add user profile"

# Quick execute
/workflow:lite-execute
```

#### 6. Test-Driven Development
```bash
# Plan tests
/workflow:tdd-plan "User authentication"

# Verify implementation
/workflow:tdd-verify
```

#### 7. Code Review
```bash
# Review module
/workflow:review-module-cycle

# Review session
/workflow:review-session-cycle
```

---

### Skill Invocations

#### Direct Skill Usage
```bash
/annotate "Label this folder"
/project-analyze
/review-code
/ccw-loop "Develop feature"
```

#### Indirect Skill Usage
Skills trigger automatically based on keywords:
- "template" → template skill
- "quotation" → quotation skill
- "analyze project" → project-analyze skill
- "review code" → review-code skill

---

## Part 5: Advanced Concepts

### Complexity Classification

| Complexity | Task Count | Hierarchy | Decomposition |
|------------|------------|-----------|---------------|
| **Simple** | <5 tasks | 1 level | Minimal |
| **Medium** | 5-15 tasks | 2 levels | Moderate |
| **Complex** | >15 tasks | 2 levels | Frequent |

**Characteristics**:
- **Simple**: Bug fixes, small features
- **Medium**: New features, API endpoints
- **Complex**: Major features, architecture refactoring

### Agent Assignment

| Task Type | Agent |
|-----------|--------|
| Planning | @action-planning-agent |
| Implementation | @code-developer |
| Test execution/fixing | @test-fix-agent |
| Review | @universal-executor |

### Context Management

**Context Package**:
- Location: `.workflow/WFS-session/.process/context-package.json`
- Contains: Project structure, dependencies, artifacts
- Loaded in `pre_analysis` steps

**Focus Paths**:
- Format: Array of concrete paths
- Examples: `["src/auth", "tests/auth"]`
- No wildcards allowed

**Shared Context**:
- Data shared across tasks
- Defined in task JSON
- Accessed via `[variable_name]`

### Execution Models

**Synchronous (Main Process)**:
- Commands execute via SlashCommand
- Blocking until complete
- Used by `/ccw` orchestrator

**Asynchronous (Background)**:
- CLI commands in background
- Hook callbacks for results
- Used by `/ccw-coordinator`

---

## Summary

Your `.claude` global directory contains a sophisticated development automation system:

**36 Skills** covering:
- Business workflows (template, quotation)
- Document manipulation (docx, pptx, pdf, xlsx)
- Media processing (FFmpeg, ImageMagick, SAM3, YOLO)
- Development (project-analyze, review-code, issue-manage)
- Meta (skill-creator, skill-generator, skill-tuning)
- Documentation (software-manual, copyright-docs)
- Utilities (google-drive, prompt-enhancer)

**108 Commands** organized as:
- Main orchestrators (ccw, ccw-coordinator)
- Spec commands (create, execute, list, status)
- Bug commands (analyze, create, fix, verify)
- Template & quotation commands
- 30+ workflow commands (plan, execute, debug, test, review, session, brainstorm, ui-design)

**Workflow System**:
- JSON-based task state
- Session management (active/archived)
- 2-level task hierarchy
- Flow control with dependencies
- Multiple execution models

This is a production-grade system designed for enterprise software development with extensive automation capabilities.
