import type { NoteCreate } from "@/lib/api/notes";
import { IssueIcon, NotesIcon } from "@/lib/components/icons";
import { InputGroup, TextArea } from "@/lib/components/inputs/index";
import Button from "@/lib/components/ui/Button";
import { useState } from "react";

export default function CreateNoteForm({
  onCreateNote,
}: {
  onCreateNote?: (note: NoteCreate) => void;
}) {
  const [message, setMessage] = useState("");

  return (
    <div className="flex flex-col p-4 w-full">
      <InputGroup
        label="Add a note"
        name="message"
        help="Write the note message and click on the type of note you want to create."
      >
        <TextArea
          name="message"
          value={message}
          placeholder="Type your note here..."
          onChange={(e) => setMessage(e.target.value)}
        />
      </InputGroup>
      <div className="flex flex-row gap-4 justify-end">
        <Button
          variant="danger"
          mode="text"
          onClick={() => {
            onCreateNote?.({
              message,
              is_issue: true,
            });
            setMessage("");
          }}
        >
          <IssueIcon className="inline-block mr-1 w-5 h-5" />
          Add Issue
        </Button>
        <Button
          variant="primary"
          mode="text"
          onClick={() => {
            onCreateNote?.({
              message,
              is_issue: false,
            });
            setMessage("");
          }}
        >
          <NotesIcon className="inline-block mr-1 w-5 h-5" />
          Add Note
        </Button>
      </div>
    </div>
  );
}
