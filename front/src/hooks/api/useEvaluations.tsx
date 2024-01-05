import { useMutation } from "@tanstack/react-query";

import { type EvaluationFilter } from "@/api/evaluations";
import api from "@/app/api";
import useFilter from "@/hooks/utils/useFilter";
import usePagedQuery from "@/hooks/utils/usePagedQuery";

const _empty: EvaluationFilter = {};
const _fixed: (keyof EvaluationFilter)[] = [];

export default function useEvaluations({
  filter: initialFilter = _empty,
  fixed = _fixed,
  pageSize = 10,
  enabled = true,
}: {
  filter?: EvaluationFilter;
  fixed?: (keyof EvaluationFilter)[];
  pageSize?: number;
  enabled?: boolean;
} = {}) {
  const filter = useFilter<EvaluationFilter>({
    defaults: initialFilter,
    fixed,
  });

  const { query, pagination, items, total } = usePagedQuery({
    name: "evaluations",
    queryFn: api.evaluations.getMany,
    pageSize: pageSize,
    filter: filter.filter,
    enabled,
  });

  const create = useMutation({
    mutationFn: api.evaluations.create,
    onSuccess: () => {
      query.refetch();
    },
  });

  return {
    ...query,
    filter,
    pagination,
    items,
    total,
    create,
  } as const;
}
