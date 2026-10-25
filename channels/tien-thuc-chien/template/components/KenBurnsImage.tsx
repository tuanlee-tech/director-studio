import React from "react";
import { Img, interpolate, useCurrentFrame } from "remotion";

interface KenBurnsImageProps {
  src: string;
  durationInFrames: number;
  effect?: "ken_burns_zoom_in" | "ken_burns_zoom_out" | "ken_burns_pan_left" | "ken_burns_pan_right" | "static";
}

export const KenBurnsImage: React.FC<KenBurnsImageProps> = ({
  src,
  durationInFrames,
  effect = "ken_burns_zoom_in",
}) => {
  const frame = useCurrentFrame();

  let scale = 1.0;
  let translateX = 0;
  let translateY = 0;

  if (effect === "ken_burns_zoom_in") {
    scale = interpolate(frame, [0, durationInFrames], [1.0, 1.15], {
      extrapolateRight: "clamp",
    });
  } else if (effect === "ken_burns_zoom_out") {
    scale = interpolate(frame, [0, durationInFrames], [1.15, 1.0], {
      extrapolateRight: "clamp",
    });
  } else if (effect === "ken_burns_pan_left") {
    scale = 1.1;
    translateX = interpolate(frame, [0, durationInFrames], [0, -30], {
      extrapolateRight: "clamp",
    });
  } else if (effect === "ken_burns_pan_right") {
    scale = 1.1;
    translateX = interpolate(frame, [0, durationInFrames], [-30, 0], {
      extrapolateRight: "clamp",
    });
  }

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        overflow: "hidden",
        position: "relative",
      }}
    >
      <Img
        src={src}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
          transformOrigin: "center center",
        }}
      />
    </div>
  );
};
