"use client";

import dynamic from "next/dynamic";
import { useMemo, useState } from "react";

import Pagination from "@/app/components/Pagination";
import RecordingSpectrogram from "@/app/components/recordings/RecordingSpectrogram";

import useRecordings from "@/app/hooks/api/useRecordings";

import ExplorationLayout from "@/lib/components/layouts/Exploration";
import ListCounts from "@/lib/components/lists/ListCounts";
import RecordingItem from "@/lib/components/recordings/RecordingItem";
import Empty from "@/lib/components/ui/Empty";

import type { Recording, RecordingFilter } from "@/lib/types";

const RecordingMap = dynamic(
  () => import("@/lib/components/exploration/RecordingMap"),
  { ssr: false },
);

export default function Page() {
  const [selectedRecording, setSelectedRecording] = useState<Recording | null>(
    null,
  );

  const initialFilter: RecordingFilter = useMemo(
    () => ({
      latitude: { is_null: false },
      longitude: { is_null: false },
    }),
    [],
  );

  const {
    items: recordings,
    total,
    pagination,
    isLoading,
  } = useRecordings({
    pageSize: 500,
    filter: initialFilter,
  });

  return (
    <ExplorationLayout
      isLoading={isLoading}
      Pagination={
        <Pagination
          pagination={pagination}
          pageSizeOptions={[100, 200, 500, 1000, 2000, 5000, -1]}
        />
      }
      Counts={
        <ListCounts
          total={total}
          startIndex={pagination.page * pagination.pageSize}
          endIndex={(pagination.page + 1) * pagination.pageSize}
        />
      }
    >
      <div className="grid grid-cols-2 gap-4">
        <RecordingMap
          recordings={recordings}
          onClickRecording={setSelectedRecording}
        />
        <div className="col-start-2 h-full grow">
          {selectedRecording == null ? (
            <Empty outerClassName="h-full" className="h-full grow">
              Select a Recording by clicking on the map.
            </Empty>
          ) : (
            <RecordingItem
              recording={selectedRecording}
              SpectrogramRecording={RecordingSpectrogram}
              height={400}
            />
          )}
        </div>
      </div>
    </ExplorationLayout>
  );
}
