import { isNull } from "lodash"

export function formatMoney(input: number | string | null, decimals = 2): string | null {
  if (isNull(input)) return null

  const numVal = parseFloat(`${input}`)

  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(numVal)
}
