"""Meta-analysis capability.

Wraps :class:`MetaAnalysisPipeline` to implement a system-review /
meta-analysis flow on top of the existing research machinery.
"""

from __future__ import annotations

from typing import Any

from deeptutor.agents.research.meta_analysis.request_config import (
    MetaAnalysisRequestConfig,
    validate_meta_analysis_request_config,
)
from deeptutor.agents.research.pipeline import ResearchPipeline, SubTopicItem
from deeptutor.core.capability_protocol import CapabilityManifest, TurnCapability
from deeptutor.core.context import UnifiedContext
from deeptutor.runtime.request_contracts import get_capability_request_schema
from deeptutor.runtime.stream_bus import StreamBus
from deeptutor.services.config import load_config_with_main


class MetaAnalysisCapability(TurnCapability):
    manifest = CapabilityManifest(
        name="meta_analysis",
        description="Systematic-review-style meta analysis with protocol review, screening, and evidence synthesis.",
        stages=["protocol", "screening", "researching", "synthesis"],
        tools_used=["rag", "web_search", "paper_search", "exec"],
        cli_aliases=["meta_analysis"],
        request_schema=get_capability_request_schema("meta_analysis"),
    )

    async def run(self, context: UnifiedContext, stream: StreamBus) -> None:
        kb_name = context.knowledge_bases[0] if context.knowledge_bases else None
        request_config = validate_meta_analysis_request_config(context.config_overrides)

        enabled_tools = list(context.enabled_tools or [])
        base_config = load_config_with_main("main.yaml")

        runtime_config = {
            **base_config,
            "system": {
                "output_base_dir": "./data/user/workspace/chat/meta_analysis",
                "reports_dir": "./data/user/workspace/chat/meta_analysis/reports",
            },
            "intent": request_config.model_dump(),
        }

        confirmed_outline_items: list[SubTopicItem] | None = None
        if request_config.confirmed_outline is not None:
            confirmed_outline_items = [
                SubTopicItem(title=item.title, overview=item.overview or "")
                for item in request_config.confirmed_outline
            ]

        pipeline = ResearchPipeline(
            language=context.language,
            runtime_config=runtime_config,
            kb_name=kb_name,
            enabled_tools=enabled_tools,
        )
        result = await pipeline.run(
            context=context,
            topic=context.user_message,
            confirmed_outline=confirmed_outline_items,
            attachments=context.attachments,
            stream=stream,
        )

        if result.get("outline_preview"):
            research_config: dict[str, Any] = {
                "mode": "meta_analysis",
                "depth": request_config.depth,
                "max_studies": request_config.max_studies,
                "min_quality": request_config.min_quality,
                "effect_type": request_config.effect_type,
            }
            await stream.result(
                {**result, "research_config": research_config},
                source=self.name,
            )
