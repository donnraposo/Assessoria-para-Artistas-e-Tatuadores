import { iconGlyphs } from "./iconGlyphs";
import type { IconName } from "./iconName";

type IconProps = {
  name: IconName;
  className?: string;
  title?: string;
};

export function Icon({ name, className, title }: IconProps) {
  return (
    <svg
      aria-hidden={title ? undefined : true}
      className={className ? `icon ${className}` : "icon"}
      fill="none"
      role={title ? "img" : undefined}
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="1.6"
      viewBox="0 0 24 24"
    >
      {title && <title>{title}</title>}
      {iconGlyphs[name]}
    </svg>
  );
}
