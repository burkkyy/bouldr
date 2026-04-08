import type { Region } from "@/api/regions-api"

export type ParsedBoulderInfo = {
  name: string | null
  grade: number | null
  description: string | null
  coordinates: string | null
  regionId: number | null
}

const GRADE_RE = /\bV(\d{1,2})\b/i
const COORD_RE = /(-?\d{1,3}\.\d+),\s*(-?\d{1,3}\.\d+)/

const KNOWN_AREA_KEYWORDS = [
  "squamish",
  "nanaimo",
  "whistler",
  "vancouver",
  "victoria",
  "duncan",
  "parksville",
]

export function parseBoulderDescription(
  text: string,
  regions: Region[]
): ParsedBoulderInfo {
  const result: ParsedBoulderInfo = {
    name: null,
    grade: null,
    description: null,
    coordinates: null,
    regionId: null,
  }

  if (!text.trim()) return result

  // Extract grade (V0-V17)
  const gradeMatch = text.match(GRADE_RE)
  if (gradeMatch) {
    const gradeNum = parseInt(gradeMatch[1], 10)
    if (gradeNum >= 0 && gradeNum <= 17) {
      result.grade = gradeNum
    }
  }

  // Extract coordinates
  const coordMatch = text.match(COORD_RE)
  if (coordMatch) {
    const lat = parseFloat(coordMatch[1])
    const lng = parseFloat(coordMatch[2])
    if (lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) {
      result.coordinates = `${lat}, ${lng}`
    }
  }

  // Try to match a region from the text
  const lowerText = text.toLowerCase()
  for (const region of regions) {
    if (lowerText.includes(region.name.toLowerCase())) {
      result.regionId = region.id
      break
    }
  }

  // Extract name using heuristics:
  // Look for quoted text as a boulder name
  const quotedMatch = text.match(/["']([^"']+)["']/)
  if (quotedMatch) {
    result.name = quotedMatch[1]
  } else {
    // Look for "called X" or "named X" patterns
    const namedMatch = text.match(/(?:called|named)\s+([A-Za-z][A-Za-z0-9\s'-]{1,30})/i)
    if (namedMatch) {
      result.name = namedMatch[1].trim()
    }
  }

  // The whole text becomes the description (cleaned up)
  let desc = text
  // Remove extracted parts from description to keep it clean
  if (gradeMatch) desc = desc.replace(gradeMatch[0], "").trim()
  if (coordMatch) desc = desc.replace(coordMatch[0], "").trim()

  // Clean up extra whitespace and punctuation artifacts
  desc = desc.replace(/\s{2,}/g, " ").replace(/^[,.\s]+|[,.\s]+$/g, "").trim()

  if (desc) {
    result.description = desc
  }

  return result
}
