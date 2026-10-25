export interface WordTiming {
  word: string;
  start_ms: number;
  end_ms: number;
}

export interface SequenceItem {
  id: string; // e.g. "S001-A"
  scene: string; // e.g. "S001"
  beat: string;
  type: "AIV" | "IMG" | "GFX";
  duration_seconds: number;
  duration_frames: number;
  start_frame: number;
  asset_path?: string;
  fallback_asset?: string;
  motion_effect?: "ken_burns_zoom_in" | "ken_burns_zoom_out" | "ken_burns_pan_left" | "ken_burns_pan_right" | "static";
  gfx_component?: "ChartMotion" | "CounterNumber" | "CoinPhysics3D" | "Custom";
  gfx_props?: Record<string, any>;
  narration_text?: string;
  narration_audio_url?: string;
  words?: WordTiming[];
}

export interface VideoCompositionProps {
  title: string;
  slug: string;
  channel: string;
  fps: number;
  width: number;
  height: number;
  total_duration_seconds: number;
  total_frames: number;
  bgm_url?: string;
  bgm_volume?: number;
  bgm_duration_seconds?: number;
  bgm_duration_frames?: number;
  master_audio_url?: string;
  sequences: SequenceItem[];
}
