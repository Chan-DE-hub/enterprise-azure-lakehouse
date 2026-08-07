"""Load and render packaged monitoring SQL resources."""

import re
from collections.abc import Mapping
from importlib.resources import files

EVENT_LOG_SOURCE_TOKEN = "__EVENT_LOG_SOURCE__"

PIPELINE_ID_PATTERN = re.compile(
    r"^[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}$"
)

TEMPLATE_TOKEN_PATTERN = re.compile(
    r"__[A-Z][A-Z0-9_]*__",
)


def load_monitoring_query(resource_name: str) -> str:
    """Return one packaged monitoring SQL query."""
    resource = files("enterprise_lakehouse.monitoring.sql").joinpath(
        resource_name,
    )

    if not resource.is_file():
        raise FileNotFoundError(
            f"Monitoring SQL resource not found: {resource_name}",
        )

    return resource.read_text(encoding="utf-8").strip()


def render_monitoring_query(
    *,
    resource_name: str,
    replacements: Mapping[str, str],
) -> str:
    """Render one monitoring SQL template using explicit replacements."""
    query = load_monitoring_query(resource_name)

    for token, replacement in replacements.items():
        if token not in query:
            raise ValueError(
                f"Template token not found: {token}",
            )

        query = query.replace(
            token,
            replacement,
        )

    unresolved_tokens = sorted(
        set(TEMPLATE_TOKEN_PATTERN.findall(query)),
    )

    if unresolved_tokens:
        raise ValueError(
            f"Unresolved monitoring template tokens: {', '.join(unresolved_tokens)}",
        )

    return query


def render_pipeline_event_log_query(
    *,
    resource_name: str,
    pipeline_id: str,
) -> str:
    """Render a monitoring query against one native pipeline event log."""
    if PIPELINE_ID_PATTERN.fullmatch(pipeline_id) is None:
        raise ValueError(
            f"Invalid pipeline_id: {pipeline_id!r}",
        )

    return render_monitoring_query(
        resource_name=resource_name,
        replacements={
            EVENT_LOG_SOURCE_TOKEN: f"event_log('{pipeline_id}')",
        },
    )
