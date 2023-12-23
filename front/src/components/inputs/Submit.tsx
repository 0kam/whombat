import classNames from "classnames";
import type { InputHTMLAttributes, ReactNode } from "react";
import {
  COMMON_STYLE,
  BORDER_STYLE,
  BACKGROUND_STYLE,
  TEXT_STYLE,
  FOCUS_STYLE,
  DISABLED_STYLE,
} from "./styles";

export default function Submit({
  children,
  className,
  ...props
}: {
  children: ReactNode;
} & Omit<InputHTMLAttributes<HTMLButtonElement>, "type">) {
  return (
    <>
      <button
        type="submit"
        className={classNames(
          COMMON_STYLE,
          BORDER_STYLE,
          BACKGROUND_STYLE,
          TEXT_STYLE,
          FOCUS_STYLE,
          DISABLED_STYLE,
          className,
          "relative",
        )}
        {...props}
      >
        {children}
      </button>
    </>
  );
}
