import { AxiosInstance } from "axios";

import { GetMany, Page } from "@/lib/api/common";
import * as schemas from "@/lib/schemas";
import * as types from "@/lib/types";

const DEFAULT_ENDPOINTS = {
  get: "/api/v1/tags/",
  getRecordingTags: "/api/v1/tags/recording_tags/",
  getClipAnnotationTags: "/api/v1/tags/clip_annotation_tags/",
  getSoundEventAnnotationTags: "/api/v1/tags/sound_event_annotation_tags/",
  getRecordingCounts: "/api/v1/tags/recording_counts/",
  getClipAnnotationCounts: "/api/v1/tags/clip_annotation_counts/",
  getSoundEventAnnotationCounts: "/api/v1/tags/sound_event_annotation_counts/",
  create: "/api/v1/tags/",
};

export function registerTagAPI(
  instance: AxiosInstance,
  endpoints: typeof DEFAULT_ENDPOINTS = DEFAULT_ENDPOINTS,
) {
  async function getTags(
    query: types.GetMany & types.TagFilter,
  ): Promise<types.Page<types.Tag>> {
    const params = GetMany(schemas.TagFilterSchema).parse(query);
    const response = await instance.get(endpoints.get, {
      params: {
        limit: params.limit,
        offset: params.offset,
        sort_by: params.sort_by,
        search: params.search,
        key__eq: params.key,
        value__eq: params.value?.eq,
        value__has: params.value?.has,
        annotation_project__eq: params.annotation_project?.uuid,
        recording__eq: params.recording?.uuid,
        sound_event_annotation__eq: params.sound_event_annotation?.uuid,
        clip_annotation__eq: params.clip_annotation?.uuid,
        sound_event_prediction__eq: params.sound_event_prediction?.uuid,
        clip_prediction__eq: params.clip_prediction?.uuid,
        evaluation_set__eq: params.evaluation_set?.uuid,
        dataset__eq: params.dataset?.uuid,
      },
    });
    return Page(schemas.TagSchema).parse(response.data);
  }

  async function getRecordingTags(
    query: types.GetMany & types.RecordingTagFilter,
  ): Promise<types.Page<types.RecordingTag>> {
    const params = GetMany(schemas.RecordingTagFilterSchema).parse(query);
    const response = await instance.get(endpoints.getRecordingTags, {
      params: {
        limit: params.limit,
        offset: params.offset,
        sort_by: params.sort_by,
        recording__eq: params.recording?.uuid,
        dataset__eq: params.dataset?.uuid,
        tag__key: params.tag?.key,
        tag__value: params.tag?.value,
        issue__eq: params.issue,
      },
    });
    return Page(schemas.RecordingTagSchema).parse(response.data);
  }

  async function getRecordingCounts(
    query: types.GetMany & types.RecordingTagFilter,
  ): Promise<types.Page<types.TagCount>> {
    const params = GetMany(schemas.RecordingTagFilterSchema).parse(query);
    const response = await instance.get(endpoints.getRecordingCounts, {
      params: {
        limit: params.limit,
        offset: params.offset,
        sort_by: params.sort_by,
        recording__eq: params.recording?.uuid,
        dataset__eq: params.dataset?.uuid,
        tag__key: params.tag?.key,
        tag__value: params.tag?.value,
        issue__eq: params.issue,
      },
    });
    return Page(schemas.TagCountSchema).parse(response.data);
  }

  async function getClipAnnotationTags(
    query: types.GetMany & types.ClipAnnotationTagFilter,
  ): Promise<types.Page<types.ClipAnnotationTag>> {
    const params = GetMany(schemas.ClipAnnotationTagFilterSchema).parse(query);
    const response = await instance.get(endpoints.getClipAnnotationTags, {
      params: {
        limit: params.limit,
        offset: params.offset,
        sort_by: params.sort_by,
        annotation_project__eq: params.annotation_project?.uuid,
        evaluation_set__eq: params.evaluation_set?.uuid,
      },
    });
    return Page(schemas.ClipAnnotationTagSchema).parse(response.data);
  }

  async function getClipAnnotationCounts(
    query: types.GetMany & types.ClipAnnotationTagFilter,
  ): Promise<types.Page<types.TagCount>> {
    const params = GetMany(schemas.ClipAnnotationTagFilterSchema).parse(query);
    const response = await instance.get(endpoints.getClipAnnotationCounts, {
      params: {
        limit: params.limit,
        offset: params.offset,
        sort_by: params.sort_by,
        annotation_project__eq: params.annotation_project?.uuid,
        evaluation_set__eq: params.evaluation_set?.uuid,
      },
    });
    return Page(schemas.TagCountSchema).parse(response.data);
  }

  async function getSoundEventTags(
    query: types.GetMany & types.SoundEventAnnotationTagFilter,
  ): Promise<types.Page<types.SoundEventAnnotationTag>> {
    const params = GetMany(schemas.SoundEventAnnotationTagFilterSchema).parse(
      query,
    );
    const response = await instance.get(endpoints.getSoundEventAnnotationTags, {
      params: {
        limit: params.limit,
        offset: params.offset,
        sort_by: params.sort_by,
        annotation_project__eq: params.annotation_project?.uuid,
        evaluation_set__eq: params.evaluation_set?.uuid,
      },
    });
    return Page(schemas.SoundEventAnnotationTagSchema).parse(response.data);
  }

  async function getSoundEventAnnotationCounts(
    query: types.GetMany & types.SoundEventAnnotationTagFilter,
  ): Promise<types.Page<types.TagCount>> {
    const params = GetMany(schemas.SoundEventAnnotationTagFilterSchema).parse(
      query,
    );
    const response = await instance.get(
      endpoints.getSoundEventAnnotationCounts,
      {
        params: {
          limit: params.limit,
          offset: params.offset,
          sort_by: params.sort_by,
          annotation_project__eq: params.annotation_project?.uuid,
          evaluation_set__eq: params.evaluation_set?.uuid,
        },
      },
    );
    return Page(schemas.TagCountSchema).parse(response.data);
  }

  async function createTag(data: types.TagCreate): Promise<types.Tag> {
    const payload = {
      key: data.key,
      value: data.value,
      canonical_name: data.canonical_name,
    };
    const response = await instance.post(endpoints.create, payload);
    return schemas.TagSchema.parse(response.data);
  }

  return {
    get: getTags,
    create: createTag,
    getRecordingTags,
    getClipAnnotationTags,
    getSoundEventTags,
    getRecordingCounts,
    getClipAnnotationCounts,
    getSoundEventAnnotationCounts,
  } as const;
}
