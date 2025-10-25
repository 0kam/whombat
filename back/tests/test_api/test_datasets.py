"""Test suite for the datasets API module."""

import uuid
from collections.abc import Callable
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from whombat import api, exceptions, models, schemas


async def test_created_dataset_is_stored_in_the_database(
    session: AsyncSession,
    dataset: schemas.Dataset,
):
    """Test that a created dataset is stored in the database."""
    stmt = select(models.Dataset).where(models.Dataset.id == dataset.id)
    result = await session.execute(stmt)
    retrieved_dataset = result.unique().scalar_one_or_none()
    assert retrieved_dataset is not None
    assert retrieved_dataset.id == dataset.id
    assert retrieved_dataset.name == dataset.name
    assert retrieved_dataset.description == dataset.description


async def test_dataset_is_stored_with_relative_audio_dir(
    session: AsyncSession,
    audio_dir: Path,
    user: schemas.SimpleUser,
    random_wav_factory: Callable[..., Path],
):
    """Test that a dataset is stored with a relative audio dir."""
    dataset_audio_dir = audio_dir / "dataset_audio_dir"
    dataset_audio_dir.mkdir()
    random_wav_factory(dataset_audio_dir / "recording.wav")
    dataset = await api.datasets.create(
        session,
        name="test_dataset",
        description="This is a test dataset.",
        dataset_dir=dataset_audio_dir,
        audio_dir=audio_dir,
        user=user,
        visibility=models.VisibilityLevel.PUBLIC,
    )
    # Make sure the audio dir is stored as a relative path
    stmt = select(models.Dataset).where(models.Dataset.id == dataset.id)
    result = await session.execute(stmt)
    retrieved_dataset = result.unique().scalar_one_or_none()
    assert retrieved_dataset is not None
    assert retrieved_dataset.audio_dir == Path("dataset_audio_dir")


async def test_create_dataset_requires_audio_files(
    session: AsyncSession,
    audio_dir: Path,
    user: schemas.SimpleUser,
):
    """Ensure dataset creation fails when no compatible audio files exist."""
    dataset_audio_dir = audio_dir / "dataset_audio_dir"
    dataset_audio_dir.mkdir()
    with pytest.raises(exceptions.InvalidDataError):
        await api.datasets.create(
            session,
            name="test_dataset",
            description="This is a test dataset.",
            dataset_dir=dataset_audio_dir,
            audio_dir=audio_dir,
            user=user,
            visibility=models.VisibilityLevel.PUBLIC,
        )


async def test_create_dataset_fails_if_name_is_not_unique(
    session: AsyncSession,
    audio_dir: Path,
    user: schemas.SimpleUser,
    random_wav_factory: Callable[..., Path],
):
    """Test that creating a dataset fails if the name is not unique."""
    audio_dir1 = audio_dir / "audio1"
    audio_dir2 = audio_dir / "audio2"
    audio_dir1.mkdir()
    audio_dir2.mkdir()
    random_wav_factory(audio_dir1 / "recording.wav")
    random_wav_factory(audio_dir2 / "recording.wav")
    await api.datasets.create(
        session,
        name="test_dataset",
        description="This is a test dataset.",
        dataset_dir=audio_dir1,
        audio_dir=audio_dir,
        user=user,
        visibility=models.VisibilityLevel.PUBLIC,
    )
    with pytest.raises(exceptions.DuplicateObjectError):
        await api.datasets.create(
            session,
            name="test_dataset",
            description="This is a test dataset.",
            dataset_dir=audio_dir2,
            audio_dir=audio_dir,
            user=user,
            visibility=models.VisibilityLevel.PUBLIC,
        )


async def test_get_dataset_by_uuid(
    session: AsyncSession, dataset: schemas.Dataset
):
    """Test getting a dataset by UUID."""
    retrieved_dataset = await api.datasets.get(session, dataset.uuid)
    assert isinstance(retrieved_dataset, schemas.Dataset)
    assert retrieved_dataset.id == dataset.id


async def test_get_dataset_by_uuid_fails_when_uuid_does_not_exist(
    session: AsyncSession,
):
    """Test that getting a dataset by UUID fails when nonexisting."""
    with pytest.raises(exceptions.NotFoundError):
        await api.datasets.get(session, uuid.uuid4())


async def test_get_dataset_by_name(
    session: AsyncSession, dataset: schemas.Dataset
):
    """Test getting a dataset by name."""
    retrieved_dataset = await api.datasets.get_by_name(session, dataset.name)
    assert isinstance(retrieved_dataset, schemas.Dataset)
    assert retrieved_dataset.id == dataset.id


async def test_get_dataset_by_name_fails_when_name_does_not_exist(
    session: AsyncSession,
):
    """Test that getting a dataset by name fails when nonexisting."""
    with pytest.raises(exceptions.NotFoundError):
        await api.datasets.get_by_name(
            session,
            name="nonexisting_dataset",
        )


async def test_get_dataset_by_audio_dir(
    session: AsyncSession, dataset: schemas.Dataset
):
    """Test getting a dataset by audio directory."""
    retrieved_dataset = await api.datasets.get_by_audio_dir(
        session, dataset.audio_dir
    )
    assert isinstance(retrieved_dataset, schemas.Dataset)
    assert retrieved_dataset.id == dataset.id


async def test_get_dataset_by_audio_dir_fails_when_audio_dir_does_not_exist(
    session: AsyncSession,
    audio_dir: Path,
):
    """Test getting a dataset by audio_dir fails if does not exist."""
    audio_dir = audio_dir / "nonexisting_audio_dir"
    audio_dir.mkdir()
    with pytest.raises(exceptions.NotFoundError):
        await api.datasets.get_by_audio_dir(
            session,
            audio_dir=audio_dir,
        )


async def test_get_datasets(
    session: AsyncSession,
    audio_dir: Path,
    user: schemas.SimpleUser,
    random_wav_factory: Callable[..., Path],
):
    """Test getting all datasets."""
    # Arrange
    audio_dir_1 = audio_dir / "audio_1"
    audio_dir_1.mkdir()
    random_wav_factory(audio_dir_1 / "recording.wav")
    dataset1 = await api.datasets.create(
        session,
        name="test_dataset_1",
        description="This is a test dataset.",
        dataset_dir=audio_dir_1,
        audio_dir=audio_dir,
        user=user,
        visibility=models.VisibilityLevel.PUBLIC,
    )
    audio_dir_2 = audio_dir / "audio_2"
    audio_dir_2.mkdir()
    random_wav_factory(audio_dir_2 / "recording.wav")
    dataset2 = await api.datasets.create(
        session,
        name="test_dataset_2",
        description="This is a test dataset.",
        dataset_dir=audio_dir_2,
        audio_dir=audio_dir,
        user=user,
        visibility=models.VisibilityLevel.PUBLIC,
    )

    # Act
    retrieved_datasets, _ = await api.datasets.get_many(session)

    # Assert
    assert isinstance(retrieved_datasets, list)
    assert len(retrieved_datasets) == 2
    assert dataset1 in retrieved_datasets
    assert dataset2 in retrieved_datasets

    # Act (with limit)
    retrieved_datasets, _ = await api.datasets.get_many(session, limit=1)

    # Assert
    assert isinstance(retrieved_datasets, list)
    assert len(retrieved_datasets) == 1
    assert dataset2 in retrieved_datasets

    # Act (with offset)
    retrieved_datasets, _ = await api.datasets.get_many(session, offset=1)
    assert isinstance(retrieved_datasets, list)
    assert len(retrieved_datasets) == 1
    assert dataset1 in retrieved_datasets


async def test_update_dataset_name(
    session: AsyncSession,
    dataset: schemas.Dataset,
    user: schemas.SimpleUser,
):
    """Test updating a dataset's name."""
    assert dataset.name != "updated_dataset"
    updated_dataset = await api.datasets.update(
        session,
        dataset,
        data=schemas.DatasetUpdate(name="updated_dataset"),
        user=user,
    )
    assert isinstance(updated_dataset, schemas.Dataset)
    assert updated_dataset.name == "updated_dataset"


async def test_update_dataset_description(
    session: AsyncSession,
    dataset: schemas.Dataset,
    user: schemas.SimpleUser,
):
    """Test updating a dataset's description."""
    updated_dataset = await api.datasets.update(
        session,
        dataset,
        data=schemas.DatasetUpdate(
            description="This is an updated test dataset."
        ),
        user=user,
    )
    assert isinstance(updated_dataset, schemas.Dataset)
    assert updated_dataset.description == "This is an updated test dataset."


async def test_update_dataset_metadata_requires_owner(
    session: AsyncSession,
    dataset: schemas.Dataset,
    other_user: schemas.SimpleUser,
):
    """Ensure non-owners cannot change dataset metadata."""
    with pytest.raises(exceptions.PermissionDeniedError):
        await api.datasets.update(
            session,
            dataset,
            data=schemas.DatasetUpdate(name="forbidden"),
            user=other_user,
        )
    with pytest.raises(exceptions.PermissionDeniedError):
        await api.datasets.update(
            session,
            dataset,
            data=schemas.DatasetUpdate(description="forbidden"),
            user=other_user,
        )


async def test_dataset_manager_can_update_metadata(
    session: AsyncSession,
    audio_dir: Path,
    random_wav_factory: Callable[..., Path],
    user: schemas.SimpleUser,
    other_user: schemas.SimpleUser,
    group: schemas.Group,
    group_manager_membership: schemas.GroupMembership,
):
    """Ensure group managers can update restricted dataset metadata."""
    dataset_dir = audio_dir / "manager_dataset"
    dataset_dir.mkdir()
    random_wav_factory(dataset_dir / "sample.wav")

    restricted_dataset = await api.datasets.create(
        session,
        name="managed_dataset",
        description="managed dataset",
        dataset_dir=dataset_dir,
        audio_dir=audio_dir,
        user=user,
        visibility=models.VisibilityLevel.RESTRICTED,
        owner_group_id=group.id,
    )

    await api.groups.add_membership(
        session,
        group.id,
        other_user.id,
        models.GroupRole.MANAGER,
    )
    await session.commit()

    updated = await api.datasets.update(
        session,
        restricted_dataset,
        data=schemas.DatasetUpdate(name="updated_by_manager"),
        user=other_user,
    )
    assert updated.name == "updated_by_manager"


async def test_update_dataset_audio_dir(
    session: AsyncSession,
    audio_dir: Path,
    dataset: schemas.Dataset,
    user: schemas.SimpleUser,
):
    """Test updating a dataset's audio directory."""
    audio_dir_2 = audio_dir / "audio_2"
    audio_dir_2.mkdir()
    updated_dataset = await api.datasets.update(
        session,
        dataset,
        data=schemas.DatasetUpdate(audio_dir=audio_dir_2),
        audio_dir=audio_dir,
        user=user,
    )
    assert isinstance(updated_dataset, schemas.Dataset)
    assert updated_dataset.audio_dir == Path("audio_2")


async def test_delete_dataset(
    session: AsyncSession,
    dataset: schemas.Dataset,
    user: schemas.SimpleUser,
):
    """Test deleting a dataset."""
    await api.datasets.delete(session, dataset, user=user)
    with pytest.raises(exceptions.NotFoundError):
        await api.datasets.get(session, dataset.uuid)


async def test_delete_dataset_requires_owner(
    session: AsyncSession,
    dataset: schemas.Dataset,
    other_user: schemas.SimpleUser,
):
    """Ensure non-owners cannot delete datasets."""
    with pytest.raises(exceptions.PermissionDeniedError):
        await api.datasets.delete(session, dataset, user=other_user)


async def test_get_dataset_files(
    session: AsyncSession,
    dataset: schemas.Dataset,
    audio_dir: Path,
):
    """Test getting a dataset's files."""
    # Arrange
    dataset_audio_dir = audio_dir / dataset.audio_dir

    audio_file_1 = dataset_audio_dir / "audio_file_1.wav"
    audio_file_1.touch()
    audio_file_2 = dataset_audio_dir / "audio_file_2.wav"
    audio_file_2.touch()

    # Act
    retrieved_files = await api.datasets.get_state(
        session,
        dataset,
        audio_dir=audio_dir,
    )

    # Assert
    assert isinstance(retrieved_files, list)
    assert len(retrieved_files) == 3

    path_to_state = {file.path: file.state for file in retrieved_files}
    assert path_to_state[Path("initial.wav")] == schemas.FileState.REGISTERED
    assert path_to_state[Path("audio_file_1.wav")] == schemas.FileState.UNREGISTERED
    assert path_to_state[Path("audio_file_2.wav")] == schemas.FileState.UNREGISTERED


async def test_get_dataset_files_with_existing_files(
    session: AsyncSession,
    dataset: schemas.Dataset,
    random_wav_factory: Callable[..., Path],
    audio_dir: Path,
):
    """Test getting a dataset's files when some files already exist."""
    dataset_audio_dir = audio_dir / dataset.audio_dir
    path = random_wav_factory(dataset_audio_dir / "audio_file.wav")
    recording = await api.recordings.create(
        session,
        path=path,
        audio_dir=audio_dir,
    )

    await api.datasets.add_recording(
        session,
        dataset,
        recording,
    )

    retrieved_files = await api.datasets.get_state(
        session,
        dataset,
        audio_dir=audio_dir,
    )

    assert len(retrieved_files) == 2
    states = {file.path: file.state for file in retrieved_files}
    assert states[Path("initial.wav")] == schemas.FileState.REGISTERED
    assert states[Path("audio_file.wav")] == schemas.FileState.REGISTERED


async def test_get_dataset_files_with_missing_files(
    session: AsyncSession,
    dataset: schemas.Dataset,
    random_wav_factory: Callable[..., Path],
    audio_dir: Path,
):
    """Test getting a dataset's files when some files are missing."""
    # Arrange
    dataset_audio_dir = audio_dir / dataset.audio_dir
    path = random_wav_factory(dataset_audio_dir / "audio_file.wav")

    recording = await api.recordings.create(
        session,
        path=path,
        audio_dir=audio_dir,
    )

    # add the recording to the dataset
    await api.datasets.add_recording(
        session,
        dataset,
        recording,
    )

    # delete the file
    path.unlink()

    # Act
    retrieved_files = await api.datasets.get_state(
        session,
        dataset,
        audio_dir=audio_dir,
    )

    assert isinstance(retrieved_files, list)
    assert len(retrieved_files) == 2
    states = {file.path: file.state for file in retrieved_files}
    assert states[Path("initial.wav")] == schemas.FileState.REGISTERED
    assert states[Path("audio_file.wav")] == schemas.FileState.MISSING


async def test_add_recording_to_dataset(
    session: AsyncSession,
    dataset: schemas.Dataset,
    random_wav_factory: Callable[..., Path],
    audio_dir: Path,
):
    """Test adding a recording to a dataset."""
    # Arrange
    dataset_audio_dir = audio_dir / dataset.audio_dir
    audio_file = random_wav_factory(path=dataset_audio_dir / "audio_file.wav")

    recording = await api.recordings.create(
        session,
        path=audio_file,
        audio_dir=audio_dir,
    )

    # Act
    await api.datasets.add_recording(session, dataset, recording)

    # Assert
    # Make sure the recording was added to the dataset
    query = select(models.DatasetRecording).where(
        models.DatasetRecording.dataset_id == dataset.id,
        models.DatasetRecording.recording_id == recording.id,
    )
    result = await session.execute(query)
    dataset_recording = result.unique().scalar_one_or_none()
    assert dataset_recording is not None


async def test_get_dataset_recordings(
    session: AsyncSession,
    dataset: schemas.Dataset,
    random_wav_factory: Callable[..., Path],
    audio_dir: Path,
):
    """Test getting a dataset's recordings."""
    # Arrange
    dataset_audio_dir = audio_dir / dataset.audio_dir
    path_1 = random_wav_factory(
        path=dataset_audio_dir / "audio_file_1.wav",
        duration=1,
        samplerate=8000,
        channels=1,
    )
    recording_1 = await api.recordings.create(
        session,
        path=path_1,
        audio_dir=audio_dir,
    )

    path_2 = random_wav_factory(
        path=dataset_audio_dir / "audio_file_2.wav",
        duration=1,
        samplerate=8000,
        channels=1,
    )
    recording_2 = await api.recordings.create(
        session,
        path=path_2,
        audio_dir=audio_dir,
    )

    await api.datasets.add_recording(session, dataset, recording_1)
    await api.datasets.add_recording(session, dataset, recording_2)

    # Act
    retrieved_recordings, _ = await api.datasets.get_recordings(
        session, dataset
    )

    # Assert
    assert isinstance(retrieved_recordings, list)
    assert len(retrieved_recordings) == 3
    assert isinstance(retrieved_recordings[0], schemas.Recording)
    assert isinstance(retrieved_recordings[1], schemas.Recording)
    assert isinstance(retrieved_recordings[2], schemas.Recording)
    assert retrieved_recordings[0].path == recording_2.path
    assert retrieved_recordings[1].path == recording_1.path
    assert retrieved_recordings[2].path == recording_1.path.parent / "initial.wav"


async def test_add_file_to_dataset(
    session: AsyncSession,
    dataset: schemas.Dataset,
    random_wav_factory: Callable[..., Path],
    audio_dir: Path,
):
    """Test adding a file to a dataset."""
    # Arrange
    dataset_audio_dir = audio_dir / dataset.audio_dir
    path = random_wav_factory(
        path=dataset_audio_dir / "audio_file.wav",
        duration=1,
        samplerate=8000,
        channels=1,
    )

    # Act
    await api.datasets.add_file(
        session,
        dataset,
        path=path,
        audio_dir=audio_dir,
    )

    # Assert
    # Make sure the recording was created
    query = select(models.Recording).where(
        models.Recording.path == str(path.relative_to(audio_dir)),
    )
    result = await session.execute(query)
    assert result.scalars().first() is not None

    # Make sure the recording was added to the dataset
    recording_list, _ = await api.datasets.get_recordings(session, dataset)

    assert len(recording_list) == 2
    assert path.relative_to(audio_dir) in {
        recording.path for recording in recording_list
    }


async def test_add_file_to_dataset_fails_if_file_not_in_audio_dir(
    session: AsyncSession,
    dataset: schemas.Dataset,
    random_wav_factory: Callable[..., Path],
    audio_dir: Path,
):
    """Test adding a file to a dataset fails if not in audio dir."""
    # Arrange
    dataset_audio_dir = audio_dir / dataset.audio_dir
    other_dir = dataset_audio_dir.parent / "other_dir"
    other_dir.mkdir()
    path = random_wav_factory(
        path=other_dir / "audio_file.wav",
        duration=1,
        samplerate=8000,
        channels=1,
    )

    # Act
    with pytest.raises(ValueError):
        await api.datasets.add_file(
            session,
            dataset,
            path=path,
            audio_dir=audio_dir,
        )


async def test_add_file_to_dataset_with_existing_recording(
    session: AsyncSession,
    dataset: schemas.Dataset,
    random_wav_factory: Callable[..., Path],
    audio_dir: Path,
):
    """Test adding a file to a dataset that already exists in the dataset."""
    # Arrange
    dataset_audio_dir = audio_dir / dataset.audio_dir
    path = random_wav_factory(
        path=dataset_audio_dir / "audio_file.wav",
        duration=1,
        samplerate=8000,
        channels=1,
    )

    await api.recordings.create(session, path=path, audio_dir=audio_dir)

    # Act
    await api.datasets.add_file(
        session,
        dataset,
        path=path,
        audio_dir=audio_dir,
    )

    # Assert
    recording_list, _ = await api.datasets.get_recordings(session, dataset)

    assert len(recording_list) == 2
    assert path.relative_to(audio_dir) in {
        recording.path for recording in recording_list
    }


async def test_add_recordings_to_dataset(
    session: AsyncSession,
    dataset: schemas.Dataset,
    random_wav_factory: Callable[..., Path],
    audio_dir: Path,
):
    """Test adding multiple recordings to a dataset."""
    # Arrange
    dataset_audio_dir = audio_dir / dataset.audio_dir
    path_1 = random_wav_factory(
        path=dataset_audio_dir / "audio_file_1.wav",
        duration=1,
        samplerate=8000,
        channels=1,
    )
    recording_1 = await api.recordings.create(
        session,
        path=path_1,
        audio_dir=audio_dir,
    )

    path_2 = random_wav_factory(
        path=dataset_audio_dir / "audio_file_2.wav",
        duration=1,
        samplerate=8000,
        channels=1,
    )
    recording_2 = await api.recordings.create(
        session,
        path=path_2,
        audio_dir=audio_dir,
    )

    # Act
    added_paths = await api.datasets.add_recordings(
        session,
        dataset,
        [recording_1, recording_2],
    )

    # Assert
    assert len(added_paths) == 2
    assert added_paths[0].path == path_1.relative_to(dataset_audio_dir)
    assert added_paths[1].path == path_2.relative_to(dataset_audio_dir)


async def test_add_recordings_to_dataset_ignores_files_not_in_audio_dir(
    session: AsyncSession,
    dataset: schemas.Dataset,
    random_wav_factory: Callable[..., Path],
    audio_dir: Path,
):
    """Test adding recordings to a dataset ignores files not in audio dir."""
    # Arrange
    dataset_audio_dir = audio_dir / dataset.audio_dir
    other_dir = dataset_audio_dir.parent / "other_dir"
    other_dir.mkdir()

    path_1 = random_wav_factory(path=dataset_audio_dir / "audio_file_1.wav")
    recording_1 = await api.recordings.create(
        session,
        path=path_1,
        audio_dir=audio_dir,
    )

    path_2 = random_wav_factory(path=other_dir / "audio_file_2.wav")
    recording_2 = await api.recordings.create(
        session,
        path=path_2,
        audio_dir=audio_dir,
    )

    # Act
    added_paths = await api.datasets.add_recordings(
        session,
        dataset,
        [recording_1, recording_2],
    )

    # Assert
    assert len(added_paths) == 1
    assert added_paths[0].path == path_1.relative_to(dataset_audio_dir)


async def test_add_recordings_to_dataset_ignores_duplicate_recordings(
    session: AsyncSession,
    dataset: schemas.Dataset,
    random_wav_factory: Callable[..., Path],
    audio_dir: Path,
):
    """Test adding recordings to a dataset ignores duplicate recordings."""
    # Arrange
    dataset_audio_dir = audio_dir / dataset.audio_dir
    path_1 = random_wav_factory(
        path=dataset_audio_dir / "audio_file_1.wav",
        duration=1,
        samplerate=8000,
        channels=1,
    )
    recording_1 = await api.recordings.create(
        session,
        path=path_1,
        audio_dir=audio_dir,
    )

    path_2 = random_wav_factory(
        path=dataset_audio_dir / "audio_file_2.wav",
        duration=1,
        samplerate=8000,
        channels=1,
    )
    recording_2 = await api.recordings.create(
        session,
        path=path_2,
        audio_dir=audio_dir,
    )

    # Act
    added_paths = await api.datasets.add_recordings(
        session,
        dataset,
        [recording_1, recording_2, recording_1],
    )

    # Assert
    assert len(added_paths) == 2
    assert added_paths[0].path == path_1.relative_to(dataset_audio_dir)
    assert added_paths[1].path == path_2.relative_to(dataset_audio_dir)


async def test_add_recordings_to_dataset_ignores_recordings_already_in_dataset(
    session: AsyncSession,
    dataset: schemas.Dataset,
    random_wav_factory: Callable[..., Path],
    audio_dir: Path,
):
    """Test adding multiple recordings ignores already in dataset."""
    # Arrange
    dataset_audio_dir = audio_dir / dataset.audio_dir
    path_1 = random_wav_factory(
        path=dataset_audio_dir / "audio_file_1.wav",
        duration=1,
        samplerate=8000,
        channels=1,
    )
    recording_1 = await api.recordings.create(
        session,
        path=path_1,
        audio_dir=audio_dir,
    )

    path_2 = random_wav_factory(
        path=dataset_audio_dir / "audio_file_2.wav",
        duration=1,
        samplerate=8000,
        channels=1,
    )
    recording_2 = await api.recordings.create(
        session,
        path=path_2,
        audio_dir=audio_dir,
    )

    await api.datasets.add_recording(
        session,
        dataset,
        recording_2,
    )

    # Act
    added_paths = await api.datasets.add_recordings(
        session,
        dataset,
        [recording_1, recording_2],
    )

    # Assert
    assert len(added_paths) == 1
    assert added_paths[0].path == path_1.relative_to(dataset_audio_dir)


async def test_create_dataset_registers_all_recordings(
    session: AsyncSession,
    random_wav_factory: Callable[..., Path],
    audio_dir: Path,
    user: schemas.SimpleUser,
):
    """Test creating dataset registers all recordings in the directory."""
    dataset_audio_dir = audio_dir / "audio"

    if dataset_audio_dir.exists():
        dataset_audio_dir.rmdir()

    dataset_audio_dir.mkdir()
    audio_file_1 = random_wav_factory(
        path=dataset_audio_dir / "audio_file_1.wav"
    )

    subdirectory = dataset_audio_dir / "subdirectory"
    subdirectory.mkdir()

    audio_file_2 = random_wav_factory(path=subdirectory / "audio_file_2.wav")

    text_file = dataset_audio_dir / "text_file.txt"
    text_file.touch()

    # Act
    dataset = await api.datasets.create(
        session,
        name="test_dataset",
        description="This is a test dataset.",
        dataset_dir=dataset_audio_dir,
        audio_dir=audio_dir,
        user=user,
        visibility=models.VisibilityLevel.PUBLIC,
    )

    # Assert
    assert isinstance(dataset, schemas.Dataset)
    assert dataset.audio_dir == Path("audio")
    assert dataset.name == "test_dataset"
    assert dataset.description == "This is a test dataset."

    dataset_recordings, _ = await api.datasets.get_recordings(session, dataset)
    assert len(dataset_recordings) == 2
    assert {rec.path for rec in dataset_recordings} == {
        audio_file_1.relative_to(audio_dir),
        audio_file_2.relative_to(audio_dir),
    }

    all_recordings, _ = await api.recordings.get_many(session)
    assert len(all_recordings) == 2


async def test_exported_datasets_paths_are_not_absolute(
    session: AsyncSession,
    example_data_dir: Path,
):
    example_dataset = example_data_dir / "example_dataset.json"
    assert example_dataset.is_file()

    audio_dir = example_data_dir / "audio"
    assert audio_dir.is_dir()

    whombat_dataset = await api.datasets.import_dataset(
        session,
        example_dataset,
        dataset_audio_dir=audio_dir,
        audio_dir=example_data_dir,
    )
    exported = await api.datasets.export_dataset(session, whombat_dataset)

    for recording in exported.data.recordings or []:
        # Check that paths are not absolute (full paths)
        assert not recording.path.is_absolute()

        # Check that paths were exported relative to the dataset audio_dir
        assert (audio_dir / recording.path).is_file()


async def test_recording_is_deleted_if_it_does_not_belong_to_a_dataset(
    session: AsyncSession,
    dataset: schemas.Dataset,
    dataset_recording: schemas.Recording,
    user: schemas.SimpleUser,
):
    await api.recordings.get(session, dataset_recording.uuid)

    await api.datasets.delete(session, dataset, user=user)

    with pytest.raises(exceptions.NotFoundError):
        await api.recordings.get(session, dataset_recording.uuid)


async def test_recordings_belonging_to_multiple_datastes_are_not_deleted(
    session: AsyncSession,
    dataset_recording: schemas.Recording,
    audio_dir: Path,
    dataset_dir: Path,
    user: schemas.SimpleUser,
):
    await api.recordings.get(session, dataset_recording.uuid)

    dataset2 = await api.datasets.create(
        session,
        name="other_dataset",
        description="other dataset",
        dataset_dir=dataset_dir,
        audio_dir=audio_dir,
        user=user,
        visibility=models.VisibilityLevel.PUBLIC,
    )

    await api.datasets.add_recording(session, dataset2, dataset_recording)

    await api.recordings.get(session, dataset_recording.uuid)


async def test_list_candidates_excludes_registered_directories(
    session: AsyncSession,
    audio_dir: Path,
    user: schemas.SimpleUser,
    random_wav_factory: Callable[..., Path],
):
    """Only unregistered top-level directories should be returned."""
    candidate_a = audio_dir / "candidate_a"
    candidate_b = audio_dir / "candidate_b"
    registered = audio_dir / "registered"

    candidate_a.mkdir()
    candidate_b.mkdir()
    registered.mkdir()

    random_wav_factory(candidate_a / "a.wav")
    random_wav_factory(candidate_b / "b.wav")
    nested_registered = registered / "nested"
    nested_registered.mkdir()
    random_wav_factory(nested_registered / "r.wav")

    await api.datasets.create(
        session,
        name="registered",
        description="already registered",
        dataset_dir=nested_registered,
        audio_dir=audio_dir,
        user=user,
        visibility=models.VisibilityLevel.PUBLIC,
    )

    candidates = await api.datasets.list_candidates(session, audio_dir=audio_dir)
    candidate_paths = {candidate.relative_path for candidate in candidates}

    assert candidate_paths == {Path("candidate_a"), Path("candidate_b")}
    assert all(candidate.absolute_path.is_absolute() for candidate in candidates)


async def test_inspect_candidate_reports_nested_directories(
    audio_dir: Path,
    random_wav_factory: Callable[..., Path],
    session: AsyncSession,
):
    """Inspecting a candidate should identify nested folders and audio count."""
    candidate = audio_dir / "inspect_me"
    candidate.mkdir()
    nested = candidate / "nested"
    nested.mkdir()

    random_wav_factory(candidate / "top.wav")
    random_wav_factory(nested / "inner.wav")

    info = await api.datasets.inspect_candidate(
        directory=candidate,
        audio_dir=audio_dir,
    )

    assert info.relative_path == Path("inspect_me")
    assert info.absolute_path == candidate
    assert info.has_nested_directories is True
    assert info.audio_file_count == 2
