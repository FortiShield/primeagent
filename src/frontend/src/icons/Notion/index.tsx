import type React from "react";
import { forwardRef } from "react";
import SvgnotionLogo from "./notionLogo";

export const notionIcon = forwardRef<
  SVGSVGElement,
  React.PropsWithChildren<{}>
>((props, ref) => {
  return (
    <span
      style={{
        display: "inline-grid",
        width: 22,
        height: 22,
        placeItems: "center",
        flexShrink: 0,
      }}
    >
      <SvgnotionLogo ref={ref} {...props} />
    </span>
  );
});
