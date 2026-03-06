import { isString } from "lodash"

export function length(length: number) {
  return (v: unknown): boolean | string => {
    if (isString(v) && v.length !== length) {
      return `Must be ${length} characters`
    }

    return true
  }
}

export default length
