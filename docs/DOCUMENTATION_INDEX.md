# Foldline Documentation Index

**Last Updated:** 2025-11-22

Quick reference guide to all documentation in the Foldline project.

---

## 📢 Recent Changes (2025-11-22)

**Documentation Consolidation:**
- ✅ Moved `FOLDLINE_DESIGN_SPEC.md` to `design/` directory
- ✅ Archived `IMPLEMENTATION_PLAN.md`, `VIEWS_ROADMAP_ASSESSMENT.md`, and `payment_planning.md`
- ✅ Moved legacy test scripts from root to `tools/dev-scripts/`
- ✅ Updated all references to use `PAYMENT_ARCHITECTURE.md` instead of `payment_planning.md`
- ✅ Enhanced archive documentation with complete document history

**Why:** Reduce clutter in root directory, consolidate related docs, and clarify active vs. archived documentation.

---

## 📋 Start Here

### New to Foldline?
1. **[README.md](README.md)** - Project overview, setup instructions, and quick start
2. **[PRE_COMMERCIAL_MVP_PLAN.md](PRE_COMMERCIAL_MVP_PLAN.md)** - Current development roadmap
3. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Codebase organization (if exists)

### Want to Contribute?
1. **[PRE_COMMERCIAL_MVP_PLAN.md](PRE_COMMERCIAL_MVP_PLAN.md)** - See current priorities and task breakdown
2. **[TESTING_PLAN.md](TESTING_PLAN.md)** - Testing strategy and guidelines
3. **[FOLDLINE_DESIGN_SPEC.md](design/FOLDLINE_DESIGN_SPEC.md)** - Design system and UI patterns (if exists)

---

## 🎯 Current Planning Documents

### Core Plans (Active)

#### [PRE_COMMERCIAL_MVP_PLAN.md](PRE_COMMERCIAL_MVP_PLAN.md)
**Status:** 🟢 ACTIVE - Primary planning document
**Purpose:** Unified pre-commercial MVP roadmap (5-6 weeks)
**Use For:**
- Current implementation priorities
- Week-by-week task breakdown
- Success criteria and acceptance tests
- Technical architecture decisions

**Key Contents:**
- Week 1: GDPR Import + Schema Enhancement
- Week 2: Garmin Express Detection (macOS)
- Week 3: Garmin Express Sync + Windows Support
- Week 4: Visualization (Plotly)
- Week 5: Basic Analytics
- Week 6: Polish & Beta Testing

**What's Included in MVP:**
- ✅ GDPR import
- ✅ Garmin Express auto-sync
- ✅ Basic visualization (heatmaps, trends)
- ✅ Core metric queries

**What's Deferred to Commercial Launch:**
- ⏭️ Payment system
- ⏭️ Advanced analytics
- ⏭️ Power user features

---

#### [CONTINUAL_SYNC_SPEC.md](CONTINUAL_SYNC_SPEC.md)
**Status:** 🟢 ACTIVE - Technical specification
**Purpose:** Sync architecture and UX requirements
**Use For:**
- Garmin Express integration details
- Sync mode specifications
- File deduplication logic
- Privacy guarantees

**Key Contents:**
- §2: Three sync modes (Garmin Express, Manual, Watched Folders)
- §3: Garmin Express implementation (device detection, sync triggering, folder scanning)
- §6: Deduplication & file registry schema
- §7: FIT ingestion pipeline
- §8: UX requirements and onboarding flows
- §10: Privacy & security guarantees

**Implemented:**
- ✅ Device detection (§3.2)
- ✅ Folder scanning algorithm (§3.4)
- ✅ Enhanced file registry schema (§6.1)
- ✅ Deduplication strategy (§6.2)

**In Progress:**
- 🟨 GDPR import integration (§7)
- 🟨 Settings panel UI (§9)

**Deferred:**
- ⏭️ Watched folder sync (Mode 3)
- ⏭️ Continuous file watching (§11)

---

### Reference Documents (Active)

#### [FOLDLINE_HANDOFF.md](FOLDLINE_HANDOFF.md)
**Status:** 🟢 ACTIVE - Reference material
**Purpose:** Knowledge transfer from gar-mining project
**Use For:**
- Algorithm implementations (health score, recovery, correlations)
- Visualization patterns (Plotly examples)
- Data model insights
- Proven design decisions

**Key Contents:**
- Lines 78-400: Data models and schemas
- Lines 744-2612: Analytics algorithms (with Python code)
- Lines 1095-1380: Visualization patterns (Plotly examples)
- Design decisions and lessons learned

**How to Use:**
- Copy-paste algorithm implementations
- Reference Plotly chart examples
- Understand field mappings for GDPR data

---

#### [TESTING_PLAN.md](TESTING_PLAN.md)
**Status:** 🟢 ACTIVE - Testing strategy
**Purpose:** Pragmatic testing approach
**Use For:**
- What to test (priorities)
- What NOT to test (avoid waste)
- Infrastructure setup
- Test writing guidelines

**Key Contents:**
- Lines 9-105: What to test (data integrity first)
- Lines 132-163: What NOT to test
- Lines 166-274: Infrastructure setup
- Lines 275-434: Phase-by-phase testing plan

---

#### [PAYMENT_ARCHITECTURE.md](PAYMENT_ARCHITECTURE.md)
**Status:** 🟡 DEFERRED - Still relevant for commercial launch
**Purpose:** Payment system and licensing architecture
**Use For:** Commercial launch preparation (post-MVP)

**Key Contents:**
- Lemon Squeezy integration architecture
- Pay-what-you-want model details
- License activation flow
- Free vs. Premium feature matrix
- Privacy-first payment approach

**Timeline:** Post pre-commercial MVP (after beta testing)

---

#### [EFF_DONATIONS.md](EFF_DONATIONS.md)
**Status:** 🟢 ACTIVE - Ongoing commitment
**Purpose:** EFF donation commitment and tracking methodology
**Use For:** Understanding revenue allocation and donation calculations

**Key Contents:**
- 10% net revenue commitment to EFF
- Revenue calculation methodology
- Donation tracking tools (in `tools/donations/`)
- Transparency and reporting approach

**Why EFF:** Aligns with Foldline's privacy-first principles

---

## 📁 Design & Architecture

### [design/FOLDLINE_DESIGN_SPEC.md](design/FOLDLINE_DESIGN_SPEC.md)
**Status:** 🟢 ACTIVE
**Purpose:** Design system, UI patterns, component library
**Use For:** Building consistent UI components

**Key Contents:**
- Brand essence and visual philosophy
- Logo system and usage guidelines
- Color system and design tokens
- Typography and layout principles
- Component specifications

### [design/](design/)
**Status:** 🟢 ACTIVE - Design system directory
**Contains:**
- `FOLDLINE_DESIGN_SPEC.md` - Main design specification
- `BRAND_TOKENS.css` - CSS design tokens (source of truth)
- `TYPOGRAPHY.css` - Font definitions
- `ACCESSIBILITY.md` - Accessibility guidelines
- `COMPONENT_STATES.md` - Component state specifications
- `DATA_TABLES.md`, `DATA_VISUALIZATION.md`, `FORMS.md` - Component guides
- `FILE_CONSOLIDATION_STRATEGY.md` - Design token management strategy

### [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
**Status:** 🟢 ACTIVE
**Purpose:** Directory structure and organization
**Use For:** Understanding codebase layout (Frontend, Marketing, Backend separation)

---

## 🗄️ Archived Documentation

### [docs/archive/](docs/archive/)
**Status:** 🔴 ARCHIVED - Historical reference only

**Integration Planning Suite (4 documents):**
- **INTEGRATION_PLAN.md** - Original 6-phase roadmap
- **INTEGRATION_ROADMAP.md** - Original week-by-week guide
- **INTEGRATION_ANALYSIS.md** - Original gap analysis
- **INTEGRATION_SUMMARY.md** - Original executive summary

**Feature Planning Documents (3 documents):**
- **IMPLEMENTATION_PLAN.md** - Fitness tracking features implementation plan
- **VIEWS_ROADMAP_ASSESSMENT.md** - Visualization views assessment
- **payment_planning.md** - Original payment planning (superseded by PAYMENT_ARCHITECTURE.md)

**Why Archived:**
- Integration docs: Assumed commercial launch as MVP (now pre-commercial), didn't include Garmin Express sync
- Feature docs: Point-in-time planning completed or outdated
- Payment docs: Superseded by more comprehensive PAYMENT_ARCHITECTURE.md

**Still Useful For:**
- Reference on advanced analytics algorithms
- Understanding planning evolution
- Historical context for decision-making
- Post-commercial roadmap ideas

**See:** [docs/archive/README.md](docs/archive/README.md) for complete details and document history

---

## 📊 Documentation by Topic

### Planning & Roadmap
- 🟢 [PRE_COMMERCIAL_MVP_PLAN.md](PRE_COMMERCIAL_MVP_PLAN.md) - Current plan
- 🔴 [docs/archive/INTEGRATION_PLAN.md](docs/archive/INTEGRATION_PLAN.md) - Archived (reference only)

### Data Import & Sync
- 🟢 [CONTINUAL_SYNC_SPEC.md](CONTINUAL_SYNC_SPEC.md) - Sync architecture
- 🟢 [FOLDLINE_HANDOFF.md](FOLDLINE_HANDOFF.md) - GDPR field mappings (reference)

### Analytics & Algorithms
- 🟢 [FOLDLINE_HANDOFF.md](FOLDLINE_HANDOFF.md) - Algorithm implementations
- 🔴 [docs/archive/INTEGRATION_PLAN.md](docs/archive/INTEGRATION_PLAN.md) - Algorithm descriptions (archived)

### Visualization
- 🟢 [FOLDLINE_HANDOFF.md](FOLDLINE_HANDOFF.md) - Plotly examples
- 🟢 [PRE_COMMERCIAL_MVP_PLAN.md](PRE_COMMERCIAL_MVP_PLAN.md) - Week 4 implementation

### Testing
- 🟢 [TESTING_PLAN.md](TESTING_PLAN.md) - Testing strategy
- 🟢 [PRE_COMMERCIAL_MVP_PLAN.md](PRE_COMMERCIAL_MVP_PLAN.md) - Acceptance criteria per week

### Payment & Licensing
- 🟡 [PAYMENT_ARCHITECTURE.md](PAYMENT_ARCHITECTURE.md) - Payment system architecture (deferred to commercial launch)
- 🟢 [EFF_DONATIONS.md](EFF_DONATIONS.md) - EFF donation commitment
- 🔴 [docs/archive/payment_planning.md](docs/archive/payment_planning.md) - Original payment planning (archived)

### Design & UX
- 🟢 [CONTINUAL_SYNC_SPEC.md](CONTINUAL_SYNC_SPEC.md) - Sync UX requirements (§8)
- 🟢 [design/FOLDLINE_DESIGN_SPEC.md](design/FOLDLINE_DESIGN_SPEC.md) - Design system
- 🟢 [design/](design/) - Complete design system directory

### Development Tools
- 🟢 [tools/dev-scripts/](tools/dev-scripts/) - Legacy test and debugging scripts
- 🟢 [tools/donations/](tools/donations/) - EFF donation tracking tools
- 🟢 [scripts/](scripts/) - Build and development scripts

---

## 🔄 Document Status Legend

- 🟢 **ACTIVE** - Current, use for implementation
- 🟡 **DEFERRED** - Relevant but not immediate priority
- 🟨 **IN PROGRESS** - Being actively developed
- 🔴 **ARCHIVED** - Superseded, kept for reference only

---

## 📝 How to Keep Documentation Updated

### When to Update

**Update PRE_COMMERCIAL_MVP_PLAN.md when:**
- Completing a weekly milestone
- Changing priorities or timeline
- Discovering new requirements
- Shifting resources or scope

**Update CONTINUAL_SYNC_SPEC.md when:**
- Adding new sync modes
- Changing file registry schema
- Updating privacy guarantees
- Modifying UX flows

**Update TESTING_PLAN.md when:**
- Adding new test categories
- Changing testing infrastructure
- Updating test priorities

**Update this index when:**
- Creating new documentation
- Archiving old documentation
- Changing document status

### Who Maintains What

| Document | Owner | Update Frequency |
|----------|-------|------------------|
| PRE_COMMERCIAL_MVP_PLAN.md | Product Lead | Weekly (during MVP) |
| CONTINUAL_SYNC_SPEC.md | Engineering Lead | As needed |
| TESTING_PLAN.md | QA Lead | Monthly |
| FOLDLINE_HANDOFF.md | Reference Only | No updates |
| DOCUMENTATION_INDEX.md | Project Lead | When docs change |

---

## 🚀 Quick Task Lookup

### "I want to implement..."

**...Garmin Express device detection**
→ [CONTINUAL_SYNC_SPEC.md](CONTINUAL_SYNC_SPEC.md) §3.2 + [PRE_COMMERCIAL_MVP_PLAN.md](PRE_COMMERCIAL_MVP_PLAN.md) Week 2

**...GDPR import**
→ [PRE_COMMERCIAL_MVP_PLAN.md](PRE_COMMERCIAL_MVP_PLAN.md) Week 1 + [FOLDLINE_HANDOFF.md](FOLDLINE_HANDOFF.md) (field mappings)

**...Visualization**
→ [PRE_COMMERCIAL_MVP_PLAN.md](PRE_COMMERCIAL_MVP_PLAN.md) Week 4 + [FOLDLINE_HANDOFF.md](FOLDLINE_HANDOFF.md) lines 1095-1380

**...Health Score algorithm**
→ Deferred to post-MVP, see [FOLDLINE_HANDOFF.md](FOLDLINE_HANDOFF.md) lines 744-2612

**...Payment system**
→ Deferred to commercial launch, see [PAYMENT_ARCHITECTURE.md](PAYMENT_ARCHITECTURE.md)

---

## 📞 Getting Help

### Document Questions
- Check this index first
- Read document headers for purpose/scope
- Check "Related Active Documentation" sections

### Implementation Questions
- Start with [PRE_COMMERCIAL_MVP_PLAN.md](PRE_COMMERCIAL_MVP_PLAN.md)
- Reference [CONTINUAL_SYNC_SPEC.md](CONTINUAL_SYNC_SPEC.md) for sync details
- Check [FOLDLINE_HANDOFF.md](FOLDLINE_HANDOFF.md) for algorithm examples

### Planning Questions
- Review [PRE_COMMERCIAL_MVP_PLAN.md](PRE_COMMERCIAL_MVP_PLAN.md)
- Check [docs/archive/](docs/archive/) for context on planning evolution
- See "Post-Pre-Commercial Roadmap" section in MVP plan

---

**Last Review:** 2025-11-22
**Next Review:** After Week 3 of MVP (Garmin Express sync complete)
