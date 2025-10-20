"""REST API routes for annotation projects."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import Response
from soundevent.io.aoef import to_aeof

from whombat import api, models, schemas
from whombat.api.io import aoef
from whombat.filters.annotation_projects import AnnotationProjectFilter
from whombat.routes.dependencies import (
    Session,
    WhombatSettings,
    get_current_user_dependency,
    get_optional_current_user_dependency,
)
from whombat.routes.types import Limit, Offset

__all__ = ["get_annotation_projects_router"]


def get_annotation_projects_router(settings: WhombatSettings) -> APIRouter:
    current_user_dep = get_current_user_dependency(settings)
    optional_user_dep = get_optional_current_user_dependency(settings)

    router = APIRouter()

    @router.get(
        "/",
        response_model=schemas.Page[schemas.AnnotationProject],
    )
    async def get_annotation_projects(
        session: Session,
        filter: Annotated[
            AnnotationProjectFilter, Depends(AnnotationProjectFilter)  # type: ignore
        ],
        limit: Limit = 10,
        offset: Offset = 0,
        user: models.User | None = Depends(optional_user_dep),
    ) -> schemas.Page[schemas.AnnotationProject]:
        projects, total = await api.annotation_projects.get_many(
            session,
            limit=limit,
            offset=offset,
            filters=[filter],
            user=user,
        )
        return schemas.Page(
            items=projects,
            total=total,
            limit=limit,
            offset=offset,
        )

    @router.post(
        "/",
        response_model=schemas.AnnotationProject,
    )
    async def create_annotation_project(
        session: Session,
        data: schemas.AnnotationProjectCreate,
        user: models.User = Depends(current_user_dep),
    ) -> schemas.AnnotationProject:
        annotation_project = await api.annotation_projects.create(
            session,
            name=data.name,
            description=data.description,
            annotation_instructions=data.annotation_instructions,
            user=user,
            visibility=data.visibility,
            owner_group_id=data.owner_group_id,
        )
        await session.commit()
        return annotation_project

    @router.get(
        "/detail/",
        response_model=schemas.AnnotationProject,
    )
    async def get_annotation_project(
        session: Session,
        annotation_project_uuid: UUID,
        user: models.User | None = Depends(optional_user_dep),
    ) -> schemas.AnnotationProject:
        return await api.annotation_projects.get(
            session,
            annotation_project_uuid,
            user=user,
        )

    @router.patch(
        "/detail/",
        response_model=schemas.AnnotationProject,
    )
    async def update_annotation_project(
        session: Session,
        annotation_project_uuid: UUID,
        data: schemas.AnnotationProjectUpdate,
        user: models.User = Depends(current_user_dep),
    ) -> schemas.AnnotationProject:
        annotation_project = await api.annotation_projects.get(
            session,
            annotation_project_uuid,
            user=user,
        )
        annotation_project = await api.annotation_projects.update(
            session,
            annotation_project,
            data,
            user=user,
        )
        await session.commit()
        return annotation_project

    @router.delete(
        "/detail/",
        response_model=schemas.AnnotationProject,
    )
    async def delete_annotation_project(
        session: Session,
        annotation_project_uuid: UUID,
        user: models.User = Depends(current_user_dep),
    ) -> schemas.AnnotationProject:
        annotation_project = await api.annotation_projects.get(
            session,
            annotation_project_uuid,
            user=user,
        )
        project = await api.annotation_projects.delete(
            session,
            annotation_project,
            user=user,
        )
        await session.commit()
        return project

    @router.post(
        "/detail/tags/",
        response_model=schemas.AnnotationProject,
    )
    async def add_tag_to_annotation_project(
        session: Session,
        annotation_project_uuid: UUID,
        key: str,
        value: str,
        user: models.User = Depends(current_user_dep),
    ) -> schemas.AnnotationProject:
        annotation_project = await api.annotation_projects.get(
            session,
            annotation_project_uuid,
            user=user,
        )
        tag = await api.tags.get(session, (key, value))
        project = await api.annotation_projects.add_tag(
            session,
            annotation_project,
            tag,
            user=user,
        )
        await session.commit()
        return project

    @router.delete(
        "/detail/tags/",
        response_model=schemas.AnnotationProject,
    )
    async def remove_tag_from_annotation_project(
        session: Session,
        annotation_project_uuid: UUID,
        key: str,
        value: str,
        user: models.User = Depends(current_user_dep),
    ) -> schemas.AnnotationProject:
        annotation_project = await api.annotation_projects.get(
            session,
            annotation_project_uuid,
            user=user,
        )
        tag = await api.tags.get(session, (key, value))
        project = await api.annotation_projects.remove_tag(
            session,
            annotation_project,
            tag,
            user=user,
        )
        await session.commit()
        return project

    @router.get(
        "/detail/download/",
        response_model=schemas.Page[schemas.Recording],
    )
    async def download_annotation_project(
        session: Session,
        annotation_project_uuid: UUID,
        settings: WhombatSettings,
        user: models.User | None = Depends(optional_user_dep),
    ) -> Response:
        audio_dir = settings.audio_dir

        whombat_project = await api.annotation_projects.get(
            session,
            annotation_project_uuid,
            user=user,
        )

        base_dir = await api.annotation_projects.get_base_dir(
            session,
            whombat_project,
        )

        project = await api.annotation_projects.to_soundevent(
            session,
            whombat_project,
            audio_dir=audio_dir / base_dir,
        )

        obj = to_aeof(project, audio_dir=audio_dir / base_dir)
        filename = f"{project.name}_{obj.created_on.isoformat()}.json"
        return Response(
            obj.model_dump_json(),
            media_type="application/json",
            status_code=200,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    @router.post(
        "/import/",
        response_model=schemas.AnnotationProject,
    )
    async def import_annotation_project(
        settings: WhombatSettings,
        session: Session,
        annotation_project: UploadFile,
        user: models.User = Depends(current_user_dep),
    ) -> schemas.AnnotationProject:
        db_project = await aoef.import_annotation_project(
            session,
            annotation_project.file,
            audio_dir=settings.audio_dir,
            base_audio_dir=settings.audio_dir,
        )
        await session.commit()
        await session.refresh(db_project)
        return schemas.AnnotationProject.model_validate(db_project)

    return router
