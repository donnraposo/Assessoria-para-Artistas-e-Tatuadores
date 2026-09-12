import type { ReactElement } from "react";

import type { IconName } from "./iconName";

export const iconGlyphs: Record<IconName, ReactElement> = {
  overview: <><rect height="7" width="7" x="3" y="3" rx="1.5" /><rect height="7" width="7" x="14" y="3" rx="1.5" /><rect height="7" width="7" x="3" y="14" rx="1.5" /><rect height="7" width="7" x="14" y="14" rx="1.5" /></>,
  create: <><circle cx="12" cy="12" r="9" /><path d="M12 8v8M8 12h8" /></>,
  artist: <><circle cx="12" cy="8" r="3.5" /><path d="M5 20a7 7 0 0 1 14 0" /></>,
  studio: <><path d="M4 10 12 4l8 6v10a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1Z" /><path d="M9.5 21v-6h5v6" /></>,
  proposal: <><path d="M6 3h8l4 4v14H6Z" /><path d="M14 3v4h4" /><path d="M9 13h6M9 17h4" /></>,
  reservation: <><rect height="16" width="17" x="3.5" y="4.5" rx="2" /><path d="M3.5 9.5h17M8 3v3M16 3v3" /><path d="m9.5 14.5 2 2 3.5-3.5" /></>,
  lead: <><circle cx="12" cy="12" r="8" /><circle cx="12" cy="12" r="3.5" /><path d="M12 4v3M12 17v3M4 12h3M17 12h3" /></>,
  cancellation: <><circle cx="12" cy="12" r="8.5" /><path d="m9 9 6 6M15 9l-6 6" /></>,
  logistics: <><path d="M2.5 16.5h12v-9h-12Z" /><path d="M14.5 11h4l3 3v2.5h-7Z" /><circle cx="7" cy="18.5" r="1.8" /><circle cx="17.5" cy="18.5" r="1.8" /></>,
  schedule: <><rect height="16" width="17" x="3.5" y="4.5" rx="2" /><path d="M3.5 9.5h17M8 3v3M16 3v3" /><path d="M8 14h3M8 17.5h8" /></>,
  portfolio: <><rect height="15" width="18" x="3" y="4.5" rx="2" /><circle cx="8.5" cy="10" r="1.75" /><path d="m4 17 5-4.5 4 3.5 3-2.5 4 3.5" /></>,
  guest: <><path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11Z" /><circle cx="12" cy="10" r="2.5" /></>,
  trip: <><path d="M3 14.5 21 8l-1.5 4.5-6 2L10 21l-1.5-5Z" /><path d="m13.5 14.5-3 6.5" /></>,
  revenue: <><rect height="12" width="18" x="3" y="6" rx="2" /><circle cx="12" cy="12" r="2.75" /><path d="M6.5 12h.01M17.5 12h.01" /></>,
  alert: <><path d="M12 3.5 21.5 20h-19Z" /><path d="M12 10v4M12 17h.01" /></>,
  approved: <><circle cx="12" cy="12" r="8.5" /><path d="m8.25 12.25 2.5 2.5 5-5.5" /></>,
  declined: <><circle cx="12" cy="12" r="8.5" /><path d="M8.5 12h7" /></>,
  pending: <><circle cx="12" cy="12" r="8.5" /><path d="M12 7.5V12l3 2" /></>,
  arrow: <path d="M5 12h13m-5.5-5.5L18 12l-5.5 5.5" />,
  signout: <><path d="M14.5 7.5V5a1.5 1.5 0 0 0-1.5-1.5H5.5A1.5 1.5 0 0 0 4 5v14a1.5 1.5 0 0 0 1.5 1.5H13a1.5 1.5 0 0 0 1.5-1.5v-2.5" /><path d="M10 12h10m-3.5-3.5L20 12l-3.5 3.5" /></>,
  bell: <><path d="M6.5 10a5.5 5.5 0 0 1 11 0c0 4 1.5 5.5 1.5 5.5H5S6.5 14 6.5 10Z" /><path d="M10 19a2.2 2.2 0 0 0 4 0" /></>,
  empty: <><path d="M4 8.5 12 4l8 4.5v7L12 20l-8-4.5Z" /><path d="M4 8.5 12 13l8-4.5M12 13v7" /></>,
  upload: <><path d="M12 16V4.5m0 0L7.5 9M12 4.5 16.5 9" /><path d="M4.5 15v3.5A1.5 1.5 0 0 0 6 20h12a1.5 1.5 0 0 0 1.5-1.5V15" /></>,
  trash: <><path d="M4.5 7h15M9.5 7V4.5h5V7" /><path d="M6.5 7l1 13h9l1-13" /><path d="M10.5 11v5M13.5 11v5" /></>,
};
