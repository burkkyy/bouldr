import { isString } from "lodash"

export function clamp(min: number, max: number) {
  return (v: unknown): boolean | string => {
    if (isString(v) && (v.length < min || v.length > max)) {
      return `Must be between ${min} and ${max} characters`
    }

    return true
  }
}

export default clamp
