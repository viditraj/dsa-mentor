"""System Design study routes."""
from fastapi import APIRouter, HTTPException

from system_design_data import (
    SYSTEM_DESIGN_PHASES,
    SYSTEM_DESIGN_CONCEPTS,
    get_concept_by_id,
    get_concepts_by_phase,
    get_concepts_by_tag,
    get_all_tags,
)

router = APIRouter()


@router.get("/system-design/overview")
async def get_overview():
    """Get full System Design curriculum overview."""
    phases = {}
    for phase_num, phase_info in SYSTEM_DESIGN_PHASES.items():
        concepts = get_concepts_by_phase(phase_num)
        phases[phase_num] = {
            **phase_info,
            "concept_count": len(concepts),
            "concepts_preview": [
                {
                    "id": c["id"],
                    "title": c["title"],
                    "difficulty": c["difficulty"],
                    "estimated_minutes": c["estimated_minutes"],
                    "frequency": c["frequency"],
                    "tags": c["tags"],
                    "companies_asking": c["companies_asking"][:4],
                }
                for c in concepts
            ],
        }
    return {
        "total_concepts": len(SYSTEM_DESIGN_CONCEPTS),
        "total_phases": len(SYSTEM_DESIGN_PHASES),
        "phases": phases,
        "all_tags": get_all_tags(),
    }


@router.get("/system-design/concepts")
async def list_concepts(phase: int = None, tag: str = None):
    """List concepts, optionally filtered by phase or tag."""
    if phase is not None:
        concepts = get_concepts_by_phase(phase)
    elif tag is not None:
        concepts = get_concepts_by_tag(tag)
    else:
        concepts = SYSTEM_DESIGN_CONCEPTS
    return [
        {
            "id": c["id"],
            "title": c["title"],
            "phase": c["phase"],
            "difficulty": c["difficulty"],
            "estimated_minutes": c["estimated_minutes"],
            "tags": c["tags"],
            "frequency": c["frequency"],
            "companies_asking": c["companies_asking"],
            "cheat_sheet": c["cheat_sheet"],
        }
        for c in concepts
    ]


@router.get("/system-design/concept/{concept_id}")
async def get_concept(concept_id: int):
    """Get full detail for a single System Design concept."""
    concept = get_concept_by_id(concept_id)
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    return concept
