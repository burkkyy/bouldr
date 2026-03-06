import type { ThemeTypes } from "./ThemeTypes"

const THEME: ThemeTypes = {
  name: "THEME",
  dark: false,
  variables: {
    "border-color": "#e5eaef",
  },
  colors: {
    primary: "#439392",
    secondary: "#D9A756",
    info: "#539BFF",
    success: "#0B7E0B",
    accent: "#45748D",
    warning: "#FFAE1F",
    error: "#9E0E0E",

    appHeader: "#170a04",

    lightprimary: "#f5fcfd",
    lightsecondary: "#E8F7FF",
    lightsuccess: "#E6FFFA",
    lighterror: "#FDEDE8",
    lightwarning: "#FEF5E5",
    lightinfo: "#EBF3FE",

    textPrimary: "#170a04",
    textSecondary: "#170a04",

    borderColor: "#e5eaef",
    inputBorder: "#374B73",
    containerBg: "#ffffff",

    background: "#F5F9FC",

    hoverColor: "#f6f9fc",
    surface: "#fff",
    "on-surface-variant": "#fff",
    grey100: "#F2F6FA",
    grey200: "#EAEFF4",
  },
}

export { THEME }
