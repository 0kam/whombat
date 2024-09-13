import { useCallback } from "react";
import toast from "react-hot-toast";

import api from "@/app/api";
import useObject from "@/lib/hooks/utils/useObject";

import type { AxiosError } from "axios";
import type { RecordingUpdate } from "@/lib/api/recordings";
import type { NoteCreate } from "@/lib/api/notes";
import type { Recording, Tag, Note, Feature } from "@/lib/types";

export default function useRecording({
  uuid,
  recording,
  enabled = true,
  onUpdateRecording,
  onDeleteRecording,
  onAddRecordingTag,
  onDeleteRecordingTag,
  onAddRecordingNote,
  onDeleteRecordingNote,
  onAddRecordingFeature,
  onDeleteRecordingFeature,
  onUpdateRecordingFeature,
  onError,
}: {
  uuid: string;
  recording?: Recording;
  enabled?: boolean;
  onUpdateRecording?: (recording: Recording) => void;
  onDeleteRecording?: (recording: Recording) => void;
  onAddRecordingTag?: (recording: Recording, tag: Tag) => void;
  onDeleteRecordingTag?: (recording: Recording, tag: Tag) => void;
  onAddRecordingNote?: (recording: Recording, note: NoteCreate) => void;
  onDeleteRecordingNote?: (recording: Recording, note: Note) => void;
  onAddRecordingFeature?: (recording: Recording, feature: Feature) => void;
  onDeleteRecordingFeature?: (recording: Recording, feature: Feature) => void;
  onUpdateRecordingFeature?: (recording: Recording, feature: Feature) => void;
  onError?: (error: AxiosError) => void;
}) {
  if (recording !== undefined && recording.uuid !== uuid) {
    throw new Error("Recording uuid does not match");
  }

  const { query, useMutation, useDestruction } = useObject<Recording>({
    id: uuid,
    initialData: recording,
    name: "recording",
    enabled,
    queryFn: api.recordings.get,
    onError,
  });

  const update = useMutation<RecordingUpdate>({
    mutationFn: api.recordings.update,
    onSuccess: (data) => {
      toast.success("Recording updated");
      onUpdateRecording?.(data);
    },
  });

  const addTag = useMutation({
    mutationFn: api.recordings.addTag,
    onSuccess: (data, tag) => {
      toast.success("Tag added");
      onAddRecordingTag?.(data, tag);
    },
  });

  const removeTag = useMutation({
    mutationFn: api.recordings.removeTag,
    onSuccess: (data, tag) => {
      toast.success("Tag removed");
      onDeleteRecordingTag?.(data, tag);
    },
  });

  const addNote = useMutation({
    mutationFn: api.recordings.addNote,
    onSuccess: (data, note) => {
      toast.success("Note added");
      onAddRecordingNote?.(data, note);
    },
  });

  const removeNote = useMutation({
    mutationFn: api.recordings.removeNote,
    onSuccess: (data, note) => {
      toast.success("Note removed");
      onDeleteRecordingNote?.(data, note);
    },
  });

  const addFeature = useMutation({
    mutationFn: api.recordings.addFeature,
    onSuccess: (data, feature) => {
      toast.success("Feature added");
      onAddRecordingFeature?.(data, feature);
    },
  });

  const updateFeature = useMutation({
    mutationFn: api.recordings.updateFeature,
    onSuccess: (data, feature) => {
      toast.success("Feature updated");
      onUpdateRecordingFeature?.(data, feature);
    },
  });

  const removeFeature = useMutation({
    mutationFn: api.recordings.removeFeature,
    onSuccess: (data, feature) => {
      toast.success("Feature removed");
      onDeleteRecordingFeature?.(data, feature);
    },
  });

  const download = useCallback(() => {
    api.recordings.download(uuid);
  }, [uuid]);

  const delete_ = useDestruction({
    mutationFn: api.recordings.delete,
    onSuccess: (data) => {
      toast.success("Recording deleted");
      onDeleteRecording?.(data);
    },
  });

  return {
    ...query,
    update,
    addTag,
    removeTag,
    addNote,
    removeNote,
    addFeature,
    updateFeature,
    removeFeature,
    download,
    delete: delete_,
  };
}
