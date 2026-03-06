import { isNil } from "lodash"
import { DateTime, DateTimeFormatOptions, LocaleOptions } from "luxon"

export function formatDate(
  date: Date | string | null,
  formatOpts: DateTimeFormatOptions = DateTime.DATE_FULL,
  opts?: LocaleOptions
) {
  if (isNil(date)) return ""

  if (date instanceof Date) {
    return DateTime.fromJSDate(date).toLocaleString(formatOpts, opts)
  }

  return DateTime.fromISO(date).toLocaleString(formatOpts, opts)
}

export function formatDateShort(date: string | null): string {
  if (isNil(date)) {
    return "N/A"
  }
  const utcDate = DateTime.fromISO(date).setZone("utc")
  return utcDate.toFormat("yyyy-MM-dd")
}

export function formatDateRelative(date: string | null, options = undefined): string | null {
  if (isNil(date)) {
    return "N/A"
  }
  const _date = new Date(date)
  return DateTime.fromJSDate(_date).toRelative(options)
}

export function formatDateLong(date: string | null): string {
  if (isNil(date)) {
    return "N/A"
  }
  const _date = new Date(date)
  const dateOptions = {
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "UTC",
  }
  return _date.toLocaleString("en-US", dateOptions as Intl.DateTimeFormatOptions)
}

export function formatDateForPicker(date: string | null): string {
  if (isNil(date)) {
    return "N/A"
  }
  const utcDate = DateTime.fromISO(date).setZone("utc")
  return utcDate.toFormat("yyyy-MM-dd")
}

export default formatDate
