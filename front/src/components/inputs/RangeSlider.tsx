import { useRef } from "react";
import { useSliderState } from "react-stately";
import {
  useNumberFormatter,
  useSlider,
  VisuallyHidden,
  type AriaSliderProps,
} from "react-aria";
import { Thumb } from './Slider';


export default function RangeSlider({
  formatter,
  ...props
}: AriaSliderProps & {
  formatter?: (value: number) => string;
}) {
  const trackRef = useRef<HTMLDivElement | null>(null);
  const numberFormatter = useNumberFormatter({ style: "decimal" });
  const state = useSliderState({ ...props, numberFormatter });
  const { groupProps, trackProps, labelProps, outputProps } = useSlider(
    props,
    state,
    trackRef,
  );
  return (
    <div {...groupProps} className="ml-2 w-full pe-2">
      {props.label && (
        <div className="flex justify-between text-xs text-stone-600 dark:text-stone-400">
          <VisuallyHidden>
            <label {...labelProps}>{props.label}</label>
          </VisuallyHidden>
          <output {...outputProps}>
            {formatter
              ? formatter(state.getThumbValue(0))
              : state.getThumbValueLabel(0)}
          </output>
          <output {...outputProps}>
            {formatter
              ? formatter(state.getThumbValue(1))
              : state.getThumbValueLabel(1)}
          </output>
        </div>
      )}
      <div
        className="py-1 w-full cursor-pointer"
        {...trackProps}
        ref={trackRef}
      >
        <div className="w-full h-1 rounded-full bg-stone-900">
          <span
            className="absolute h-1 bg-emerald-600 rounded-full dark:bg-emerald-200"
            style={{
              left: `${state.getThumbPercent(0) * 100}%`,
              right: `${(1 - state.getThumbPercent(1)) * 100}%`,
            }}
          ></span>
          <Thumb
            index={0}
            state={state}
            trackRef={trackRef}
            name={"currentTime"}
          />
          <Thumb
            index={1}
            state={state}
            trackRef={trackRef}
            name={"currentTime"}
          />
        </div>
      </div>
    </div>
  );
}
