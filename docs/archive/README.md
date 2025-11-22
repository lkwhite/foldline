# Archived Documentation

**Date Archived:** 2025-11-22

This directory contains documentation that has been **superseded** by more recent planning documents but is preserved for historical reference and context.

---

## Archived Documents

### Integration Planning Suite (Archived 2025-11-22)

These four documents were created to plan the integration of gar-mining functionality into Foldline. They have been **consolidated and updated** into `PRE_COMMERCIAL_MVP_PLAN.md`.

**Why Archived:**
- Original plans assumed commercial launch as MVP
- Did not include Garmin Express auto-sync (added via CONTINUAL_SYNC_SPEC.md)
- Strategy shifted to pre-commercial beta before payment system

**What Replaced Them:**
- `PRE_COMMERCIAL_MVP_PLAN.md` - Unified plan integrating all sources

---

#### 1. INTEGRATION_PLAN.md (992 lines)
**Original Purpose:** Comprehensive 6-phase roadmap for porting gar-mining to Foldline

**Contents:**
- Detailed comparison: gar-mining vs. Foldline
- 6 implementation phases (Analytics, Visualization, GDPR Import, Schema, Advanced Analytics, Future Features)
- Critical gap analysis
- Proven design patterns to adopt
- Complete migration checklist

**Status:** Content integrated into PRE_COMMERCIAL_MVP_PLAN.md with updated priorities

---

#### 2. INTEGRATION_ROADMAP.md (688 lines)
**Original Purpose:** Week-by-week implementation guide for MVP launch

**Contents:**
- Visual 4-6 week MVP timeline
- Weekly task breakdowns
- Current vs. target state comparisons
- Implementation checklist
- Success criteria

**Status:** Roadmap updated in PRE_COMMERCIAL_MVP_PLAN.md to include Garmin Express sync and defer payment system

---

#### 3. INTEGRATION_ANALYSIS.md (603 lines)
**Original Purpose:** Gap analysis and strategy comparison

**Contents:**
- Detailed gap analysis matrix
- Strategy A vs. Strategy B comparison ("Launch First" vs. "Complete Integration")
- Recommendations for analytics implementation order
- Risk assessment
- Decision framework

**Status:** Recommendations incorporated into PRE_COMMERCIAL_MVP_PLAN.md with pre-commercial focus

---

#### 4. INTEGRATION_SUMMARY.md (429 lines)
**Original Purpose:** Executive summary of integration analysis

**Contents:**
- High-level overview of planning docs
- Gap analysis summary
- Recommended strategy (MVP in 4-6 weeks)
- Next actions

**Status:** Summary concept retained, content updated in PRE_COMMERCIAL_MVP_PLAN.md

---

## Why These Were Superseded

### Context Change: Pre-Commercial MVP
After these docs were created, the project strategy shifted:
- **Original:** Launch for revenue (payment system first)
- **Updated:** Pre-commercial beta for validation (skip payment, add Garmin Express sync)

### New Input: CONTINUAL_SYNC_SPEC.md
A detailed sync specification was developed separately, which included:
- Garmin Express auto-sync as primary UX
- Three sync modes (Express, Manual, Watched Folders)
- Enhanced file registry for change tracking
- Pull-triggered sync model (no background daemons)

This was not accounted for in the original integration planning suite.

### Consolidation Benefits
The original four documents had overlapping content:
- INTEGRATION_SUMMARY.md summarized INTEGRATION_ANALYSIS.md
- INTEGRATION_ROADMAP.md visualized INTEGRATION_PLAN.md
- All four discussed similar topics from different angles

**PRE_COMMERCIAL_MVP_PLAN.md** consolidates everything into a single source of truth.

---

## How to Use These Archived Docs

### ✅ Still Valuable For:
- **Reference:** Detailed algorithm descriptions from gar-mining
- **Context:** Understanding how the plan evolved
- **Comparison:** Original vs. updated priorities
- **Completeness:** Full 6-phase roadmap (useful for post-commercial planning)

### ❌ Don't Use For:
- **Current implementation guidance** → Use `PRE_COMMERCIAL_MVP_PLAN.md`
- **Timeline planning** → Use `PRE_COMMERCIAL_MVP_PLAN.md`
- **Priority decisions** → Use `PRE_COMMERCIAL_MVP_PLAN.md`

---

## Related Active Documentation

For current planning, see:
- **`PRE_COMMERCIAL_MVP_PLAN.md`** - Current unified plan (5-6 week pre-commercial MVP)
- **`CONTINUAL_SYNC_SPEC.md`** - Sync architecture and UX requirements
- **`FOLDLINE_HANDOFF.md`** - Source material from gar-mining (algorithms, patterns)
- **`TESTING_PLAN.md`** - Testing strategy (still applicable)
- **`payment_planning.md`** - Payment system plan (deferred to commercial launch)

---

## Document History

| Document | Created | Archived | Replaced By |
|----------|---------|----------|-------------|
| INTEGRATION_PLAN.md | 2025-11-22 | 2025-11-22 | PRE_COMMERCIAL_MVP_PLAN.md |
| INTEGRATION_ROADMAP.md | 2025-11-22 | 2025-11-22 | PRE_COMMERCIAL_MVP_PLAN.md |
| INTEGRATION_ANALYSIS.md | 2025-11-22 | 2025-11-22 | PRE_COMMERCIAL_MVP_PLAN.md |
| INTEGRATION_SUMMARY.md | 2025-11-22 | 2025-11-22 | PRE_COMMERCIAL_MVP_PLAN.md |

**Note:** These documents were created and archived on the same day because the strategy shifted during the documentation process after CONTINUAL_SYNC_SPEC.md was introduced.
