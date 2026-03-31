export async function resizeImage(
  file: File,
  maxWidth: number,
  maxHeight: number,
  quality: number = 0.9
): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()

    reader.onerror = () => reject(new Error("Failed to read file"))

    reader.onload = (e) => {
      const img = new Image()

      img.onerror = () => reject(new Error("Failed to load image"))

      img.onload = () => {
        // Calculate new dimensions while maintaining aspect ratio
        let { width, height } = img

        if (width > maxWidth || height > maxHeight) {
          const aspectRatio = width / height

          if (width > height) {
            width = maxWidth
            height = width / aspectRatio
          } else {
            height = maxHeight
            width = height * aspectRatio
          }
        }

        // Create canvas and draw resized image
        const canvas = document.createElement("canvas")
        canvas.width = width
        canvas.height = height

        const ctx = canvas.getContext("2d", { alpha: true })
        if (!ctx) {
          reject(new Error("Failed to get canvas context"))
          return
        }

        ctx.clearRect(0, 0, width, height)
        ctx.drawImage(img, 0, 0, width, height)
        const dataUrl = canvas.toDataURL("image/png", quality)

        resolve(dataUrl)
      }

      img.src = e.target?.result as string
    }

    reader.readAsDataURL(file)
  })
}

export async function resizeToStandard(file: File): Promise<string> {
  return resizeImage(file, 512, 512, 0.9)
}

export default {
  resizeImage,
  resizeToStandard,
}
