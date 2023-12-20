import React from "react";

import { type User, type Note } from "@/api/schemas";
import NoteComponent from "@/components/Note";

export default function Feed({
  notes,
  currentUser,
  onUpdate,
  onDelete,
}: {
  notes: Note[];
  currentUser?: User;
  onUpdate?: (note: Note) => void;
  onDelete?: (note: Note) => void;
}) {
  return (
    <ul
      aria-label="feed"
      role="feed"
      className="flex relative flex-col gap-12 py-12 pl-6 before:absolute before:top-0 before:left-6 before:h-full before:-translate-x-1/2 before:border before:border-dashed before:border-stone-200 before:dark:border-stone-700 after:absolute after:top-6 after:left-6 after:bottom-6 after:-translate-x-1/2 after:border after:border-stone-200 after:dark:border-stone-700"
    >
      {notes.map((note) => (
        <NoteComponent
          key={note.uuid}
          note={note}
          currentUser={currentUser}
          onUpdate={onUpdate}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
}
