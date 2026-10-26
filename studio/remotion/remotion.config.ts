import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
Config.setCodec("h264");
Config.setChromiumDisableWebSecurity(true);
if (process.argv.includes("preview")) {
  const remotionPort = parseInt(process.env.PORT || process.env.REMOTION_PORT || "3100", 10);
  Config.setPort(remotionPort);
}
