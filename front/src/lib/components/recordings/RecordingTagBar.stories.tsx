import type { Meta, StoryObj } from "@storybook/react";
import { fn } from "@storybook/test";

import RecordingTagBar from "@/lib/components/recordings/RecordingTagBar";
import TagSearchBar, {
  type TagSearchBarProps,
} from "@/lib/components/tags/TagSearchBar";

const meta: Meta<typeof RecordingTagBar> = {
  title: "Recordings/TagBar",
  component: RecordingTagBar,
};

export default meta;

type Story = StoryObj<typeof RecordingTagBar>;

const tags = [
  { key: "tag1", value: "value1", canonical_name: "value1" },
  { key: "tag2", value: "value2", canonical_name: "value2" },
  { key: "tag3", value: "value3", canonical_name: "value3" },
  { key: "tag4", value: "value4", canonical_name: "value4" },
  { key: "tag1", value: "value5", canonical_name: "value5" },
  { key: "tag1", value: "value6", canonical_name: "value6" },
  { key: "tag1", value: "value7", canonical_name: "value7" },
];

const props = {
  onSelectTag: fn(),
  onCreateTag: fn(),
  onClickTag: fn(),
  onDeleteTag: fn(),
  TagSearchBar: (props: TagSearchBarProps) => (
    <TagSearchBar tags={tags} {...props} />
  ),
};

export const Primary: Story = {
  args: {
    tags: [{ key: "tag1", value: "value1", canonical_name: "value1" }],
    ...props,
  },
};

export const NoTags: Story = {
  args: {
    tags: [],
    ...props,
  },
};

export const ManyTags: Story = {
  args: {
    tags: [
      { key: "tag1", value: "value1", canonical_name: "value1" },
      { key: "tag2", value: "value2", canonical_name: "value2" },
      { key: "tag3", value: "value3", canonical_name: "value3" },
      { key: "tag4", value: "value4", canonical_name: "value4" },
      { key: "tag1", value: "value5", canonical_name: "value5" },
      { key: "tag1", value: "value6", canonical_name: "value6" },
      { key: "tag1", value: "value7", canonical_name: "value7" },
    ],
    ...props,
  },
};
