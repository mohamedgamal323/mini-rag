def validate_project_id(project_id: str) -> None:
    if not project_id.isalnum():
        raise ValueError("project_id must be alphanumeric")