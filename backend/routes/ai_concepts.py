"""AI/ML concepts study routes."""
from fastapi import APIRouter, HTTPException

from ai_concepts_data import (
    AI_PHASES,
    AI_CONCEPTS,
    get_ai_concept_by_id,
    get_ai_concepts_by_phase,
    get_ai_concepts_by_tag,
    get_all_ai_tags,
)

router = APIRouter()


@router.get("/ai-concepts/overview")
async def get_overview():
    """Get full AI/ML curriculum overview."""
    phases = {}
    for phase_num, phase_info in AI_PHASES.items():
        concepts = get_ai_concepts_by_phase(phase_num)
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
        "total_concepts": len(AI_CONCEPTS),
        "total_phases": len(AI_PHASES),
        "phases": phases,
        "all_tags": get_all_ai_tags(),
    }


@router.get("/ai-concepts/concepts")
async def list_concepts(phase: int = None, tag: str = None):
    """List concepts, optionally filtered by phase or tag."""
    if phase is not None:
        concepts = get_ai_concepts_by_phase(phase)
    elif tag is not None:
        concepts = get_ai_concepts_by_tag(tag)
    else:
        concepts = AI_CONCEPTS
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


@router.get("/ai-concepts/concept/{concept_id}")
async def get_concept(concept_id: int):
    """Get full detail for a single AI/ML concept."""
    concept = get_ai_concept_by_id(concept_id)
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    return concept
