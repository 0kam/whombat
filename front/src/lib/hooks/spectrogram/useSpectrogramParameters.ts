import { useMemo } from "react";

import type {
  AudioSettings,
  SpectrogramParameters,
  SpectrogramSettings,
} from "@/lib/types";

export default function useSpectrogramParameters({
  audioSettings,
  spectrogramSettings,
}: {
  audioSettings: AudioSettings;
  spectrogramSettings: SpectrogramSettings;
}): SpectrogramParameters {
  const { channel, resample, samplerate, low_freq, high_freq, filter_order } =
    audioSettings;
  const {
    window_size,
    overlap,
    window,
    scale,
    cmap,
    min_dB,
    max_dB,
    normalize,
    pcen,
    clamp,
    time_scale,
    freq_scale,
  } = spectrogramSettings;

  return useMemo(
    () => ({
      channel,
      resample,
      samplerate,
      low_freq,
      high_freq,
      filter_order,
      window_size,
      overlap,
      window,
      scale,
      cmap,
      min_dB,
      max_dB,
      normalize,
      pcen,
      clamp,
      time_scale,
      freq_scale,
    }),
    [
      channel,
      resample,
      samplerate,
      low_freq,
      high_freq,
      filter_order,
      window_size,
      overlap,
      window,
      scale,
      cmap,
      min_dB,
      max_dB,
      normalize,
      pcen,
      clamp,
      time_scale,
      freq_scale,
    ],
  );
}
