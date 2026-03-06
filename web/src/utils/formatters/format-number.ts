import { isNull, isUndefined } from "lodash";

export function formatInteger(input: number | string | null): string {
  if (isNull(input) || isUndefined(input)) return "—";

  const numVal = Number(input);
  if (isNaN(numVal)) return "—";

  return numVal.toLocaleString("en-US", {
    maximumFractionDigits: 0,
  });
}

export function formatPercent(input: number | string | null): string {
  if (isNull(input) || isUndefined(input)) return "—";

  const numVal = Number(input);
  if (isNaN(numVal)) return "—";

  return `${numVal.toFixed(0)}%`;
}
