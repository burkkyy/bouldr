function hexToRgb(hex: string) {
  hex = hex.replace("#", "")
  const bigint = parseInt(hex, 16)
  const r = (bigint >> 16) & 255
  const g = (bigint >> 8) & 255
  const b = bigint & 255
  return { r, g, b }
}

function rgbToHex(r: number, g: number, b: number) {
  return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toUpperCase()
}

export function combineHexColors(hex1: string, hex2: string) {
  const rgb1 = hexToRgb(hex1)
  const rgb2 = hexToRgb(hex2)

  const r = Math.round((rgb1.r + rgb2.r) / 2)
  const g = Math.round((rgb1.g + rgb2.g) / 2)
  const b = Math.round((rgb1.b + rgb2.b) / 2)

  return rgbToHex(r, g, b)
}
