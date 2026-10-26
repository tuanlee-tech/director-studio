import React from "react";
import { interpolate, useCurrentFrame, Img } from "remotion";

interface KenBurnsImageProps {
  src: string;
  durationInFrames: number;
  effect?: "ken_burns_zoom_in" | "ken_burns_zoom_out" | "ken_burns_pan_left" | "ken_burns_pan_right" | "static";
  alt?: string;
}

export const KenBurnsImage: React.FC<KenBurnsImageProps> = ({
  src,
  durationInFrames,
  effect = "ken_burns_zoom_in",
  alt = "Ken Burns Image",
}) => {
  const frame = useCurrentFrame();

  let scale = 1.0;
  let translateX = 0;
  let translateY = 0;

  if (effect === "ken_burns_zoom_in") {
    scale = interpolate(frame, [0, durationInFrames], [1.0, 1.08], {
      extrapolateRight: "clamp",
    });
  } else if (effect === "ken_burns_zoom_out") {
    scale = interpolate(frame, [0, durationInFrames], [1.08, 1.0], {
      extrapolateRight: "clamp",
    });
  } else if (effect === "ken_burns_pan_left") {
    scale = 1.05;
    translateX = interpolate(frame, [0, durationInFrames], [2, -2], {
      extrapolateRight: "clamp",
    });
  } else if (effect === "ken_burns_pan_right") {
    scale = 1.05;
    translateX = interpolate(frame, [0, durationInFrames], [-2, 2], {
      extrapolateRight: "clamp",
    });
  }

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
        height: "100%",
        overflow: "hidden",
        backgroundColor: "#0b0f19",
      }}
    >
      <Img
        src={src}
        alt={alt}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translate(${translateX}%, ${translateY}%)`,
          transformOrigin: "center center",
        }}
      />
      {/* Cinematic Vignette Overlay */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          background: "radial-gradient(circle, transparent 65%, rgba(0, 0, 0, 0.45) 100%)",
          pointerEvents: "none",
        }}
      />
    </div>
  );
};
