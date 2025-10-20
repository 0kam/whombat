import { z } from "zod";

import * as schemas from "@/lib/schemas";

export type Tag = z.infer<typeof schemas.TagSchema>;

export type TagCount = z.infer<typeof schemas.TagCountSchema>;

export type TagFilter = z.infer<typeof schemas.TagFilterSchema>;

export type TagCreate = Pick<Tag, "key" | "value" | "canonical_name">;

export type AnnotationTag = z.infer<typeof schemas.TagAssociationSchema>;

export type PredictionTag = z.infer<typeof schemas.PredictionTagSchema>;
